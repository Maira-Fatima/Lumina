# Machine Learning Module 🤖

## Overview

The **Machine Learning Module** provides intelligent classification and prediction capabilities for the Lumina AI Study Companion. It uses supervised learning algorithms to enhance the tutoring experience through topic classification, difficulty assessment, and performance prediction.

---

## Module Structure

```
ml_module/
├── __init__.py              # Module initialization and exports
├── classifier.py            # Topic and Difficulty classifiers
├── predictor.py             # Performance prediction using Linear Regression
├── data_generator.py        # Synthetic training data generation
├── model_trainer.py         # Unified training pipeline
├── models/                  # Saved model files (.pkl)
│   ├── topic_classifier.pkl
│   ├── difficulty_classifier.pkl
│   └── performance_predictor.pkl
├── data/                    # Generated datasets
│   ├── training_data.csv
│   ├── validation_data.csv
│   ├── test_data.csv
│   └── predictor_training_data.pkl
└── README.md                # This file
```

---

## Components

### 1. **classifier.py** - Topic & Difficulty Classification

#### **TopicClassifier**
Classifies user queries into predefined topics using **Naive Bayes**.

**How it works:**
1. **Text Preprocessing**: Applies NLP preprocessing (tokenization, lemmatization, stop-word removal)
2. **TF-IDF Vectorization**: Converts text to numerical features (max 1000 features, unigrams + bigrams)
3. **Multinomial Naive Bayes**: Classifies queries with alpha=0.1 for smoothing
4. **Confidence Scoring**: Returns prediction confidence using probability estimates

**Key Methods:**
- `train(questions, topics)` - Train on question-topic pairs
- `predict(question)` - Predict single topic with confidence
- `predict_top_k(question, k=3)` - Get top K most likely topics
- `save_model()` / `load_model()` - Model persistence

**Example Usage:**
```python
from ml_module.classifier import TopicClassifier

classifier = TopicClassifier()
# classifier.train(questions, topics)  # Training done once

topic, confidence = classifier.predict("What is a neural network?")
print(f"Topic: {topic}, Confidence: {confidence:.2f}")
# Output: Topic: AI, Confidence: 0.95
```

---

#### **DifficultyClassifier**
Predicts question difficulty: **Beginner**, **Intermediate**, **Advanced**, **Expert**.

**How it works:**
- Same architecture as TopicClassifier but trained on difficulty labels
- Uses question complexity indicators (terminology, sentence structure)
- Maps difficulty to numeric scores (1-4) for adaptive learning

**Key Methods:**
- `train(questions, difficulties)` - Train on labeled data
- `predict(question)` - Predict difficulty level
- `get_difficulty_score(difficulty)` - Convert to numeric score

**Example Usage:**
```python
from ml_module.classifier import DifficultyClassifier

diff_classifier = DifficultyClassifier()
difficulty, confidence = diff_classifier.predict("Explain backpropagation")
print(f"Difficulty: {difficulty}")
# Output: Difficulty: Advanced
```

---

### 2. **predictor.py** - Performance Prediction

#### **PerformancePredictor**
Uses **Linear Regression** to predict future student performance based on historical data.

**How it works:**
1. **Feature Engineering**: Extracts features from performance history
   - Total questions attempted
   - Overall success rate
   - Average time taken
   - Average difficulty level
   - Recent success rate (last 10 questions)

2. **Regression Model**: Trains on historical patterns to predict future success
3. **Trend Analysis**: Calculates learning trajectory using sliding window
4. **Topic-Specific Metrics**: Analyzes performance per topic

**Key Methods:**
- `predict_future_performance(history)` - Predict next success rate
- `analyze_trend(history)` - Detect improvement/decline patterns
- `calculate_simple_success_rate(history)` - (correct/total) × 100
- `get_topic_performance(history, topic)` - Topic-specific metrics

**Performance Record Format:**
```python
{
    'timestamp': datetime,
    'topic': str,
    'difficulty': str,  # Beginner/Intermediate/Advanced/Expert
    'correct': bool,
    'time_taken': float  # seconds
}
```

**Example Usage:**
```python
from ml_module.predictor import PerformancePredictor

predictor = PerformancePredictor()

history = [
    {'topic': 'AI', 'difficulty': 'Beginner', 'correct': True, 'time_taken': 25},
    {'topic': 'AI', 'difficulty': 'Beginner', 'correct': True, 'time_taken': 20},
    # ... more records
]

future_rate = predictor.predict_future_performance(history)
print(f"Predicted success rate: {future_rate:.2%}")

trend = predictor.analyze_trend(history)
print(f"Learning trend: {trend['trend']}")  # improving/stable/declining
```

---

### 3. **data_generator.py** - Synthetic Data Generation

#### **DataGenerator**
Automatically generates training datasets from the expanded knowledge base.

**How it works:**
1. **Question Variations**: Generates multiple phrasings for each question
   - Template-based generation (What/How/Why/Difference)
   - Simple variations ("Tell me about X", "Explain X")
   
2. **Dataset Splitting**: 70% train, 15% validation, 15% test
3. **Performance Simulation**: Creates synthetic learning histories
   - Simulates realistic learning progression
   - Models difficulty progression over time
   - Generates time-series performance data

**Key Methods:**
- `generate_question_variations(entry, n)` - Create question variants
- `generate_training_dataset()` - Create train/val/test splits
- `generate_performance_history()` - Simulate learning sessions
- `save_datasets(output_dir)` - Save all data to files

**Example Usage:**
```python
from ml_module.data_generator import DataGenerator
from core.data_loader import get_expanded_knowledge_base

kb = get_expanded_knowledge_base()
generator = DataGenerator(kb)

# Generate and save datasets
train_df, val_df, test_df = generator.save_datasets()
print(f"Generated {len(train_df)} training samples")
```

---

### 4. **model_trainer.py** - Unified Training Pipeline

#### **ModelTrainer**
Orchestrates training for all ML models with evaluation.

**Training Pipeline:**
1. Data generation/loading
2. Topic classifier training with evaluation
3. Difficulty classifier training with evaluation
4. Performance predictor training with evaluation
5. Model persistence

**Key Methods:**
- `train_all_models(regenerate_data)` - Train everything
- `evaluate_models()` - Comprehensive evaluation report

**Evaluation Metrics:**
- **Classification**: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
- **Regression**: Mean Squared Error (MSE), Mean Absolute Error (MAE)

**Example Usage:**
```python
from ml_module.model_trainer import ModelTrainer
from core.data_loader import get_expanded_knowledge_base

kb = get_expanded_knowledge_base()
trainer = ModelTrainer(kb)

# Train all models
trainer.train_all_models(regenerate_data=True)

# Evaluate performance
metrics = trainer.evaluate_models()
print(f"Topic Accuracy: {metrics['topic_accuracy']:.2%}")
```

---

## API Functions for Integration

The module exposes clean API functions for use by `helper.py`:

```python
# In helper.py
from ml_module import TopicClassifier, DifficultyClassifier, PerformancePredictor

# Initialize (load pre-trained models)
topic_clf = TopicClassifier()
diff_clf = DifficultyClassifier()
predictor = PerformancePredictor()

# Classify topic
topic, confidence = topic_clf.predict(user_question)

# Predict difficulty
difficulty, conf = diff_clf.predict(user_question)

# Analyze performance
success_rate = predictor.calculate_simple_success_rate(history)
trend = predictor.analyze_trend(history)
```

---

## Training the Models

### Initial Training

Run the training script to create and train all models:

```bash
python -m ml_module.model_trainer
```

This will:
1. Generate 7,500+ synthetic training samples
2. Train Topic Classifier (Naive Bayes)
3. Train Difficulty Classifier (Naive Bayes)
4. Train Performance Predictor (Linear Regression)
5. Save all models to `ml_module/models/`
6. Display evaluation metrics

### Retraining

To retrain models with updated knowledge base:

```python
from ml_module.model_trainer import quick_train
quick_train()
```

---

## Model Performance

**Expected Performance Metrics:**

| Model | Metric | Expected Value |
|-------|--------|----------------|
| Topic Classifier | Accuracy | > 90% |
| Difficulty Classifier | Accuracy | > 85% |
| Performance Predictor | MAE | < 0.1 |

---

## Data Flow

```
Knowledge Base (7,500+ entries)
        ↓
Data Generator
        ↓
Training Data (70%) + Validation (15%) + Test (15%)
        ↓
Model Trainer
        ↓
Trained Models (.pkl files)
        ↓
API Functions (classifier.py, predictor.py)
        ↓
Integration with helper.py
        ↓
User Experience Enhancement
```

---

## Dependencies

- **scikit-learn**: Naive Bayes, Linear Regression, TF-IDF
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **pickle**: Model serialization
- **core.nlp_utils**: Text preprocessing

---

## File Descriptions

| File | Purpose | Lines of Code |
|------|---------|---------------|
| `__init__.py` | Module exports | ~20 |
| `classifier.py` | Topic/Difficulty classification | ~300 |
| `predictor.py` | Performance prediction | ~350 |
| `data_generator.py` | Dataset generation | ~400 |
| `model_trainer.py` | Training orchestration | ~350 |

---

## Integration Points

1. **Topic Recognition**: Replace current simple keyword matching with ML classification
2. **Adaptive Difficulty**: Use difficulty prediction to select appropriate questions
3. **Performance Tracking**: Use predictor for trend analysis and forecasting
4. **Recommendation Engine**: ML predictions feed into expert system for smart recommendations

---

## Future Enhancements

- [ ] Deep Learning models (LSTM for sequence prediction)
- [ ] Active learning for continuous improvement
- [ ] Multi-label classification for complex queries
- [ ] Transfer learning from pre-trained language models
- [ ] Real-time model updates based on user feedback

---

## Testing

Run unit tests:

```bash
python tests/test_ml_module.py
```

---

## Author Notes

This module implements the **Machine Learning** component of the Lumina AI Study Companion project. It uses classical ML algorithms (Naive Bayes, Linear Regression) chosen for their:
- **Interpretability**: Easy to understand and debug
- **Efficiency**: Fast training and prediction
- **Reliability**: Well-established algorithms with proven performance
- **Low Resource Requirements**: No GPU needed

For questions or improvements, refer to the main project documentation.
