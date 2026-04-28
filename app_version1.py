from datetime import datetime, timedelta
import os, time, json
import streamlit as st
from core.ai_companion import load_ai_companion
from backend.chat_manager import DATA_DIR, save_conversation, load_conversation, delete_conversation, rename_conversation, toggle_pin_status
from backend.helper import get_ai_response

# Page Configuration
st.set_page_config(page_title="Lumina ✨", page_icon="✨", layout="centered")

# Initialize session state for a new chat
def initialize_new_chat():
    st.session_state.clear()
    st.session_state.messages = []
    st.session_state.context = "General"
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.current_chat_title = "Untitled"

if "messages" not in st.session_state:
    initialize_new_chat()

# --- Sidebar for Controls and History ---
with st.sidebar:
    st.title("Lumina ✨")

    if st.button("➕ New Chat", use_container_width=True):
        initialize_new_chat()
        st.rerun()

    st.divider()
    st.header("Chat History")

    try:
        chat_files = sorted(
            [f for f in os.listdir(DATA_DIR) if f.endswith(".json")],
            reverse=True
        )
        
        # Cache metadata (title and pinned status) to avoid re-reading files
        if 'chat_metadata' not in st.session_state:
            st.session_state.chat_metadata = {}
            for f in chat_files:
                session_id = f.replace('.json','')
                try:
                    with open(os.path.join(DATA_DIR, f), 'r') as file:
                        data = json.load(file)
                        st.session_state.chat_metadata[session_id] = {
                            "title": data.get('title', 'Untitled Chat'),
                            "pinned": data.get('pinned', False)
                        }
                except:
                     st.session_state.chat_metadata[session_id] = { "title": "Invalid Log", "pinned": False }
        
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        groups = {"Pinned": [], "Today": [], "Yesterday": [], "Previous 7 Days": [], "Older": []}
        
        for session_id in [f.replace('.json', '') for f in chat_files]:
            metadata = st.session_state.chat_metadata.get(session_id)
            if not metadata: continue
            
            if metadata.get("pinned"):
                groups["Pinned"].append(session_id)
                continue

            try:
                chat_date = datetime.strptime(session_id, "%Y%m%d_%H%M%S").date()
                if chat_date == today: groups["Today"].append(session_id)
                elif chat_date == yesterday: groups["Yesterday"].append(session_id)
                elif today - chat_date <= timedelta(days=7): groups["Previous 7 Days"].append(session_id)
                else: groups["Older"].append(session_id)
            except ValueError:
                groups["Older"].append(session_id)

        for group_name, session_ids in groups.items():
            if session_ids:
                with st.expander(group_name, expanded=(group_name in ["Pinned", "Today"])):
                    for session_id in session_ids:
                        metadata = st.session_state.chat_metadata[session_id]
                        title = metadata["title"]
                        is_pinned = metadata["pinned"]

                        col1, col2 = st.columns([0.85, 0.15])
                        
                        with col1:
                            if st.button(title, key=f"load_{session_id}", use_container_width=True, help=f"Load '{title}'"):
                                load_conversation(session_id)
                        
                        with col2:
                           with st.popover("⋮", use_container_width=True):
                                pin_unpin_label = "Unpin" if is_pinned else "Pin"
                                if st.button(pin_unpin_label, key=f"pin_{session_id}", use_container_width=True):
                                    toggle_pin_status(session_id)
                                    del st.session_state.chat_metadata # Force refresh
                                    st.rerun()

                                if st.button("Rename", key=f"edit_{session_id}", use_container_width=True):
                                    st.session_state.renaming_chat_id = session_id
                                    st.rerun()
                                
                                if st.button("Delete", key=f"del_{session_id}", use_container_width=True, type="primary"):
                                    delete_conversation(session_id)
                                    del st.session_state.chat_metadata
                                    if st.session_state.session_id == session_id:
                                        initialize_new_chat()
                                    st.rerun()
    except FileNotFoundError:
        st.write("No history yet.")

    if st.session_state.get("renaming_chat_id"):
        sid_to_rename = st.session_state.renaming_chat_id
        current_title = st.session_state.chat_metadata.get(sid_to_rename, {}).get("title", "")
        
        with st.form(key="rename_form"):
            st.write(f"Renaming: *{current_title}*")
            new_title = st.text_input("New Title", value=current_title, label_visibility="collapsed")
            if st.form_submit_button("Save"):
                rename_conversation(sid_to_rename, new_title)
                del st.session_state.chat_metadata
                st.session_state.renaming_chat_id = None
                st.rerun()

# --- Main Chat Interface ---

if not st.session_state.messages:
    st.markdown("<h1 style='text-align: center;'>Lumina ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Your brilliant AI study companion. How can I help you today?</p>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("Explain a concept")
            st.write("e.g., *'What is polymorphism in OOP?'*")
    with col2:
         with st.container(border=True):
            st.subheader("Define a term")
            st.write("e.g., *'Tell me about hash tables.'*")

else:
    st.subheader(st.session_state.current_chat_title)
    st.caption(f"Current Context: {st.session_state.context}")
    st.divider()
    for i, message in enumerate(st.session_state.messages):
        role_icon = "👤" if message["role"] == "user" else "✨"
        with st.chat_message(message["role"], avatar=role_icon):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                # Simplified copy button
                st.button("📋 Copy", key=f"copy_{st.session_state.session_id}_{i}", on_click=lambda c=message["content"]: (st.toast("Copied to clipboard!")))


# --- Handle new user input ---
if prompt := st.chat_input("What would you like to discuss?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("🧠 Thinking..."):
            response, new_context = get_ai_response(prompt, st.session_state.context)
        
        # Stream the response
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.03) # Adjusted for a nice flow
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.context = new_context
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    save_conversation()
    if 'chat_metadata' in st.session_state:
        del st.session_state.chat_metadata # Force refresh on next run
    st.rerun()