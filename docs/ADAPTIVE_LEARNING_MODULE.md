# Adaptive Learning Module

## Overview

The Adaptive Learning Module is the integration layer that brings together the ML Module and Expert System to create a personalized, adaptive learning experience. It manages user state, tracks performance, adjusts difficulty dynamically, and provides intelligent recommendations based on both ML predictions and expert system rules.

## Architecture

```
adaptive_learning/
├── __init__.py              # Module exports
├── state_manager.py         # Central state management (Singleton)
├── difficulty_manager.py    # Adaptive difficulty adjustment
├── recommendation_engine.py # Intelligent recommendations
├── performance_tracker.py   # Performance analytics
├── quiz_manager.py          # Quiz system
└── README.md               # This file
```

## Components

### 1. StateManager (state_manager.py)

**Purpose**: Central hub for managing all user state, progress, and performance data.

**Design Pattern**: Singleton pattern ensures only one instance exists across the application.

**Data Storage**:
- **JSON Files**: User profiles, preferences, session data
- **SQLite Database**: Performance history, topic statistics, time-series data

**Key Features**:
- User profile management (username, preferences, learning goals)
- Topic mastery tracking (0-100 scale per topic)
- Current difficulty levels per topic
- Performance history with timestamps
- Session state management
- Database initialization and migrations

**API**:
```python
from adaptive_learning.state_manager import StateManager

# Get singleton instance
state = StateManager()

# Load user profile
state.load_user("alice")

# Topic mastery
state.set_topic_mastery("Neural Networks", 75)
mastery = state.get_topic_mastery("Neural Networks")  # Returns: 75

# Difficulty management
state.set_topic_difficulty("Neural Networks", "Advanced")
difficulty = state.get_topic_difficulty("Neural Networks")  # Returns: "Advanced"

# Record performance
state.record_performance(
    topic="Neural Networks",
    difficulty="Advanced",
    correct=True,
    time_taken=45.2,
    question="What is backpropagation?"
)

# Get performance history
history = state.get_performance_history(
    topic="Neural Networks",
    days=7
)

# Topic statistics
stats = state.get_topic_stats("Neural Networks")
# Returns: {
#     'total_questions': 25,
#     'correct_answers': 20,
#     'success_rate': 80.0,
#     'avg_time': 42.3,
#     'last_attempt': '2025-12-11 10:30:00'
# }

# Session tracking
state.increment_topic_questions("Neural Networks")
state.increment_topic_correct("Neural Networks")
questions_count = state.get_topic_questions_since_adjustment("Neural Networks")

# Save state
state.save_user_profile()
```

**Database Schema**:

**performance_history** table:
- id (INTEGER PRIMARY KEY)
- timestamp (TEXT)
- topic (TEXT)
- difficulty (TEXT)
- correct (INTEGER 0/1)
- time_taken (REAL seconds)
- question (TEXT)

**topic_stats** table:
- topic (TEXT PRIMARY KEY)
- total_questions (INTEGER)
- correct_answers (INTEGER)
- avg_time (REAL)
- last_attempt (TEXT)

**sessions** table:
- id (INTEGER PRIMARY KEY)
- start_time (TEXT)
- end_time (TEXT)
- topics_covered (TEXT JSON array)
- total_questions (INTEGER)
- success_rate (REAL)

### 2. DifficultyManager (difficulty_manager.py)

**Purpose**: Implements adaptive difficulty adjustment based on user performance.

**Adjustment Rules**:
- Evaluate performance every 3 questions per topic
- Increase difficulty if success rate ≥ 80%
- Decrease difficulty if success rate < 50%
- Stay at current level if 50% ≤ success rate < 80%

**Difficulty Levels**: Beginner → Intermediate → Advanced → Expert

**Key Features**:
- Automatic difficulty adjustment
- Performance threshold configuration
- Adjustment reasoning and explanations
- Counter reset after adjustment
- Boundary protection (can't go below Beginner or above Expert)

**API**:
```python
from adaptive_learning.difficulty_manager import DifficultyManager
from adaptive_learning.state_manager import StateManager

state = StateManager()
state.load_user("alice")
diff_manager = DifficultyManager(state)

# Check if adjustment is needed
topic = "Neural Networks"
should_adjust = diff_manager.should_adjust_difficulty(topic)

if should_adjust:
    # Calculate adjustment
    action, new_difficulty, reason = diff_manager.calculate_difficulty_adjustment(topic)
    # action: "increase", "decrease", or "maintain"
    # new_difficulty: "Beginner", "Intermediate", "Advanced", or "Expert"
    # reason: Human-readable explanation
    
    print(f"Action: {action}")
    print(f"New Difficulty: {new_difficulty}")
    print(f"Reason: {reason}")
    
    # Apply adjustment
    diff_manager.apply_difficulty_adjustment(topic, action, new_difficulty)
    
# Get current difficulty
current_difficulty = diff_manager.get_current_difficulty(topic)
```

**Example Output**:
```
Action: increase
New Difficulty: Advanced
Reason: Success rate is 85.0% over last 3 questions - increasing difficulty
```

### 3. RecommendationEngine (recommendation_engine.py)

**Purpose**: Generate intelligent recommendations by combining ML predictions and expert system rules.

**Data Sources**:
1. **ML Module**: Topic classification, difficulty prediction, performance forecasting
2. **Expert System**: Prerequisite rules, learning paths, domain knowledge
3. **Performance Tracker**: Historical trends, weak areas, success patterns

**Recommendation Types**:
- **Next Topic**: What to study next based on prerequisites and performance
- **Practice Recommendations**: Topics needing more practice
- **Learning Path**: Structured curriculum based on goals
- **Difficulty Adjustment**: When to increase/decrease difficulty
- **Resource Suggestions**: Additional materials for struggling topics

**Key Features**:
- Multi-source recommendation fusion
- Context-aware suggestions
- Prerequisite validation
- Performance-based prioritization
- Lazy loading of modules (avoids circular imports)

**API**:
```python
from adaptive_learning.recommendation_engine import RecommendationEngine
from adaptive_learning.state_manager import StateManager

state = StateManager()
state.load_user("alice")
rec_engine = RecommendationEngine(state)

# Get comprehensive recommendations
recommendations = rec_engine.get_recommendations(
    current_topic="Neural Networks",
    recent_performance=[
        {'topic': 'Neural Networks', 'correct': True},
        {'topic': 'Neural Networks', 'correct': True},
        {'topic': 'Neural Networks', 'correct': False}
    ]
)
# Returns: {
#     'next_topics': ['Convolutional Neural Networks', 'Recurrent Neural Networks'],
#     'practice_topics': ['Backpropagation', 'Gradient Descent'],
#     'learning_path': ['CNN Basics', 'CNN Architectures', 'Transfer Learning'],
#     'difficulty_advice': 'Consider increasing difficulty for Neural Networks',
#     'reasoning': 'Based on 67% recent success rate...'
# }

# Suggest next topic
next_topic = rec_engine.suggest_next_topic("Neural Networks")
# Returns: "Convolutional Neural Networks"

# Get practice recommendations
practice_recs = rec_engine.get_practice_recommendations(topic="Machine Learning")
# Returns: ['Linear Regression', 'Logistic Regression', 'Decision Trees']
```

### 4. PerformanceTracker (performance_tracker.py)

**Purpose**: Analyze performance trends over time and generate insights.

**Analytics**:
- Success rate calculation
- Time-series trend analysis
- Topic-specific performance
- Learning velocity metrics
- Weak area identification

**Key Features**:
- Daily performance aggregation
- Trend detection (improving/declining/stable)
- Multi-day performance summaries
- Comparative analysis
- Statistical calculations

**API**:
```python
from adaptive_learning.performance_tracker import PerformanceTracker
from adaptive_learning.state_manager import StateManager

state = StateManager()
state.load_user("alice")
tracker = PerformanceTracker(state)

# Calculate success rate
success_rate = tracker.calculate_success_rate(
    topic="Neural Networks",
    days=7
)
# Returns: 78.5

# Get performance trend
trend = tracker.get_performance_trend(
    topic="Neural Networks",
    days=14
)
# Returns: {
#     'trend': 'improving',  # or 'declining' or 'stable'
#     'current_rate': 80.0,
#     'previous_rate': 65.0,
#     'change': +15.0,
#     'daily_rates': [
#         {'date': '2025-12-01', 'rate': 60.0, 'questions': 10},
#         {'date': '2025-12-02', 'rate': 70.0, 'questions': 8},
#         ...
#     ]
# }

# Get learning summary
summary = tracker.get_learning_summary(days=30)
# Returns: {
#     'total_questions': 250,
#     'total_correct': 200,
#     'overall_success_rate': 80.0,
#     'topics_studied': 15,
#     'avg_time_per_question': 35.2,
#     'most_improved_topic': 'Neural Networks',
#     'needs_practice': ['Reinforcement Learning', 'GANs'],
#     'mastered_topics': ['Python Basics', 'Linear Regression']
# }
```

### 5. QuizManager (quiz_manager.py)

**Purpose**: Comprehensive quiz system with multiple modes and detailed analytics.

**Quiz Types**:
- **Topic-Specific**: Focus on single topic
- **Mixed-Difficulty**: Questions from multiple difficulty levels
- **Time-Limited**: Timed quizzes with countdowns
- **Adaptive**: Difficulty adjusts during quiz
- **Review Mode**: Practice wrong answers

**Key Features**:
- Question selection and randomization
- Timer management
- Answer validation
- Score calculation with grading
- Detailed result analysis
- Wrong answer review
- Comparison with previous attempts
- Topic breakdown statistics

**API**:
```python
from adaptive_learning.quiz_manager import QuizManager
from adaptive_learning.state_manager import StateManager

state = StateManager()
state.load_user("alice")
quiz_manager = QuizManager(state)

# Create a quiz
quiz_id = quiz_manager.create_quiz(
    topic="Neural Networks",
    difficulty="Intermediate",
    num_questions=10,
    time_limit=600,  # 10 minutes in seconds
    mix_difficulties=False
)

# Start the quiz
quiz_manager.start_quiz(quiz_id)

# Submit answers
quiz_manager.submit_answer(
    quiz_id=quiz_id,
    question_index=0,
    user_answer="Backpropagation is an algorithm...",
    correct_answer="Backpropagation is an algorithm...",
    is_correct=True
)

# Complete the quiz
results = quiz_manager.complete_quiz(quiz_id)
# Returns: {
#     'quiz_id': 'quiz_123',
#     'score': 8,
#     'total_questions': 10,
#     'score_percentage': 80.0,
#     'grade': 'B',
#     'time_taken': 480,  # seconds
#     'time_limit': 600,
#     'topic_breakdown': {
#         'Neural Networks': {'correct': 8, 'total': 10, 'percentage': 80.0}
#     },
#     'weak_areas': ['Activation Functions', 'Loss Functions']
# }

# Get quiz summary
summary = quiz_manager.get_quiz_summary(quiz_id)

# Get wrong answers for review
wrong_answers = quiz_manager.get_wrong_answers(quiz_id)
# Returns: [
#     {
#         'question': 'What is the vanishing gradient problem?',
#         'user_answer': '...',
#         'correct_answer': '...',
#         'explanation': '...'
#     }
# ]

# Compare with previous quiz
comparison = quiz_manager.compare_with_previous(quiz_id, previous_quiz_id)
# Returns: {
#     'score_change': +10.0,  # percentage points
#     'time_change': -30,  # seconds
#     'improvement': True,
#     'areas_improved': ['Backpropagation', 'Optimization'],
#     'areas_declined': []
# }
```

**Grading Scale**:
- A: 90-100%
- B: 80-89%
- C: 70-79%
- D: 60-69%
- F: <60%

## Integration

### With ML Module

```python
from ml_module.classifier import TopicClassifier, DifficultyClassifier
from adaptive_learning.state_manager import StateManager

state = StateManager()
topic_classifier = TopicClassifier()
difficulty_classifier = DifficultyClassifier()

# Classify user question
question = "What is a convolutional neural network?"
topic, confidence = topic_classifier.predict(question)

# Predict appropriate difficulty
difficulty = difficulty_classifier.predict(question)

# Record performance
state.record_performance(
    topic=topic,
    difficulty=difficulty,
    correct=True,
    time_taken=30.0,
    question=question
)
```

### With Expert System

```python
from expert_system.knowledge_base import KnowledgeBase
from expert_system.inference_engine import InferenceEngine
from expert_system.prerequisite_graph import PrerequisiteGraph
from adaptive_learning.state_manager import StateManager

state = StateManager()
kb = KnowledgeBase()
inference = InferenceEngine(kb)
prereq_graph = PrerequisiteGraph()

# Check prerequisites
topic = "Convolutional Neural Networks"
prerequisites = prereq_graph.get_all_prerequisites(topic)

# Validate prerequisites met
for prereq in prerequisites:
    mastery = state.get_topic_mastery(prereq)
    if mastery < 70:
        print(f"Need more practice in {prereq} (current mastery: {mastery}%)")

# Get recommendations from inference engine
kb.set_topic_mastery(topic, state.get_topic_mastery(topic))
recommendations = inference.get_recommendations()
```

### In Main Application (app.py)

```python
import streamlit as st
from adaptive_learning.state_manager import StateManager
from adaptive_learning.difficulty_manager import DifficultyManager
from adaptive_learning.recommendation_engine import RecommendationEngine
from adaptive_learning.quiz_manager import QuizManager

# Initialize state
if 'state_manager' not in st.session_state:
    st.session_state.state_manager = StateManager()
    st.session_state.state_manager.load_user(st.session_state.username)

state = st.session_state.state_manager

# After each question
if user_submitted_answer:
    # Record performance
    state.record_performance(
        topic=current_topic,
        difficulty=current_difficulty,
        correct=is_correct,
        time_taken=time_taken,
        question=question_text
    )
    
    state.increment_topic_questions(current_topic)
    if is_correct:
        state.increment_topic_correct(current_topic)
    
    # Check for difficulty adjustment
    diff_manager = DifficultyManager(state)
    if diff_manager.should_adjust_difficulty(current_topic):
        action, new_diff, reason = diff_manager.calculate_difficulty_adjustment(current_topic)
        diff_manager.apply_difficulty_adjustment(current_topic, action, new_diff)
        st.info(f"Difficulty adjusted to {new_diff}: {reason}")

# Show recommendations
rec_engine = RecommendationEngine(state)
recommendations = rec_engine.get_recommendations(
    current_topic=current_topic,
    recent_performance=recent_answers
)
st.sidebar.write("Recommendations:", recommendations['next_topics'])

# Quiz mode
if quiz_mode:
    quiz_manager = QuizManager(state)
    quiz_id = quiz_manager.create_quiz(
        topic=selected_topic,
        difficulty=selected_difficulty,
        num_questions=10
    )
    quiz_manager.start_quiz(quiz_id)
    # ... quiz interface
```

## Data Flow

```
User Question
     ↓
TopicClassifier (ML) → Topic + Confidence
     ↓
DifficultyClassifier (ML) → Appropriate Difficulty
     ↓
PrerequisiteGraph (Expert) → Validate Prerequisites
     ↓
StateManager → Record Performance
     ↓
DifficultyManager → Check if Adjustment Needed
     ↓
RecommendationEngine → Generate Recommendations
     ↓
Display Response + Recommendations
```

## Configuration

### StateManager Configuration

Default user profile structure:
```json
{
    "username": "alice",
    "preferences": {
        "default_difficulty": "Intermediate",
        "questions_before_adjustment": 3,
        "increase_threshold": 80.0,
        "decrease_threshold": 50.0
    },
    "topic_mastery": {
        "Neural Networks": 75,
        "Python": 90,
        "Machine Learning": 60
    },
    "topic_difficulty": {
        "Neural Networks": "Advanced",
        "Python": "Expert",
        "Machine Learning": "Intermediate"
    },
    "learning_goals": [
        "Master Deep Learning",
        "Complete ML specialization"
    ],
    "total_sessions": 45,
    "total_questions_answered": 1250,
    "last_login": "2025-12-11 10:30:00"
}
```

### DifficultyManager Configuration

Constants (can be modified in code):
```python
QUESTIONS_BEFORE_ADJUSTMENT = 3
INCREASE_THRESHOLD = 80.0  # percentage
DECREASE_THRESHOLD = 50.0  # percentage
DIFFICULTY_ORDER = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
```

## Performance Considerations

1. **Singleton Pattern**: StateManager uses singleton to avoid multiple database connections
2. **Lazy Loading**: RecommendationEngine lazy-loads ML and Expert modules to prevent circular imports
3. **Database Indexing**: SQLite tables have indexes on frequently queried columns (topic, timestamp)
4. **Caching**: User profiles cached in memory, written to disk only on save
5. **Batch Operations**: Performance records can be batched for efficiency

## Testing

Example test file (tests/test_adaptive_learning.py):
```python
import pytest
from adaptive_learning.state_manager import StateManager
from adaptive_learning.difficulty_manager import DifficultyManager
from adaptive_learning.quiz_manager import QuizManager

def test_state_manager():
    state = StateManager()
    state.load_user("test_user")
    
    # Test topic mastery
    state.set_topic_mastery("Python", 80)
    assert state.get_topic_mastery("Python") == 80
    
    # Test difficulty
    state.set_topic_difficulty("Python", "Advanced")
    assert state.get_topic_difficulty("Python") == "Advanced"

def test_difficulty_adjustment():
    state = StateManager()
    state.load_user("test_user")
    state.set_topic_difficulty("Python", "Intermediate")
    
    # Simulate high performance
    for i in range(3):
        state.record_performance("Python", "Intermediate", True, 30.0, "Q")
        state.increment_topic_questions("Python")
        state.increment_topic_correct("Python")
    
    diff_manager = DifficultyManager(state)
    action, new_diff, reason = diff_manager.calculate_difficulty_adjustment("Python")
    
    assert action == "increase"
    assert new_diff == "Advanced"

def test_quiz_creation():
    state = StateManager()
    state.load_user("test_user")
    quiz_manager = QuizManager(state)
    
    quiz_id = quiz_manager.create_quiz(
        topic="Python",
        difficulty="Intermediate",
        num_questions=5
    )
    
    assert quiz_id in quiz_manager.active_quizzes
    assert len(quiz_manager.active_quizzes[quiz_id]['questions']) == 5
```

## Troubleshooting

### Issue: StateManager not persisting data
**Solution**: Ensure `save_user_profile()` is called before application exit. Add cleanup handlers:
```python
import atexit
state = StateManager()
atexit.register(state.save_user_profile)
```

### Issue: Difficulty not adjusting
**Solution**: Verify questions counter is being incremented:
```python
state.increment_topic_questions(topic)
if is_correct:
    state.increment_topic_correct(topic)
```

### Issue: Circular import errors
**Solution**: RecommendationEngine uses lazy imports. Ensure ML and Expert modules don't import from adaptive_learning.

### Issue: SQLite database locked
**Solution**: Only one StateManager instance should exist (singleton pattern). Don't create multiple instances.

## Future Enhancements

1. **Multi-User Support**: Currently single-user, could extend to multi-user with user ID parameter
2. **Advanced Analytics**: More sophisticated trend analysis, predictive modeling
3. **Gamification**: Points, badges, achievements based on performance
4. **Collaborative Learning**: Compare performance with peers, group quizzes
5. **Mobile Support**: REST API for mobile app integration
6. **A/B Testing**: Test different adjustment thresholds and recommendation strategies
7. **Export/Import**: Backup and restore user progress
8. **Real-time Sync**: Cloud synchronization across devices

## Summary

The Adaptive Learning Module is the intelligent core that makes the AI Study Companion truly adaptive. By combining:
- **State Management**: Persistent tracking of progress and performance
- **Difficulty Adjustment**: Automatic adaptation based on performance
- **Recommendations**: AI-powered suggestions for learning path
- **Performance Analytics**: Deep insights into learning patterns
- **Quiz System**: Comprehensive assessment capabilities

The module creates a personalized learning experience that evolves with each user interaction, ensuring optimal challenge level and accelerated learning outcomes.
