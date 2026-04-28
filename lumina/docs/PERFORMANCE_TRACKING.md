# 📊 Performance Tracking System - Implementation Guide

## Overview

The **Overall Performance** feature tracks user progress across all learning activities in Lumina. It displays:
- **Success Rate** - Percentage of questions answered correctly
- **Questions** - Total number of questions attempted  
- **Topics Studied** - Number of unique topics explored

---

## How It Works

### 1. Data Collection

Performance data is automatically recorded when users:

**a) Answer Quiz Questions:**
```python
# In app_enhanced.py, when user submits quiz answer:
is_correct = check_quiz_answer(
    user_id=st.session_state.username,
    question=q_data['question'],
    user_answer=user_answer,
    correct_answer=q_data['answer'],
    topic=q_data.get('topic', 'General'),
    difficulty=q_data.get('difficulty', 'Intermediate')
)
```

**b) Interact in Chat Mode:**
```python
# When user asks questions, the AI companion records performance:
result = tutor.ask(
    query=prompt,
    user_id=st.session_state.username,
    record_performance=True  # Tracks the interaction
)
```

### 2. Data Storage

**StateManager** stores performance data in two places:

**JSON File** (`data/profiles/{username}.json`):
```json
{
  "profile": {
    "username": "student1",
    "total_questions": 44,
    "total_correct": 35,
    "level": "Intermediate"
  },
  "topic_mastery": {
    "Python": "Proficient",
    "Machine Learning": "Learning"
  }
}
```

**SQLite Database** (`data/profiles/{username}.db`):
```sql
CREATE TABLE performance_history (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    topic TEXT,
    difficulty TEXT,
    question TEXT,
    correct INTEGER,
    time_taken REAL
);

CREATE TABLE topic_stats (
    topic TEXT PRIMARY KEY,
    total_attempts INTEGER,
    total_correct INTEGER,
    mastery_level TEXT,
    last_practiced TEXT
);
```

### 3. Data Retrieval

**Frontend calls `get_user_stats()`:**
```python
# In app_enhanced.py:
stats = get_user_stats(st.session_state.username, days=30)

# Returns:
{
    'total_questions': 44,
    'total_correct': 35,
    'overall_success_rate': 79.5,
    'topics_studied': 8,
    'mastered_topics': ['Python', 'Data Structures'],
    'needs_practice': ['Machine Learning', 'Deep Learning']
}
```

**Processing Flow:**
```
UI Request
   ↓
get_user_stats() (backend/helper.py)
   ↓
PerformanceTracker.get_learning_summary()
   ↓
StateManager.get_overall_stats() + get_all_topic_stats()
   ↓
Aggregates data from JSON + SQLite
   ↓
Returns formatted stats to UI
```

---

## Implementation Details

### StateManager Methods

**Recording Performance:**
```python
state = StateManager()
state.load_user("student1")

# Record a question attempt
state.record_performance(
    topic="Python",
    difficulty="Intermediate",
    question="What is a lambda function?",
    correct=True,
    time_taken=25.0
)

# Update counters
state.increment_topic_questions("Python")
state.increment_topic_correct("Python")
```

**Retrieving Stats:**
```python
# Overall stats
overall = state.get_overall_stats()
# Returns: {
#     'total_questions': 44,
#     'total_correct': 35,
#     'success_rate': 79.5,
#     'mastered_topics': 2,
#     'learning_topics': 3
# }

# Per-topic stats
all_topics = state.get_all_topic_stats()
# Returns: [
#     {
#         'topic': 'Python',
#         'attempts': 15,
#         'correct': 12,
#         'success_rate': 80.0,
#         'mastery_level': 'Proficient'
#     },
#     ...
# ]
```

### PerformanceTracker Methods

**Calculating Success Rate:**
```python
tracker = PerformanceTracker(state)

# Topic-specific success rate
rate = tracker.calculate_success_rate(topic="Python")
# Returns: 80.0

# Overall success rate
rate = tracker.calculate_success_rate(topic=None)
# Returns: 79.5
```

**Getting Learning Summary:**
```python
summary = tracker.get_learning_summary(days=30)
# Returns: {
#     'total_questions': 44,
#     'overall_success_rate': 79.5,
#     'topics_studied': 8,
#     'mastered_topics': ['Python', 'Data Structures'],
#     'needs_practice': ['Machine Learning'],
#     'trend': 'improving'
# }
```

---

## UI Display Logic

### Progress Card Display

```python
# In app_enhanced.py:
with st.expander("📊 Your Progress", expanded=True):
    stats = get_user_stats(st.session_state.username, days=30)
    
    if stats and stats.get('total_questions', 0) > 0:
        # Show performance card
        st.markdown(f"""
        <div class='stats-card'>
            <h3>🎯 Overall Performance</h3>
            <p><b>Success Rate:</b> {stats['overall_success_rate']:.1f}%</p>
            <p><b>Questions:</b> {stats['total_questions']}</p>
            <p><b>Topics Studied:</b> {stats['topics_studied']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show welcome message for new users
        st.info("Welcome! Your progress will appear here.")
```

### Mastered Topics Badge
```python
mastered = stats.get('mastered_topics', [])
if mastered:
    st.success(f"✅ Mastered: {', '.join(mastered[:3])}")
```

### Needs Practice Warning
```python
needs_practice = stats.get('needs_practice', [])
if needs_practice:
    st.warning(f"💪 Practice: {', '.join(needs_practice[:3])}")
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    User Actions                         │
│  • Answers Quiz Questions                              │
│  • Asks Questions in Chat                              │
│  • Interacts with Learning Content                     │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              Backend Functions                          │
│  • check_quiz_answer()                                 │
│  • record_interaction()                                │
│  • tutor.ask() with record_performance=True            │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              StateManager                               │
│  • record_performance()                                │
│  • increment_topic_questions()                         │
│  • increment_topic_correct()                           │
│  • Updates JSON + SQLite                               │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              Data Storage                               │
│  ┌──────────────────┐     ┌────────────────────┐      │
│  │ JSON Profile     │     │ SQLite Database    │      │
│  │ • User profile   │     │ • Performance hist.│      │
│  │ • Topic mastery  │     │ • Topic statistics │      │
│  │ • Difficulty     │     │ • Time-series data │      │
│  └──────────────────┘     └────────────────────┘      │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│          Retrieval (When UI Loads)                      │
│  get_user_stats() → PerformanceTracker                 │
│  → get_learning_summary()                              │
│  → StateManager.get_overall_stats()                    │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                  UI Display                             │
│  📊 Overall Performance Card                           │
│  • Success Rate: 79.5%                                 │
│  • Questions: 44                                       │
│  • Topics Studied: 8                                   │
│  ✅ Mastered: Python, Data Structures                  │
│  💪 Practice: Machine Learning                         │
└─────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Problem: Shows 0% Success Rate with 0 Questions

**Cause:** User hasn't answered any questions yet.

**Solution:** 
1. Take a quiz in Quiz Mode
2. Answer questions in Chat Mode
3. Data will update automatically

### Problem: Stats Not Updating

**Cause:** Session state or caching issue.

**Solution:**
```python
# Refresh the page (Streamlit reloads)
# Or clear cache:
st.cache_data.clear()
```

### Problem: Missing Topics Studied Count

**Cause:** `topics_studied` calculation issue.

**Fix Applied:**
```python
# In performance_tracker.py get_learning_summary():
all_topics = self.state.get_all_topic_stats()
topics_studied = len([t for t in all_topics if t.get('attempts', 0) > 0])
```

---

## Testing

### Manual Test
```bash
# Run performance tracking test:
python tests/test_performance_tracking.py
```

### Expected Output:
```
✓ User loaded: test_performance_user
✓ Recorded 15 questions across 3 topics

📊 Stats from get_user_stats (UI):
  Total Questions: 15
  Overall Success Rate: 80.0%
  Topics Studied: 3
  Mastered Topics: []
  Needs Practice: []

✅ SUCCESS: Performance tracking is working!
```

### Integration Test
```bash
# Run all integration tests:
python tests/test_integration.py
```

---

## Recent Fixes (December 11, 2024)

### 1. Fixed `get_learning_summary()` Return Format
**Issue:** UI expected `overall_success_rate` but function returned `success_rate`

**Fix:**
```python
return {
    'overall_success_rate': overall['success_rate'],
    'success_rate': overall['success_rate'],  # Backwards compatibility
    'topics_studied': topics_studied,  # Now properly calculated
    ...
}
```

### 2. Added Topics Studied Calculation
**Issue:** `topics_studied` was returning mastered count instead of total studied

**Fix:**
```python
all_topics = self.state.get_all_topic_stats()
topics_studied = len([t for t in all_topics if t.get('attempts', 0) > 0])
```

### 3. Improved Error Handling
**Issue:** Errors were silently failing

**Fix:**
```python
except Exception as e:
    print(f"Error getting user stats: {e}")
    traceback.print_exc()
    return default_empty_stats
```

### 4. Added Welcome Message for New Users
**Issue:** Empty stats showed nothing

**Fix:**
```python
if stats and stats.get('total_questions', 0) > 0:
    # Show performance card
else:
    # Show welcome message
    st.info("Welcome! Your progress will appear here.")
```

---

## Best Practices

### 1. Always Load User First
```python
state = StateManager()
state.load_user(user_id)  # Required!
state.record_performance(...)
```

### 2. Record Performance Immediately
```python
# Right after checking answer:
is_correct = check_answer(user_answer, correct_answer)
state.record_performance(topic, difficulty, question, is_correct, time_taken)
state.increment_topic_questions(topic)
if is_correct:
    state.increment_topic_correct(topic)
```

### 3. Use Helper Functions
```python
# Instead of direct StateManager calls:
stats = get_user_stats(user_id, days=30)  # Preferred
# vs
state = StateManager()
overall = state.get_overall_stats()  # More complex
```

### 4. Handle Empty Data Gracefully
```python
if stats and stats.get('total_questions', 0) > 0:
    # Show data
else:
    # Show empty state message
```

---

## Future Enhancements

- [ ] Real-time progress charts
- [ ] Weekly/monthly progress reports
- [ ] Comparison with other users (anonymized)
- [ ] Achievement badges
- [ ] Streak tracking
- [ ] Export progress to PDF
- [ ] Progress goals and targets
- [ ] Topic-specific progress cards

---

*Last Updated: December 11, 2024*  
*Status: ✅ Fully Functional*  
*Tested: Performance tracking working correctly*
