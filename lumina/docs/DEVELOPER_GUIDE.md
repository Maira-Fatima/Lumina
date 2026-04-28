# 🚀 Lumina - Developer Quick Reference Guide

**Quick access to common tasks, APIs, and troubleshooting**

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Common Tasks](#common-tasks)
3. [API Reference](#api-reference)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Testing](#testing)

---

## Quick Start

### Install & Run
```bash
# Install
pip install -r requirements.txt

# Run app
streamlit run app.py

# Run tests
python test_integration.py
```

### First Use
```python
from core.ai_companion import load_ai_companion

# Load AI (cached, only loads once)
tutor = load_ai_companion()

# Ask a question
result = tutor.ask("What is machine learning?", user_id="student_123")
print(result['answer'])
```

---

## Common Tasks

### 1. Get AI Response

```python
from backend.helper import get_ai_response
from core.ai_companion import load_ai_companion

tutor = load_ai_companion()

response = get_ai_response(
    query="What is Python?",
    user_id="student_123",
    ai_companion=tutor
)

print(response['answer'])
print(response['topic'])
print(response['difficulty'])
```

### 2. Create Quiz

```python
from backend.helper import create_quiz_from_topic

quiz = create_quiz_from_topic(
    topic="Machine Learning",
    user_id="student_123",
    ai_companion=tutor,
    num_questions=5,
    difficulty="intermediate"  # Optional, auto-adapts if None
)

# Access questions
for q in quiz['questions']:
    print(q['question'])
    print(q['options'])  # List of 4 options
    print(q['correct_answer'])
```

### 3. Check Quiz Answer

```python
from backend.helper import check_quiz_answer

result = check_quiz_answer(
    user_answer="A. Supervised learning",
    correct_answer="A. Supervised learning algorithm",
    question="What is a decision tree?",
    user_id="student_123",
    ai_companion=tutor
)

if result['is_correct']:
    print(f"✓ {result['feedback']}")
else:
    print(f"✗ {result['explanation']}")
```

### 4. Save/Load Chat

```python
from backend.chat_manager import save_chat_history, load_chat_history

# Save
messages = [
    {'role': 'user', 'content': 'Hello', 'timestamp': '2024-12-11T10:30:00'},
    {'role': 'assistant', 'content': 'Hi!', 'timestamp': '2024-12-11T10:30:05'}
]
filepath = save_chat_history(messages)

# Load
loaded = load_chat_history(filepath)
```

### 5. Track User Progress

```python
from adaptive_learning.state_manager import StateManager

state = StateManager()
state.load_user("student_123")

# Get topic mastery
mastery = state.get_topic_mastery("Machine Learning")
print(f"Mastery: {mastery}%")

# Update mastery
state.update_topic_mastery("Python", 85.0)

# Get performance history
history = state.get_performance_history("Machine Learning", limit=10)
```

### 6. Train ML Models

```python
from ml_module.model_trainer import ModelTrainingPipeline
from core.data_loader import get_expanded_knowledge_base

kb = get_expanded_knowledge_base()
pipeline = ModelTrainingPipeline(kb)

# Train all models
pipeline.train_all()

# Train individual models
pipeline.train_topic_classifier()
pipeline.train_difficulty_classifier()
pipeline.train_performance_predictor()
```

### 7. Use Expert System

```python
from expert_system import KnowledgeBase, InferenceEngine

kb = KnowledgeBase()
engine = InferenceEngine(kb)

# Check prerequisites
has_prereqs = engine.check_prerequisites("Deep Learning", "student_123")

# Get recommendations
recommendations = engine.get_recommendations("student_123")

# Get learning path
path = engine.get_learning_path("Algorithms", "Machine Learning")
```

---

## API Reference

### Core Module APIs

#### `ai_companion.ask(query, user_id, record_performance=True)`
**Returns:**
```python
{
    'answer': str,
    'corrected_query': str,
    'corrections': list,
    'suggestions': dict,
    'topic': str,
    'difficulty': str,
    'related_topics': list,
    'prerequisites': list,
    'prerequisites_met': bool,
    'recommendations': dict
}
```

#### `engine.find_match(query, threshold=0.2)`
**Returns:**
```python
{
    'answer': str,
    'similarity': float,
    'matched_question': str
}
```

#### `nlp_utils.preprocess_text(text)`
**Returns:** `str` (cleaned text)

#### `nlp_utils.correct_typos(text, confidence_threshold=90)`
**Returns:** `(corrected_text: str, corrections: list)`

### Backend Module APIs

#### `get_ai_response(query, user_id, ai_companion)`
See "Common Tasks #1" above

#### `create_quiz_from_topic(topic, user_id, ai_companion, num_questions=5, difficulty=None)`
See "Common Tasks #2" above

#### `check_quiz_answer(user_answer, correct_answer, question, user_id, ai_companion)`
See "Common Tasks #3" above

### ML Module APIs

#### `TopicClassifier.predict(question)`
**Returns:** `str` (topic name)

#### `TopicClassifier.predict_proba(question)`
**Returns:** `dict` {topic: probability}

#### `DifficultyClassifier.predict(question)`
**Returns:** `str` ('beginner', 'intermediate', or 'advanced')

#### `PerformancePredictor.predict(features)`
**Parameters:** `features` (list of 8 values)
**Returns:** `float` (0-1, predicted performance)

### Adaptive Learning APIs

#### `StateManager.load_user(user_id)`
Loads user profile and state

#### `StateManager.get_topic_mastery(topic)`
**Returns:** `float` (0-100)

#### `StateManager.update_topic_mastery(topic, level)`
Updates mastery level

#### `StateManager.record_performance(user_id, topic, score, difficulty)`
Records quiz/interaction performance

#### `DifficultyManager.should_adjust_difficulty(user_id, topic)`
**Returns:** `(bool, str, str)` (should_adjust, new_difficulty, reason)

#### `RecommendationEngine.get_recommendations(user_id)`
**Returns:** `dict` with recommendations

---

## Configuration

### Query Matching Settings

**File:** `core/engine.py`

```python
# Similarity threshold (0.0-1.0)
similarity_threshold = 0.2  # Lower = more lenient

# TF-IDF settings
max_features = 10000
ngram_range = (1, 2)  # Unigrams + bigrams
```

### Typo Correction Settings

**File:** `core/nlp_utils.py`

```python
# Confidence threshold (0-100)
confidence_threshold = 90  # % similarity required

# Technical dictionary
TECHNICAL_TERMS = [
    'machine learning',
    'neural network',
    'binary search',
    # Add more terms...
]
```

### Quiz Settings

**File:** `adaptive_learning/quiz_manager.py`

```python
# Quiz generation
NUM_QUESTIONS = 5
NUM_MCQ_OPTIONS = 4
ANSWER_MAX_WORDS = 50  # Shorten long answers

# Difficulty adjustment
LEVEL_UP_THRESHOLD = 0.7    # 70% to level up
LEVEL_DOWN_THRESHOLD = 0.3  # 30% to level down
```

### ML Model Settings

**File:** `ml_module/classifier.py`

```python
# TF-IDF vectorization
TfidfVectorizer(
    max_features=10000,      # Topic classifier
    max_features=5000,       # Difficulty classifier
    ngram_range=(1, 2),
    min_df=2
)

# Naive Bayes
MultinomialNB(alpha=1.0)     # Laplace smoothing
```

### Performance Tracking

**File:** `adaptive_learning/performance_tracker.py`

```python
# Database: data/user_data.db
# Tables: user_profiles, performance_history, topic_statistics

# Retention period
HISTORY_DAYS = 365  # Keep 1 year of data
```

---

## Troubleshooting

### Issue: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "NLTK data not found"

**Solution:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

Or run app once (downloads automatically)

### Issue: "Knowledge base not loaded"

**Check:**
```python
from core.data_loader import get_expanded_knowledge_base

kb = get_expanded_knowledge_base()
print(f"Loaded {len(kb)} entries")  # Should be 7,350
```

**If 0 entries:**
- Check `data/expanded_knowledge_base_cache.json` exists
- Verify file size is ~5MB
- Regenerate if corrupted

### Issue: "ML models not found"

**Check:**
```bash
ls ml_module/models/
# Should see:
# - topic_classifier.pkl
# - difficulty_classifier.pkl
# - performance_predictor.pkl
```

**If missing:**
```python
from ml_module.model_trainer import ModelTrainingPipeline
from core.data_loader import get_expanded_knowledge_base

kb = get_expanded_knowledge_base()
pipeline = ModelTrainingPipeline(kb)
pipeline.train_all()
```

### Issue: "Streamlit caching errors"

**Solution:**
```bash
streamlit cache clear
```

Or restart Streamlit:
```bash
# Kill process
Ctrl+C

# Restart
streamlit run app.py
```

### Issue: "Slow query responses"

**Check:**
1. Knowledge base size (should be 7,350)
2. Caching enabled (`@st.cache_resource` on `load_ai_companion`)
3. TF-IDF vectorizer fitted

**Optimize:**
```python
# Reduce max_features if memory constrained
TfidfVectorizer(max_features=5000)  # Instead of 10000
```

### Issue: "Quiz answers not matching"

**Check similarity threshold:**
```python
from fuzzywuzzy import fuzz

# Test matching
score = fuzz.ratio("user answer", "correct answer")
print(f"Similarity: {score}%")  # Should be >= 80 to match
```

**Adjust threshold in `backend/helper.py`:**
```python
SIMILARITY_THRESHOLD = 80  # Lower = more lenient
```

---

## Testing

### Run All Tests

```bash
python test_integration.py
```

**Expected Output:**
```
✓ Imports                   PASS
✓ Knowledge Base            PASS
✓ Query Engine              PASS
✓ ML Models                 PASS
✓ Expert System             PASS
✓ Adaptive Learning         PASS
✓ Backend Helper            PASS
✓ AI Companion              PASS

Total: 8/8 tests passed
```

### Run Specific Tests

```python
# Test imports
from core import ai_companion, engine, nlp_utils
from ml_module import classifier
from expert_system import knowledge_base
from adaptive_learning import state_manager

# Test query matching
from core.engine import QueryMatchingEngine
from core.data_loader import get_expanded_knowledge_base

kb = get_expanded_knowledge_base()
engine = QueryMatchingEngine(kb)
engine.fit()

result = engine.find_match("What is machine learning?")
assert result['similarity'] > 0.8

# Test ML models
from ml_module.classifier import TopicClassifier

clf = TopicClassifier()
# Load or train model
topic = clf.predict("What is a neural network?")
assert topic in ["Machine Learning", "Deep Learning", "Neural Networks"]

# Test state management
from adaptive_learning.state_manager import StateManager

state = StateManager()
state.load_user("test_user")
mastery = state.get_topic_mastery("Python")
assert 0 <= mastery <= 100
```

### Performance Testing

```python
import time

# Test query speed
start = time.time()
result = tutor.ask("What is Python?", user_id="test")
elapsed = time.time() - start
print(f"Query time: {elapsed*1000:.0f}ms")  # Should be <500ms

# Test quiz generation speed
start = time.time()
quiz = create_quiz_from_topic("ML", "test", tutor, num_questions=5)
elapsed = time.time() - start
print(f"Quiz generation time: {elapsed:.2f}s")  # Should be <2s

# Test ML inference speed
from ml_module.classifier import TopicClassifier

clf = TopicClassifier()
# Load model

start = time.time()
topic = clf.predict("Test question")
elapsed = time.time() - start
print(f"ML inference time: {elapsed*1000:.0f}ms")  # Should be <100ms
```

---

## Quick Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add to functions
logger.debug(f"Query: {query}")
logger.debug(f"Processed: {processed_query}")
logger.debug(f"Match: {match}, Similarity: {similarity}")
```

### Check System State

```python
# Check AI companion
tutor = load_ai_companion()
print(f"Knowledge base entries: {len(tutor.dataset)}")
print(f"ML module loaded: {tutor.ml_module is not None}")
print(f"Expert system loaded: {tutor.expert_system is not None}")

# Check state manager
state = StateManager()
print(f"Database path: {state.db_path}")
print(f"User profiles: {state.list_users()}")

# Check ML models
import os
models_dir = "ml_module/models"
print(f"Models found: {os.listdir(models_dir)}")
```

### Verify Data Integrity

```python
# Check knowledge base
kb = get_expanded_knowledge_base()
print(f"Total entries: {len(kb)}")
print(f"Sample entry: {kb[0]}")

# Check required fields
for entry in kb[:10]:
    assert 'question' in entry
    assert 'answer' in entry
    assert 'topic' in entry
    assert 'difficulty' in entry
    print("✓ Entry valid")
```

---

## Environment Variables

### Optional Configuration

```bash
# Data directories
export LUMINA_DATA_DIR="./data"
export LUMINA_MODELS_DIR="./ml_module/models"

# Database
export LUMINA_DB_PATH="./data/user_data.db"

# Cache
export LUMINA_CACHE_DIR="./.cache"

# Logging
export LUMINA_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
```

---

## Performance Benchmarks

### Expected Performance

| Operation | Target | Actual |
|-----------|--------|--------|
| Query processing | <500ms | ~300ms |
| Quiz generation | <2s | ~1s |
| ML inference | <100ms | ~50ms |
| Knowledge base load | <2s | ~1s |
| Chat save/load | <50ms | ~20ms |

### Memory Usage

| Component | Memory |
|-----------|--------|
| Base app | ~100MB |
| Knowledge base | ~50MB |
| ML models | ~30MB |
| User data | ~10MB |
| **Total** | **~180MB** |

---

## Useful Commands

```bash
# Install
pip install -r requirements.txt

# Run app
streamlit run app.py

# Run tests
python test_integration.py

# Train models
python -c "from ml_module.model_trainer import ModelTrainingPipeline; from core.data_loader import get_expanded_knowledge_base; kb = get_expanded_knowledge_base(); pipeline = ModelTrainingPipeline(kb); pipeline.train_all()"

# Clear cache
streamlit cache clear

# Check version
python --version
pip show streamlit

# List dependencies
pip list

# Freeze dependencies
pip freeze > requirements_frozen.txt
```

---

## File Locations

### Key Files

```
lumina/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Dependencies
├── test_integration.py             # Integration tests
│
├── data/
│   ├── expanded_knowledge_base_cache.json  # 7,350 entries
│   ├── user_data.db                        # SQLite database
│   └── chats/                              # Chat history
│
├── ml_module/models/
│   ├── topic_classifier.pkl
│   ├── difficulty_classifier.pkl
│   └── performance_predictor.pkl
│
└── [module directories]/
    └── README.md                   # Module documentation
```

---

## Quick Links

- **Main README:** `README.md`
- **Testing Report:** `TESTING_REPORT.md`
- **Features Summary:** `FEATURES_SUMMARY.md`
- **Core Module Docs:** `core/README.md`
- **Backend Docs:** `backend/README.md`
- **ML Module Docs:** `ml_module/README.md`
- **Expert System Docs:** `expert_system/README.md`
- **Adaptive Learning Docs:** `adaptive_learning/README.md`

---

*Quick Reference Guide v2.0*  
*Last Updated: December 11, 2024*
