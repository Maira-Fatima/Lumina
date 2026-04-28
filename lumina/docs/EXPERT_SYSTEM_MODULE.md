# Expert System Module 🧠

## Overview

The **Expert System Module** implements an advanced rule-based reasoning system that provides intelligent guidance, prerequisite checking, and personalized learning recommendations. It uses forward and backward chaining inference to make intelligent decisions about the learning path.

---

## Module Structure

```
expert_system/
├── __init__.py                  # Module initialization
├── knowledge_base.py            # Facts, rules, and domain knowledge storage
├── inference_engine.py          # Forward/backward chaining reasoning
├── prerequisite_graph.py        # Topic dependency management
├── rule_manager.py              # Rule generation and management
├── rules/                       # JSON rule files
│   ├── prerequisites.json       # Prerequisite checking rules
│   ├── learning_paths.json      # Structured learning curricula
│   └── recommendations.json     # Smart recommendation rules
└── README.md                    # This file
```

---

## Components

### 1. **knowledge_base.py** - Knowledge Repository

#### **KnowledgeBase**
Central storage for facts, rules, and user state.

**What it stores:**
1. **Facts**: Current state assertions (e.g., "mastered_BFS", "struggling_Neural Networks")
2. **Rules**: If-then logic for reasoning
3. **User State**: Current learning progress and preferences
4. **Domain Knowledge**: Topic relationships and metadata

**Key Methods:**
- `add_fact(fact)` - Assert a new fact
- `has_fact(fact)` - Check if fact exists
- `check_conditions(conditions)` - Evaluate rule conditions
- `set_topic_mastery(topic, level)` - Update mastery level
- `get_mastered_topics()` - List of mastered topics
- `save_state(filepath)` / `load_state(filepath)` - Persistence

**Example Usage:**
```python
from expert_system import KnowledgeBase

kb = KnowledgeBase()

# Add facts about student progress
kb.set_topic_mastery("BFS", "Mastered")
kb.set_topic_mastery("DFS", "Learning")
kb.add_fact("struggling_A* Search")

# Query knowledge
if kb.has_fact("mastered_BFS"):
    print("Student has mastered BFS")

mastered = kb.get_mastered_topics()
print(f"Mastered topics: {mastered}")
```

---

### 2. **inference_engine.py** - Reasoning Engine

#### **InferenceEngine**
Implements forward and backward chaining for intelligent reasoning.

**Forward Chaining (Data-Driven):**
- Start with known facts
- Apply rules whose conditions are met
- Derive new facts until no more can be inferred
- Used for: proactive recommendations, automatic prerequisite checking

**Backward Chaining (Goal-Driven):**
- Start with a goal
- Find rules that can achieve the goal
- Recursively prove conditions
- Used for: "Can I learn topic X?", prerequisite validation

**Key Methods:**
- `forward_chain(max_depth)` - Derive new facts from rules
- `backward_chain(goal)` - Prove if goal is achievable
- `get_recommendations(context)` - Generate smart recommendations
- `explain_reasoning(conclusion)` - Explain how conclusion was reached
- `resolve_conflicts(rules)` - Handle multiple applicable rules

**Example Usage:**
```python
from expert_system import KnowledgeBase, InferenceEngine

kb = KnowledgeBase()
engine = InferenceEngine(kb)

# Add student progress
kb.set_topic_mastery("BFS", "Mastered")
kb.set_topic_mastery("DFS", "Mastered")

# Apply forward chaining to derive recommendations
new_facts = engine.forward_chain()
print(f"Derived facts: {new_facts}")

# Check if student can learn A*
can_learn, required = engine.backward_chain("recommend_A* Search")
if can_learn:
    print("Student is ready for A* Search!")
else:
    print(f"Missing: {required}")

# Get recommendations
recommendations = engine.get_recommendations()
for rec in recommendations:
    print(f"Recommend: {rec['topic']} (confidence: {rec['confidence']})")
    print(f"  Reason: {rec['reason']}")
```

---

### 3. **prerequisite_graph.py** - Dependency Management

#### **PrerequisiteGraph**
Manages complex topic dependency relationships.

**Features:**
- Directed Acyclic Graph (DAG) of 100+ topics
- Transitive prerequisite resolution
- Learning path generation
- Missing prerequisite detection
- Curriculum structuring by difficulty

**Topic Coverage:**
- **Fundamentals**: Python, Mathematics
- **DSA**: Arrays, Trees, Graphs, Hash Tables
- **Search Algorithms**: BFS, DFS, A*, Dijkstra
- **Mathematics**: Linear Algebra, Calculus, Probability, Statistics
- **Machine Learning**: Supervised, Unsupervised, Linear/Logistic Regression, SVM, KNN, Naive Bayes
- **Deep Learning**: Neural Networks, CNN, RNN, LSTM, GRU, Transformers, Attention, GANs
- **NLP**: Tokenization, Word Embeddings, Word2Vec, BERT, GPT, NER, Sentiment Analysis
- **Computer Vision**: Image Processing, Object Detection, YOLO, R-CNN, Segmentation
- **Reinforcement Learning**: MDP, Q-Learning, SARSA, DQN, Policy Gradients, Actor-Critic
- **Expert Systems**: Knowledge Representation, Logic, Inference, Fuzzy Logic

**Key Methods:**
- `get_prerequisites(topic)` - Direct prerequisites
- `get_all_prerequisites(topic)` - All transitive prerequisites
- `get_missing_prerequisites(topic, mastered)` - What's missing
- `can_learn(topic, mastered)` - Check if ready
- `get_next_topics(mastered)` - Topics ready to learn
- `generate_learning_path(goal, mastered)` - Personalized path
- `get_curriculum(domain)` - Structured curriculum
- `validate_path(path)` - Check if path is valid

**Example Usage:**
```python
from expert_system import PrerequisiteGraph

prereq_graph = PrerequisiteGraph()

# Check prerequisites
prereqs = prereq_graph.get_all_prerequisites("Neural Networks")
print(f"To learn Neural Networks, you need: {prereqs}")
# Output: ['Python Basics', 'Linear Algebra', 'Calculus', 'Supervised Learning']

# Find missing prerequisites
mastered = {"Python Basics", "Linear Algebra"}
missing = prereq_graph.get_missing_prerequisites("Neural Networks", mastered)
print(f"Still need to learn: {missing}")
# Output: ['Calculus', 'Supervised Learning']

# Generate personalized learning path
path = prereq_graph.generate_learning_path("BERT", mastered)
print(f"Learning path to BERT: {path}")

# Get structured curriculum
curriculum = prereq_graph.get_curriculum("DL")  # Deep Learning
for level, topics in curriculum.items():
    print(f"\n{level}:")
    for topic in topics:
        print(f"  - {topic}")
```

---

### 4. **rule_manager.py** - Rule Generation & Management

#### **RuleManager**
Creates and manages expert system rules.

**Generated Rules:**

**1. Prerequisite Rules (8 rules)**
- Validate prerequisite chains
- Block advanced topics without foundations
- Suggest missing prerequisites
- Example: "Cannot learn Neural Networks without Linear Algebra"

**2. Learning Paths (7 curated paths)**
- Machine Learning Beginner
- Machine Learning Intermediate
- Deep Learning Path
- NLP Specialist
- Computer Vision Path
- Reinforcement Learning Path
- AI Foundations

**3. Recommendation Rules (10 rules)**
- Progressive topic suggestions
- Struggle detection and support
- Specialization guidance
- Practice and project recommendations

**Rule Format:**
```json
{
    "id": "rule_1",
    "type": "recommendation",
    "name": "Recommend DFS after BFS mastery",
    "conditions": ["mastered_BFS", "not_mastered_DFS"],
    "actions": ["recommend_DFS"],
    "confidence": 0.9,
    "priority": 8,
    "reason": "DFS is a natural next step after mastering BFS"
}
```

**Key Methods:**
- `generate_all_rules()` - Create all default rules
- `generate_prerequisite_rules()` - Prerequisite checking
- `generate_learning_path_rules()` - Structured paths
- `generate_recommendation_rules()` - Smart suggestions
- `add_custom_rule(rule, type)` - Add new rules

**Example Usage:**
```python
from expert_system import RuleManager

rule_manager = RuleManager()
rule_manager.generate_all_rules()

# Add custom rule
custom_rule = {
    "id": "custom_1",
    "type": "recommendation",
    "name": "Project recommendation",
    "conditions": ["mastered_CNN", "mastered_RNN"],
    "actions": ["recommend_build_chatbot"],
    "confidence": 0.8,
    "priority": 7,
    "reason": "Ready for practical projects"
}

rule_manager.add_custom_rule(custom_rule, 'recommendations')
```

---

## Complete System Example

Here's how all components work together:

```python
from expert_system import (
    KnowledgeBase,
    InferenceEngine,
    PrerequisiteGraph,
    RuleManager
)

# 1. Initialize system
rule_manager = RuleManager()
rule_manager.generate_all_rules()

kb = KnowledgeBase()
engine = InferenceEngine(kb)
prereq_graph = PrerequisiteGraph()

# 2. Set student's current state
mastered_topics = {"Python Basics", "BFS", "DFS", "Linear Algebra"}

for topic in mastered_topics:
    kb.set_topic_mastery(topic, "Mastered")

# 3. Student wants to learn Neural Networks
goal = "Neural Networks"

# Check prerequisites
all_prereqs = prereq_graph.get_all_prerequisites(goal)
missing = prereq_graph.get_missing_prerequisites(goal, mastered_topics)

print(f"To learn {goal}:")
print(f"  Required: {all_prereqs}")
print(f"  Still need: {missing}")

# 4. Generate personalized learning path
path = prereq_graph.generate_learning_path(goal, mastered_topics)
print(f"\nRecommended learning path:")
for i, topic in enumerate(path, 1):
    print(f"  {i}. {topic}")

# 5. Get intelligent recommendations
kb.add_fact("high_performance_BFS")
kb.add_fact("high_performance_DFS")

recommendations = engine.get_recommendations()
print(f"\nSmart Recommendations:")
for rec in recommendations[:3]:
    print(f"  • {rec['topic']} - {rec['reason']}")

# 6. Explain reasoning
explanation = engine.explain_reasoning("recommend_A* Search")
print(f"\n{explanation}")
```

---

## API Functions for Integration

The module exposes clean APIs for `helper.py`:

```python
# In helper.py or adaptive_learning module
from expert_system import KnowledgeBase, InferenceEngine, PrerequisiteGraph

# Initialize once
kb = KnowledgeBase()
engine = InferenceEngine(kb)
prereq_graph = PrerequisiteGraph()

# Check if student can learn a topic
def can_learn_topic(topic, mastered_topics):
    return prereq_graph.can_learn(topic, mastered_topics)

# Get prerequisites
def get_missing_prerequisites(topic, mastered_topics):
    return prereq_graph.get_missing_prerequisites(topic, mastered_topics)

# Get recommendations
def get_smart_recommendations(user_state):
    # Update KB with current state
    for topic, mastery in user_state.items():
        kb.set_topic_mastery(topic, mastery)
    
    # Run inference
    recommendations = engine.get_recommendations()
    return recommendations

# Generate learning path
def create_learning_path(goal_topic, current_mastery):
    return prereq_graph.generate_learning_path(goal_topic, current_mastery)
```

---

## Data Flow

```
User Progress Data
        ↓
Knowledge Base (Facts + Rules)
        ↓
Inference Engine (Forward/Backward Chaining)
        ↓
Prerequisite Graph (Dependency Resolution)
        ↓
Smart Recommendations + Learning Paths
        ↓
Adaptive Learning Module
        ↓
User Experience
```

---

## Rule Execution Example

**Scenario**: Student has mastered BFS and DFS

1. **Facts Added**:
   - `mastered_BFS`
   - `mastered_DFS`

2. **Forward Chaining**:
   - Rule "Recommend A* after BFS/DFS" matches
   - Action: Add `recommend_A* Search`
   - New fact derived!

3. **Prerequisite Check**:
   - A* requires: BFS, DFS, Heuristics
   - Missing: Heuristics
   - Recommendation: Learn Heuristics first

4. **Final Suggestion**:
   - "You're ready for advanced search! Learn Heuristics, then A* Search."

---

## Initialization

Initialize the expert system on first run:

```bash
python -m expert_system.rule_manager
```

This creates all rule files in `expert_system/rules/`.

---

## Dependencies

- **Python Standard Library**: json, os, collections, typing
- **No external dependencies** (pure Python implementation)

---

## File Descriptions

| File | Purpose | Lines of Code |
|------|---------|---------------|
| `knowledge_base.py` | Fact and rule storage | ~250 |
| `inference_engine.py` | Forward/backward chaining | ~350 |
| `prerequisite_graph.py` | Dependency management | ~450 |
| `rule_manager.py` | Rule generation | ~400 |

---

## Integration Points

1. **Adaptive Learning Module**: Uses expert system for difficulty adjustment and recommendations
2. **ML Module**: Provides context for classification and prediction
3. **UI**: Displays prerequisite warnings and recommendations
4. **Performance Tracker**: Updates knowledge base with mastery levels

---

## Advanced Features

### Multi-Step Reasoning
```python
# Complex prerequisite chain
"To learn BERT, you need Transformers"
"To learn Transformers, you need LSTM + Attention"
"To learn LSTM, you need RNN"
"To learn RNN, you need Neural Networks"
# System automatically derives complete path!
```

### Conflict Resolution
```python
# Multiple rules fire simultaneously
# System uses priority + confidence to select best action
```

### Confidence-Based Reasoning
```python
# Recommendations include confidence scores
# Low confidence → suggest alternatives
# High confidence → strong recommendation
```

---

## Testing

Test the expert system:

```bash
python tests/test_expert_system.py
```

---

## Author Notes

This module implements a **production-grade expert system** with:
- **100+ topic dependencies** across AI domains
- **25+ inference rules** for intelligent guidance
- **Forward and backward chaining** for comprehensive reasoning
- **Personalized learning paths** based on current mastery
- **Automatic prerequisite validation**

The system is designed to be **extensible** - new topics, rules, and learning paths can be easily added through JSON files or programmatically.

---

## Future Enhancements

- [ ] Probabilistic reasoning (Bayesian networks)
- [ ] Natural language rule definition
- [ ] User-contributed rules
- [ ] Multi-user learning group recommendations
- [ ] Integration with external knowledge graphs (DBpedia, Wikidata)
