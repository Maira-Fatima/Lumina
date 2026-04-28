# Core Module - NLP & Query Processing

## Overview

The Core module handles all natural language processing, query matching, and topic navigation. It's the foundation that processes user queries and finds the best matching answers from the knowledge base.

## Components

### 1. `ai_companion.py` - Main AI Orchestration

**Purpose**: Unified class that coordinates all system components (NLP, ML, Expert System, Adaptive Learning)

**Key Features**:
- Lazy loading of modules (loads only when needed)
- Caching with `@st.cache_resource` for performance
- Integration of all three intelligence layers

**Main Class**: `AIStudyCompanion`

**Methods**:
- `__init__(dataset, topic_graph)`: Initialize with knowledge base
- `ask(query, user_id, record_performance)`: Process user query and return answer
- `_load_ml_module()`: Lazy load ML classifiers
- `_load_expert_system()`: Lazy load expert system
- `_load_adaptive_learning()`: Lazy load adaptive learning
- `extract_topic_from_query(query)`: Extract topic from text

**Usage**:
```python
from core.ai_companion import load_ai_companion

tutor = load_ai_companion()  # Cached, loads once
result = tutor.ask("What is machine learning?", user_id="student_123")
print(result['answer'])
```

**Returns**:
```python
{
    'answer': str,              # The answer text
    'corrected_query': str,     # Corrected version of query
    'corrections': list,        # List of corrections made
    'suggestions': dict,        # Suggested corrections
    'topic': str,               # Detected topic
    'difficulty': str,          # Detected difficulty
    'related_topics': list,     # Related topics
    'prerequisites': list,      # Required prerequisites
    'prerequisites_met': bool,  # Are prerequisites satisfied
    'recommendations': dict,    # Learning recommendations
    'difficulty_adjusted': bool,# Was difficulty changed
    'adjustment_reason': str    # Why difficulty was changed
}
```

---

### 2. `engine.py` - Query Matching Engine

**Purpose**: Finds the best matching answer using TF-IDF and cosine similarity

**Key Features**:
- TF-IDF vectorization for efficient search
- Cosine similarity for relevance scoring
- Typo correction integration
- Confidence threshold filtering

**Main Class**: `QueryMatchingEngine`

**Methods**:
- `__init__(dataset)`: Initialize with Q&A dataset
- `fit()`: Train TF-IDF vectorizer on questions
- `find_match(query, threshold=0.2)`: Find best matching answer

**How It Works**:
1. Preprocesses all questions in knowledge base
2. Creates TF-IDF matrix (term frequency-inverse document frequency)
3. For each query:
   - Corrects typos
   - Preprocesses query
   - Converts to TF-IDF vector
   - Computes cosine similarity with all questions
   - Returns best match if similarity > threshold

**Example**:
```python
from core.engine import QueryMatchingEngine

engine = QueryMatchingEngine(knowledge_base)
engine.fit()

result = engine.find_match("What is marchine lerning?")
# Auto-corrects to "machine learning"
print(result['answer'])
print(f"Similarity: {result['similarity']}")
```

---

### 3. `nlp_utils.py` - NLP Utilities

**Purpose**: Text preprocessing, typo correction, and linguistic processing

**Key Features**:
- Text preprocessing (lowercase, tokenization, lemmatization)
- Fuzzy matching for typo correction
- Technical term dictionary (100+ terms)
- Suggestion generation for ambiguous queries

**Functions**:

**`preprocess_text(text)`**
- Converts to lowercase
- Tokenizes into words
- Removes punctuation and stopwords
- Lemmatizes words
- Returns cleaned text

**`correct_typos(text, confidence_threshold=90)`**
- Uses fuzzy matching (fuzzywuzzy library)
- Checks against technical term dictionary
- Returns corrected text and list of corrections
- Only corrects if confidence ≥ threshold

**`suggest_corrections(text)`**
- Generates suggestions for potential typos
- Returns dictionary of word: [suggestions]
- Helps when correction confidence is low

**Technical Dictionary** includes:
- ML terms: neural network, gradient descent, backpropagation
- Algorithm terms: binary search, dynamic programming
- Programming: object oriented, polymorphism, inheritance
- And 100+ more terms

**Example**:
```python
from core.nlp_utils import preprocess_text, correct_typos

# Preprocessing
clean = preprocess_text("What is Machine Learning?")
# Returns: "machine learning"

# Typo correction
corrected, changes = correct_typos("masheen lerning")
# Returns: ("machine learning", [("masheen", "machine", 95), ("lerning", "learning", 92)])

# Suggestions
suggestions = suggest_corrections("maching")
# Returns: {"maching": ["machine", "matching", "caching"]}
```

---

### 4. `data_loader.py` - Data Loading

**Purpose**: Load knowledge base and manage NLTK data

**Functions**:

**`download_nltk_data()`**
- Downloads required NLTK packages:
  - punkt (tokenizer)
  - stopwords (common words to remove)
  - wordnet (lemmatization)
- Checks if already installed
- Called automatically on first run

**`get_expanded_knowledge_base()`**
- Loads 7,350-entry knowledge base from cache
- Falls back to combined_data if cache missing
- Returns list of dictionaries with structure:
```python
{
    "question": str,
    "answer": str,
    "topic": str,
    "intent": str,
    "difficulty": str
}
```

**`combined_data`**
- Small fallback dataset (30 entries)
- Used if main knowledge base not found
- Covers: OOP, DSA, AI, ML, Data Mining, Database

**Example**:
```python
from core.data_loader import get_expanded_knowledge_base, download_nltk_data

# Download NLTK data
download_nltk_data()

# Load knowledge base
kb = get_expanded_knowledge_base()
print(f"Loaded {len(kb)} entries")  # 7350

# Access entry
entry = kb[0]
print(entry['question'])
print(entry['answer'])
print(entry['topic'])
```

---

### 5. `topic_graph.py` - Topic Navigation

**Purpose**: Build and navigate relationships between topics

**Key Features**:
- Graph-based topic relationships
- BFS/DFS search for related topics
- Similarity-based connections
- Topic clustering

**Main Class**: `SearchNavigationModule`

**Methods**:
- `__init__(topic_graph)`: Initialize with topic graph
- `get_related_topics(topic, method='bfs', max_depth=2)`: Find related topics
- `search_path(start, end)`: Find learning path between topics

**Graph Structure**:
```python
{
    "Python Basics": ["OOP", "Data Structures", "Functions"],
    "Machine Learning": ["Python Basics", "Mathematics", "Statistics"],
    "Deep Learning": ["Machine Learning", "Neural Networks"]
}
```

**Functions**:

**`build_topic_graph(dataset)`**
- Creates graph from knowledge base
- Connects topics that appear in related questions
- Returns adjacency list representation

**Example**:
```python
from core.topic_graph import build_topic_graph, SearchNavigationModule

# Build graph
graph = build_topic_graph(knowledge_base)

# Navigate
navigator = SearchNavigationModule(graph)
related = navigator.get_related_topics("Machine Learning", method="bfs")
# Returns: ["Python Basics", "Deep Learning", "Statistics", "Data Science"]
```

---

## Data Flow in Core Module

```
User Query: "What is masheen lerning?"
    ↓
nlp_utils.correct_typos()
    ↓
Corrected: "What is machine learning?"
    ↓
nlp_utils.preprocess_text()
    ↓
Processed: "machine learning"
    ↓
engine.find_match()
    ↓
TF-IDF Vectorization + Cosine Similarity
    ↓
Best Match Found (similarity=0.95)
    ↓
Return Answer + Metadata
```

## Performance Characteristics

- **Query Processing**: <100ms for preprocessing
- **Similarity Matching**: <200ms for 7,350 entries
- **Typo Correction**: <50ms per query
- **Caching**: ~5x speedup with @st.cache_resource
- **Memory Usage**: ~50MB for knowledge base

## Configuration

**TF-IDF Settings** (in engine.py):
- Default similarity threshold: 0.2
- Adjustable per query
- Lower = more results, higher = stricter matching

**Typo Correction** (in nlp_utils.py):
- Default confidence threshold: 90%
- Uses Levenshtein distance
- Technical dictionary: 100+ terms

**Preprocessing** (in nlp_utils.py):
- Removes English stopwords
- Uses WordNet lemmatizer
- Preserves technical terms

## Error Handling

All functions include try-except blocks:
- Graceful fallbacks for missing data
- Informative error messages
- Continues with reduced functionality rather than crashing

## Testing

Test all core functionality:
```bash
python test_integration.py
```

Specific tests:
```python
# Test query matching
from core.engine import QueryMatchingEngine
engine = QueryMatchingEngine(knowledge_base)
engine.fit()
result = engine.find_match("test query")
assert result['answer'] is not None

# Test NLP utilities
from core.nlp_utils import preprocess_text
assert preprocess_text("HELLO World!") == "hello world"

# Test data loading
from core.data_loader import get_expanded_knowledge_base
kb = get_expanded_knowledge_base()
assert len(kb) > 0
```

## Dependencies

Required packages:
```
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
nltk>=3.8.0
fuzzywuzzy>=0.18.0
python-Levenshtein>=0.21.1
```

## Future Enhancements

- [ ] Add semantic search using embeddings
- [ ] Implement question generation
- [ ] Add multilingual support
- [ ] Improve topic graph with weights
- [ ] Add answer confidence scores
- [ ] Implement query expansion
