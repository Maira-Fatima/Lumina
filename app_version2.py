from datetime import datetime, timedelta
import os, time, json
import streamlit as st
from core.ai_companion import load_ai_companion
from backend.chat_manager import DATA_DIR, save_conversation, load_conversation, delete_conversation, rename_conversation, toggle_pin_status
from backend.helper import get_ai_response, get_user_stats, get_recommendations_for_user, create_quiz, check_quiz_answer

# Page Configuration
st.set_page_config(page_title="Lumina ✨", page_icon="✨", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
    .stButton > button {
        border-radius: 10px;
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_new_chat():
    messages = st.session_state.get("messages", [])
    mode = st.session_state.get("mode", "chat")
    username = st.session_state.get("username", "guest")
    
    st.session_state.clear()
    st.session_state.messages = messages
    st.session_state.mode = mode
    st.session_state.username = username
    st.session_state.context = "General"
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.current_chat_title = "Untitled"
    st.session_state.show_recommendations = False

if "messages" not in st.session_state:
    initialize_new_chat()

if "mode" not in st.session_state:
    st.session_state.mode = "chat"

if "username" not in st.session_state:
    st.session_state.username = "guest"

# --- Sidebar ---
with st.sidebar:
    st.title("Lumina ✨")
    
    # Username
    username_input = st.text_input("👤 Username", value=st.session_state.username)
    if username_input != st.session_state.username:
        st.session_state.username = username_input
        st.rerun()
    
    st.divider()
    
    # Progress Dashboard
    with st.expander("📊 Your Progress", expanded=True):
        try:
            stats = get_user_stats(st.session_state.username, days=30)
            
            if stats and stats.get('total_questions', 0) > 0:
                # User has data - show stats
                st.markdown(f"""
                <div class='stats-card'>
                    <h3>🎯 Overall Performance</h3>
                    <p><b>Success Rate:</b> {stats.get('overall_success_rate', 0):.1f}%</p>
                    <p><b>Questions:</b> {stats.get('total_questions', 0)}</p>
                    <p><b>Topics Studied:</b> {stats.get('topics_studied', 0)}</p>
                </div>
                """, unsafe_allow_html=True)
                
                mastered = stats.get('mastered_topics', [])
                if mastered:
                    st.success(f"✅ Mastered: {', '.join(mastered[:3])}")
                
                needs_practice = stats.get('needs_practice', [])
                if needs_practice:
                    st.warning(f"💪 Practice: {', '.join(needs_practice[:3])}")
            else:
                # No data yet - show helpful message
                st.info("""
                👋 **Welcome to Lumina!**
                
                Your progress will be tracked here as you:
                - 💬 Ask questions in chat mode
                - 📝 Take quizzes
                - 🎓 Study different topics
                
                Start by asking a question or taking a quiz below!
                """)
        except Exception as e:
            st.warning(f"⚠️ Progress tracking temporarily unavailable")
            print(f"Error loading stats: {e}")
    
    st.divider()

    if st.button("➕ New Chat", use_container_width=True):
        initialize_new_chat()
        st.rerun()

    st.divider()
    st.header("Chat History")

    try:
        chat_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".json")], reverse=True)
        
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
                     st.session_state.chat_metadata[session_id] = {"title": "Invalid Log", "pinned": False}
        
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
                            if st.button(title, key=f"load_{session_id}", use_container_width=True):
                                load_conversation(session_id)
                        
                        with col2:
                           with st.popover("⋮", use_container_width=True):
                                pin_label = "Unpin" if is_pinned else "Pin"
                                if st.button(pin_label, key=f"pin_{session_id}", use_container_width=True):
                                    toggle_pin_status(session_id)
                                    del st.session_state.chat_metadata
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

# --- Main Interface ---

# Mode Toggle
col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
with col1:
    if st.button("💬 Chat", use_container_width=True, type="primary" if st.session_state.mode == "chat" else "secondary"):
        st.session_state.mode = "chat"
        st.rerun()
with col2:
    if st.button("🎯 Quiz", use_container_width=True, type="primary" if st.session_state.mode == "quiz" else "secondary"):
        st.session_state.mode = "quiz"
        st.rerun()
with col3:
    if st.button("💡 Recs", use_container_width=True):
        st.session_state.show_recommendations = not st.session_state.get("show_recommendations", False)
        st.rerun()

st.divider()

# --- Recommendations Panel ---
if st.session_state.get("show_recommendations", False):
    with st.container(border=True):
        st.subheader("💡 Personalized Recommendations")
        try:
            recs = get_recommendations_for_user(st.session_state.username, st.session_state.context)
            
            if recs and (recs.get('next_topics') or recs.get('practice_topics')):
                col1, col2 = st.columns(2)
                
                with col1:
                    if recs.get('next_topics'):
                        st.markdown("**📚 Next Topics:**")
                        for i, topic in enumerate(recs['next_topics'][:5], 1):
                            st.markdown(f"{i}. {topic}")
                    else:
                        st.info("Complete more topics to unlock new recommendations!")
                
                with col2:
                    if recs.get('practice_topics'):
                        st.markdown("**💪 Practice More:**")
                        for i, topic in enumerate(recs['practice_topics'][:5], 1):
                            st.markdown(f"{i}. {topic}")
                    else:
                        st.info("You're doing great! Keep learning.")
            else:
                st.info("📖 Start chatting or taking quizzes to get personalized recommendations!")
        except Exception as e:
            st.warning("⚠️ Recommendations temporarily unavailable")
            print(f"Recommendations error: {e}")
    st.divider()

# --- Chat Mode ---
if st.session_state.mode == "chat":
    if not st.session_state.messages:
        st.markdown("<h1 style='text-align: center;'>Lumina ✨</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Your brilliant AI study companion</p>", unsafe_allow_html=True)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("Explain a concept")
                st.write("*'What is polymorphism?'*")
        with col2:
            with st.container(border=True):
                st.subheader("Define a term")
                st.write("*'Tell me about hash tables'*")
    else:
        st.subheader(st.session_state.current_chat_title)
        st.caption(f"Context: {st.session_state.context}")
        st.divider()
        
        for i, message in enumerate(st.session_state.messages):
            role_icon = "👤" if message["role"] == "user" else "✨"
            with st.chat_message(message["role"], avatar=role_icon):
                st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("What would you like to discuss?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("🧠 Thinking..."):
                response, new_context, metadata = get_ai_response(
                    prompt, 
                    st.session_state.context,
                    user_id=st.session_state.username,
                    record_performance=True
                )
            
            # Stream response
            message_placeholder = st.empty()
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.02)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        st.session_state.context = new_context
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        save_conversation()
        if 'chat_metadata' in st.session_state:
            del st.session_state.chat_metadata
        st.rerun()

# --- Quiz Mode ---
elif st.session_state.mode == "quiz":
    st.subheader("🎯 Quiz Mode")
    
    # Initialize quiz state
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "quiz_current_q" not in st.session_state:
        st.session_state.quiz_current_q = 0
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = []
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    
    # Quiz not started - show setup
    if not st.session_state.quiz_started:
        st.markdown("### Quiz Setup")
        col1, col2 = st.columns(2)
        with col1:
            quiz_topic = st.selectbox("Topic", ["General", "Python Basics", "Machine Learning", "Data Structures", "Deep Learning", "Algorithms", "Web Development", "Cloud Computing"], index=0)
            quiz_difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced", "Expert"])
        with col2:
            quiz_num = st.number_input("Questions", 5, 50, 10)
            quiz_time = st.number_input("Time (min)", 5, 120, 15)
        
        if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
            # Create quiz
            with st.spinner("Generating quiz..."):
                quiz = create_quiz(
                    st.session_state.username,
                    quiz_topic,
                    quiz_difficulty,
                    quiz_num,
                    quiz_time
                )
                
                if quiz and quiz.get('questions'):
                    st.session_state.quiz_data = quiz
                    st.session_state.quiz_current_q = 0
                    st.session_state.quiz_answers = []
                    st.session_state.quiz_started = True
                    st.rerun()
                else:
                    st.error(f"No questions found for {quiz_topic} at {quiz_difficulty} level. Try different settings.")
    
    # Quiz started - show questions
    else:
        quiz = st.session_state.quiz_data
        current_q = st.session_state.quiz_current_q
        questions = quiz['questions']
        
        # Quiz completed
        if current_q >= len(questions):
            st.success("🎉 Quiz Completed!")
            
            # Calculate score
            correct = sum(1 for ans in st.session_state.quiz_answers if ans['correct'])
            total = len(questions)
            score = (correct / total * 100) if total > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{score:.0f}%")
            with col2:
                st.metric("Correct", f"{correct}/{total}")
            with col3:
                st.metric("Topic", quiz['topic'])
            
            # Show review
            st.markdown("### Review Your Answers")
            for i, ans in enumerate(st.session_state.quiz_answers):
                with st.expander(f"Question {i+1} - {'✅ Correct' if ans['correct'] else '❌ Incorrect'}"):
                    st.markdown(f"**Q:** {ans['question']}")
                    st.markdown(f"**Your Answer:** {ans['user_answer']}")
                    if not ans['correct']:
                        st.markdown(f"**Correct Answer:** {ans['correct_answer']}")
            
            # Restart button
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📝 New Quiz", use_container_width=True):
                    st.session_state.quiz_started = False
                    st.session_state.quiz_data = None
                    st.session_state.quiz_current_q = 0
                    st.session_state.quiz_answers = []
                    st.rerun()
            with col2:
                if st.button("💬 Back to Chat", use_container_width=True):
                    st.session_state.mode = "chat"
                    st.session_state.quiz_started = False
                    st.rerun()
        
        # Show current question
        else:
            progress = current_q / len(questions)
            st.progress(progress, text=f"Question {current_q + 1} of {len(questions)}")
            
            q_data = questions[current_q]
            st.markdown(f"### Question {current_q + 1}")
            st.markdown(f"**Topic:** {q_data.get('topic', 'General')} | **Difficulty:** {q_data.get('difficulty', 'Intermediate')}")
            st.markdown(f"**{q_data['question']}**")
            
            # MCQ Options
            options = q_data.get('options', [])
            if options:
                # Display as radio buttons
                user_answer = st.radio(
                    "Choose your answer:",
                    options,
                    key=f"mcq_{current_q}",
                    index=None
                )
            else:
                # Fallback to text input if no options available
                user_answer = st.text_area("Your Answer:", key=f"answer_{current_q}", height=100)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("Submit Answer ➡️", type="primary", use_container_width=True):
                    if user_answer and (isinstance(user_answer, str) and user_answer.strip()):
                        # Check answer
                        is_correct = check_quiz_answer(
                            st.session_state.username,
                            q_data['question'],
                            user_answer,
                            q_data['answer'],
                            q_data.get('topic', 'General'),
                            q_data.get('difficulty', 'Intermediate')
                        )
                        
                        # Record answer
                        st.session_state.quiz_answers.append({
                            'question': q_data['question'],
                            'user_answer': user_answer,
                            'correct_answer': q_data['answer'],
                            'correct': is_correct,
                            'topic': q_data.get('topic', 'General'),
                            'difficulty': q_data.get('difficulty', 'Intermediate')
                        })
                        
                        # Move to next question
                        st.session_state.quiz_current_q += 1
                        st.rerun()
                    else:
                        st.warning("Please enter an answer before submitting.")
            with col2:
                if st.button("Exit Quiz", use_container_width=True):
                    st.session_state.quiz_started = False
                    st.session_state.mode = "chat"
                    st.rerun()

# --- Footer ---
st.markdown("---")
st.caption("Powered by Lumina AI ✨ | ML + Expert System + Adaptive Learning")
