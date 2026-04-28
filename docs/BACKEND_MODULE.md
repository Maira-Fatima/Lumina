# Backend Module - API Helpers & Chat Management

## Overview

The Backend module provides helper functions and utilities that connect the Streamlit UI to the AI companion. It handles chat history, quiz creation, answer verification, and response formatting.

## Components

### 1. `helper.py` - Core Helper Functions

**Purpose**: Bridge between UI and AI companion with simplified API

**Key Functions**:

---

#### `get_ai_response(query, user_id, ai_companion)`

**Purpose**: Get AI response with typo correction and suggestions

**Parameters**:
- `query` (str): User's question
- `user_id` (str): Unique user identifier
- `ai_companion` (AIStudyCompanion): The AI companion instance

**Returns**:
```python
{
    'answer': str,              # The answer text
    'corrected_query': str,     # Auto-corrected query
    'suggestions': dict,        # Correction suggestions
    'topic': str,               # Detected topic
    'difficulty': str,          # Detected difficulty level
    'related_topics': list,     # Related topics to explore
    'prerequisites': list,      # Required prerequisites
    'prerequisites_met': bool,  # Are prerequisites satisfied
    'recommendations': dict     # Personalized recommendations
}
```

**Example**:
```python
from backend.helper import get_ai_response

response = get_ai_response(
    query="What is masheen lerning?",
    user_id="student_123",
    ai_companion=tutor
)

print(response['answer'])  # Main answer
print(response['corrected_query'])  # "What is machine learning?"
print(response['topic'])  # "Machine Learning"
```

**Features**:
- Automatic typo correction
- Suggestion generation for ambiguous terms
- Topic and difficulty detection
- Performance tracking
- Prerequisite checking

---

#### `create_quiz_from_topic(topic, user_id, ai_companion, num_questions=5, difficulty=None)`

**Purpose**: Generate MCQ quiz based on topic and user level

**Parameters**:
- `topic` (str): The topic to quiz on
- `user_id` (str): Unique user identifier
- `ai_companion` (AIStudyCompanion): The AI companion instance
- `num_questions` (int, optional): Number of questions (default: 5)
- `difficulty` (str, optional): Difficulty level ('beginner', 'intermediate', 'advanced')

**Returns**:
```python
{
    'quiz_id': str,                    # Unique quiz identifier
    'topic': str,                      # Quiz topic
    'difficulty': str,                 # Difficulty level
    'questions': [                     # List of questions
        {
            'question': str,           # Question text
            'options': [str, ...],     # 4 MCQ options
            'correct_answer': str,     # Correct option
            'explanation': str         # Why this is correct
        },
        ...
    ]
}
```

**Example**:
```python
from backend.helper import create_quiz_from_topic

quiz = create_quiz_from_topic(
    topic="Machine Learning",
    user_id="student_123",
    ai_companion=tutor,
    num_questions=5,
    difficulty="intermediate"
)

print(f"Quiz ID: {quiz['quiz_id']}")
for i, q in enumerate(quiz['questions'], 1):
    print(f"\nQuestion {i}: {q['question']}")
    for opt in q['options']:
        print(f"  - {opt}")
```

**Features**:
- MCQ format with 4 options
- Intelligent distractor generation
- Adaptive difficulty adjustment
- Explanation for each answer
- Unique quiz IDs for tracking

---

#### `check_quiz_answer(user_answer, correct_answer, question, user_id, ai_companion)`

**Purpose**: Check quiz answer with fuzzy matching and update user performance

**Parameters**:
- `user_answer` (str): User's selected answer
- `correct_answer` (str): The correct answer
- `question` (str): The question text
- `user_id` (str): Unique user identifier
- `ai_companion` (AIStudyCompanion): The AI companion instance

**Returns**:
```python
{
    'is_correct': bool,         # Is answer correct
    'feedback': str,            # Feedback message
    'explanation': str,         # Why answer is right/wrong
    'corrected_answer': str     # Normalized correct answer
}
```

**Example**:
```python
from backend.helper import check_quiz_answer

result = check_quiz_answer(
    user_answer="A supervised learning algorithm",
    correct_answer="A. A supervised learning algorithm used for classification",
    question="What is a decision tree?",
    user_id="student_123",
    ai_companion=tutor
)

if result['is_correct']:
    print(f"✓ Correct! {result['feedback']}")
else:
    print(f"✗ Incorrect. {result['explanation']}")
```

**Features**:
- Fuzzy matching (handles typos)
- Accepts partial matches for MCQ options
- Updates user performance automatically
- Provides detailed feedback
- Normalizes answers (removes "A.", "B.", etc.)

**Matching Logic**:
```python
# Exact match
"Machine learning" == "Machine learning" → True

# MCQ option match
"A. Neural network" contains "Neural network" → True

# Fuzzy match (80% similarity threshold)
"Nural network" ≈ "Neural network" (85% similar) → True

# Partial match
"Neural" in "A. Neural network" → True
```

---

### 2. `chat_manager.py` - Chat History Management

**Purpose**: Save and load chat conversations with timestamp tracking

**Key Functions**:

---

#### `save_chat_history(messages, filename=None)`

**Purpose**: Save chat messages to JSON file with timestamp

**Parameters**:
- `messages` (list): List of message dictionaries
- `filename` (str, optional): Custom filename (auto-generated if None)

**Message Format**:
```python
{
    'role': str,        # 'user' or 'assistant'
    'content': str,     # Message text
    'timestamp': str    # ISO format timestamp
}
```

**Returns**: `str` - Full path to saved file

**Example**:
```python
from backend.chat_manager import save_chat_history

messages = [
    {'role': 'user', 'content': 'What is AI?', 'timestamp': '2024-01-20T10:30:00'},
    {'role': 'assistant', 'content': 'AI is...', 'timestamp': '2024-01-20T10:30:05'}
]

filepath = save_chat_history(messages)
print(f"Saved to: {filepath}")
# Output: data/chats/20240120_103000.json
```

**File Structure**:
```json
{
    "session_start": "2024-01-20T10:30:00",
    "messages": [
        {
            "role": "user",
            "content": "What is AI?",
            "timestamp": "2024-01-20T10:30:00"
        },
        {
            "role": "assistant",
            "content": "AI is artificial intelligence...",
            "timestamp": "2024-01-20T10:30:05"
        }
    ]
}
```

**Features**:
- Automatic timestamp generation
- Creates `data/chats/` directory if missing
- Filename format: `YYYYMMDD_HHMMSS.json`
- Thread-safe writing

---

#### `load_chat_history(filename)`

**Purpose**: Load chat history from JSON file

**Parameters**:
- `filename` (str): Name or path of chat file

**Returns**: `list` - List of message dictionaries

**Example**:
```python
from backend.chat_manager import load_chat_history

messages = load_chat_history("20240120_103000.json")
for msg in messages:
    print(f"{msg['role']}: {msg['content']}")
```

**Error Handling**:
- Returns empty list if file not found
- Prints error message for invalid JSON
- Graceful degradation

---

#### `list_chat_sessions()`

**Purpose**: Get list of all saved chat sessions

**Returns**: `list` - Sorted list of chat filenames (newest first)

**Example**:
```python
from backend.chat_manager import list_chat_sessions

sessions = list_chat_sessions()
print(f"Found {len(sessions)} chat sessions:")
for session in sessions:
    print(f"  - {session}")
```

**Output**:
```
Found 3 chat sessions:
  - 20240120_103000.json
  - 20240119_154500.json
  - 20240118_093000.json
```

---

## Data Flow in Backend Module

```
User Query (Streamlit UI)
    ↓
get_ai_response(query, user_id, ai_companion)
    ↓
ai_companion.ask() [processes query]
    ↓
Format response with corrections & suggestions
    ↓
Return to UI for display
    ↓
save_chat_history() [persist conversation]
```

```
Quiz Request (Streamlit UI)
    ↓
create_quiz_from_topic(topic, user_id, ai_companion)
    ↓
Generate MCQ questions with options
    ↓
Return quiz to UI
    ↓
User submits answer
    ↓
check_quiz_answer(user_ans, correct_ans, question, user_id)
    ↓
Update performance + return feedback
    ↓
Display results to user
```

## Usage Examples

### Complete Chat Flow

```python
from backend.helper import get_ai_response
from backend.chat_manager import save_chat_history
from core.ai_companion import load_ai_companion
import streamlit as st

# Initialize AI companion (cached)
tutor = load_ai_companion()

# Initialize chat history in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Get user input
user_query = st.text_input("Ask a question:")

if user_query:
    # Get AI response
    response = get_ai_response(
        query=user_query,
        user_id="student_123",
        ai_companion=tutor
    )
    
    # Add to chat history
    st.session_state.messages.append({
        'role': 'user',
        'content': user_query,
        'timestamp': datetime.now().isoformat()
    })
    st.session_state.messages.append({
        'role': 'assistant',
        'content': response['answer'],
        'timestamp': datetime.now().isoformat()
    })
    
    # Display response
    st.write(response['answer'])
    
    # Show corrections if any
    if response['corrected_query'] != user_query:
        st.info(f"Did you mean: {response['corrected_query']}?")
    
    # Save chat history
    save_chat_history(st.session_state.messages)
```

### Complete Quiz Flow

```python
from backend.helper import create_quiz_from_topic, check_quiz_answer
from core.ai_companion import load_ai_companion
import streamlit as st

# Initialize AI companion
tutor = load_ai_companion()

# Create quiz
if 'quiz' not in st.session_state:
    st.session_state.quiz = create_quiz_from_topic(
        topic="Machine Learning",
        user_id="student_123",
        ai_companion=tutor,
        num_questions=5
    )

quiz = st.session_state.quiz

# Display questions
for i, q in enumerate(quiz['questions'], 1):
    st.write(f"**Question {i}:** {q['question']}")
    
    # Radio button for MCQ
    user_answer = st.radio(
        "Select your answer:",
        options=q['options'],
        key=f"q{i}"
    )
    
    # Submit button
    if st.button(f"Submit Answer {i}", key=f"submit{i}"):
        result = check_quiz_answer(
            user_answer=user_answer,
            correct_answer=q['correct_answer'],
            question=q['question'],
            user_id="student_123",
            ai_companion=tutor
        )
        
        if result['is_correct']:
            st.success(f"✓ {result['feedback']}")
        else:
            st.error(f"✗ {result['feedback']}")
            st.info(f"Explanation: {result['explanation']}")
```

## Error Handling

All functions include comprehensive error handling:

```python
# get_ai_response()
try:
    result = ai_companion.ask(query, user_id)
except Exception as e:
    return {
        'answer': "Sorry, I couldn't process that query.",
        'error': str(e)
    }

# create_quiz_from_topic()
try:
    quiz = quiz_manager.generate_mcq_quiz(topic, num_questions)
except Exception as e:
    return {
        'error': f"Could not generate quiz: {str(e)}"
    }

# check_quiz_answer()
try:
    is_correct = fuzz.ratio(user_ans, correct_ans) >= 80
except Exception as e:
    return {
        'is_correct': False,
        'feedback': "Could not verify answer",
        'error': str(e)
    }
```

## Performance Optimization

### Caching
```python
# AI companion is cached
@st.cache_resource
def load_ai_companion():
    return AIStudyCompanion(...)

# Call once, use many times
tutor = load_ai_companion()  # First call: loads
tutor = load_ai_companion()  # Second call: cached (instant)
```

### Batch Operations
```python
# Generate multiple quiz questions at once
quiz = create_quiz_from_topic(topic, user_id, tutor, num_questions=10)

# Process multiple answers
results = []
for user_ans, correct_ans, question in zip(user_answers, correct_answers, questions):
    result = check_quiz_answer(user_ans, correct_ans, question, user_id, tutor)
    results.append(result)
```

## Configuration

### Fuzzy Matching Threshold
```python
# In check_quiz_answer()
SIMILARITY_THRESHOLD = 80  # 80% match required

# Adjust for stricter/looser matching
if fuzz.ratio(user_answer, correct_answer) >= SIMILARITY_THRESHOLD:
    is_correct = True
```

### Quiz Settings
```python
# Default quiz parameters
DEFAULT_NUM_QUESTIONS = 5
DEFAULT_DIFFICULTY = None  # Auto-adapt to user level

# MCQ options
NUM_MCQ_OPTIONS = 4  # 1 correct + 3 distractors
```

### Chat History
```python
# File locations
CHAT_DIR = "data/chats/"
FILENAME_FORMAT = "%Y%m%d_%H%M%S.json"

# Timestamp format
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
```

## Testing

Test backend functionality:
```python
# Test AI response
response = get_ai_response("What is AI?", "test_user", tutor)
assert 'answer' in response
assert 'topic' in response

# Test quiz creation
quiz = create_quiz_from_topic("ML", "test_user", tutor, num_questions=3)
assert len(quiz['questions']) == 3
assert all('options' in q for q in quiz['questions'])

# Test answer checking
result = check_quiz_answer("A. Correct", "A. Correct", "Test?", "test_user", tutor)
assert result['is_correct'] == True

# Test chat save/load
messages = [{'role': 'user', 'content': 'test'}]
filepath = save_chat_history(messages)
loaded = load_chat_history(filepath)
assert len(loaded) == 1
```

## Dependencies

Required packages:
```
streamlit>=1.28.0
fuzzywuzzy>=0.18.0
python-Levenshtein>=0.21.1
```

## Future Enhancements

- [ ] Add chat export (PDF, TXT)
- [ ] Implement chat search
- [ ] Add quiz statistics dashboard
- [ ] Support bulk answer checking
- [ ] Add chat tagging/categorization
- [ ] Implement quiz review mode
- [ ] Add voice input/output
- [ ] Support image-based questions
