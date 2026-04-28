import streamlit as st
import os
import json
from backend.helper import generate_chat_title

DATA_DIR = "data/chats"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def save_conversation():
    """Saves the current conversation to a JSON file."""
    if st.session_state.messages:
        if st.session_state.get("current_chat_title", "Untitled") == "Untitled":
             st.session_state.current_chat_title = generate_chat_title(st.session_state.messages)

        filename = st.session_state.session_id
        filepath = os.path.join(DATA_DIR, f"{filename}.json")

        # Preserve pinned status if it exists
        pinned_status = False
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    pinned_status = data.get("pinned", False)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        log_data = {
            "session_id": filename,
            "title": st.session_state.current_chat_title,
            "last_context": st.session_state.context,
            "log": st.session_state.messages,
            "pinned": pinned_status
        }
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=4)

def load_conversation(session_id):
    """Loads a conversation from a JSON file into the session state."""
    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    with open(filepath, 'r') as f:
        data = json.load(f)

    st.session_state.messages = data.get("log", [])
    st.session_state.context = data.get("last_context", "General")
    st.session_state.session_id = data.get("session_id", "loaded_session")
    st.session_state.current_chat_title = data.get("title", "Untitled")
    st.rerun()

def delete_conversation(session_id):
    """Deletes a conversation file."""
    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)

def rename_conversation(session_id, new_title):
    """Renames a conversation by updating its title in the JSON file."""
    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r+') as f:
            data = json.load(f)
            data['title'] = new_title
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        st.session_state.current_chat_title = new_title

def toggle_pin_status(session_id):
    """Toggles the pinned status of a conversation."""
    filepath = os.path.join(DATA_DIR, f"{session_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r+') as f:
            data = json.load(f)
            data['pinned'] = not data.get('pinned', False)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
