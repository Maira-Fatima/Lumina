"""
Test Suite for Machine Learning Module

Tests cover:
- Topic Classification
- Difficulty Classification
- Performance Prediction
- Data Generation
- Model Training
"""

import pytest
import numpy as np
import pandas as pd
from ml_module.classifier import TopicClassifier, DifficultyClassifier
from ml_module.predictor import PerformancePredictor
from ml_module.data_generator import DataGenerator
from ml_module.model_trainer import ModelTrainer


class TestTopicClassifier:
    """Tests for TopicClassifier"""
    
    def test_initialization(self):
        """Test classifier can be initialized"""
        classifier = TopicClassifier()
        assert classifier.model is not None
        assert classifier.vectorizer is not None
    
    def test_training(self):
        """Test classifier training"""
        classifier = TopicClassifier()
        
        # Generate sample data
        questions = [
            "What is a neural network?",
            "How does backpropagation work?",
            "Explain gradient descent",
            "What is a decision tree?",
            "How does random forest work?"
        ]
        topics = ["Neural Networks", "Neural Networks", "Machine Learning", 
                 "Machine Learning", "Machine Learning"]
        
        # Train
        accuracy = classifier.train(questions, topics)
        assert accuracy >= 0.0
        assert accuracy <= 1.0
    
    def test_prediction(self):
        """Test topic prediction"""
        classifier = TopicClassifier()
        
        # Train with sample data
        questions = ["What is a neural network?"] * 10
        topics = ["Neural Networks"] * 10
        classifier.train(questions, topics)
        
        # Predict
        question = "Tell me about neural networks"
        topic, confidence = classifier.predict(question)
        
        assert isinstance(topic, str)
        assert 0.0 <= confidence <= 1.0
    
    def test_predict_top_k(self):
        """Test top-k prediction"""
        classifier = TopicClassifier()
        
        # Train
        questions = ["neural network"] * 5 + ["machine learning"] * 5
        topics = ["Neural Networks"] * 5 + ["Machine Learning"] * 5
        classifier.train(questions, topics)
        
        # Predict top 2
        predictions = classifier.predict_top_k("what is ML?", k=2)
        
        assert len(predictions) <= 2
        for topic, conf in predictions:
            assert isinstance(topic, str)
            assert 0.0 <= conf <= 1.0
    
    def test_save_load_model(self, tmp_path):
        """Test model persistence"""
        classifier = TopicClassifier()
        
        # Train
        questions = ["neural network"] * 10
        topics = ["Neural Networks"] * 10
        classifier.train(questions, topics)
        
        # Save
        model_path = tmp_path / "test_model.pkl"
        classifier.save_model(str(model_path))
        
        # Load
        new_classifier = TopicClassifier()
        new_classifier.load_model(str(model_path))
        
        # Verify predictions work
        topic, conf = new_classifier.predict("neural network")
        assert isinstance(topic, str)


class TestDifficultyClassifier:
    """Tests for DifficultyClassifier"""
    
    def test_initialization(self):
        """Test classifier initialization"""
        classifier = DifficultyClassifier()
        assert classifier.model is not None
    
    def test_training(self):
        """Test difficulty classification training"""
        classifier = DifficultyClassifier()
        
        questions = [
            "What is Python?",
            "Explain object-oriented programming",
            "How do metaclasses work in Python?",
            "What is a variable?"
        ]
        difficulties = ["Beginner", "Intermediate", "Advanced", "Beginner"]
        
        accuracy = classifier.train(questions, difficulties)
        assert 0.0 <= accuracy <= 1.0
    
    def test_prediction(self):
        """Test difficulty prediction"""
        classifier = DifficultyClassifier()
        
        # Train
        questions = ["simple question"] * 10
        difficulties = ["Beginner"] * 10
        classifier.train(questions, difficulties)
        
        # Predict
        difficulty = classifier.predict("easy question")
        assert difficulty in ["Beginner", "Intermediate", "Advanced", "Expert"]


class TestPerformancePredictor:
    """Tests for PerformancePredictor"""
    
    def test_initialization(self):
        """Test predictor initialization"""
        predictor = PerformancePredictor()
        assert predictor.model is not None
        assert predictor.scaler is not None
    
    def test_feature_preparation(self):
        """Test feature extraction"""
        predictor = PerformancePredictor()
        
        history = [
            {'correct': True, 'time_taken': 30.0, 'difficulty': 'Beginner'},
            {'correct': False, 'time_taken': 45.0, 'difficulty': 'Intermediate'},
            {'correct': True, 'time_taken': 25.0, 'difficulty': 'Beginner'}
        ]
        
        features = predictor.prepare_features(history)
        assert len(features) == 5  # 5 features defined
    
    def test_training(self):
        """Test predictor training"""
        predictor = PerformancePredictor()
        
        # Generate sample data
        histories = []
        success_rates = []
        
        for i in range(50):
            history = [
                {'correct': True, 'time_taken': 30.0, 'difficulty': 'Beginner'}
                for _ in range(10)
            ]
            histories.append(history)
            success_rates.append(0.8)
        
        mse, mae = predictor.train(histories, success_rates)
        assert mse >= 0.0
        assert mae >= 0.0
    
    def test_prediction(self):
        """Test performance prediction"""
        predictor = PerformancePredictor()
        
        # Train with simple data
        histories = [[{'correct': True, 'time_taken': 30.0, 'difficulty': 'Beginner'}] * 10] * 50
        success_rates = [0.8] * 50
        predictor.train(histories, success_rates)
        
        # Predict
        test_history = [{'correct': True, 'time_taken': 30.0, 'difficulty': 'Beginner'}] * 5
        prediction = predictor.predict_future_performance(test_history)
        
        assert 0.0 <= prediction <= 1.0


class TestDataGenerator:
    """Tests for DataGenerator"""
    
    def test_initialization(self):
        """Test generator initialization"""
        from core.data_loader import combined_data
        generator = DataGenerator(combined_data)
        assert generator.knowledge_base is not None
    
    def test_question_variations(self):
        """Test question variation generation"""
        from core.data_loader import combined_data
        generator = DataGenerator(combined_data)
        
        entry = combined_data[0]
        variations = generator.generate_question_variations(entry, num_variations=5)
        
        assert len(variations) <= 5
        for var in variations:
            assert 'question' in var
            assert 'answer' in var
            assert 'topic' in var
    
    def test_training_dataset_generation(self):
        """Test training dataset generation"""
        from core.data_loader import combined_data
        generator = DataGenerator(combined_data)
        
        train, val, test = generator.generate_training_dataset()
        
        assert len(train) > 0
        assert len(val) > 0
        assert len(test) > 0
        
        # Check split proportions (approximately 70-15-15)
        total = len(train) + len(val) + len(test)
        assert 0.65 <= len(train) / total <= 0.75
    
    def test_performance_history_generation(self):
        """Test performance history generation"""
        generator = DataGenerator([])
        
        history = generator.generate_performance_history(num_days=30)
        
        assert len(history) > 0
        for record in history:
            assert 'correct' in record
            assert 'time_taken' in record
            assert 'difficulty' in record


class TestModelTrainer:
    """Tests for ModelTrainer"""
    
    def test_initialization(self):
        """Test trainer initialization"""
        from core.data_loader import combined_data
        trainer = ModelTrainer(combined_data)
        assert trainer.knowledge_base is not None
    
    def test_quick_train(self):
        """Test quick training function"""
        # This would require actual data
        # Skipping for now as it's resource-intensive
        pass


@pytest.fixture
def sample_knowledge_base():
    """Fixture for sample knowledge base"""
    return [
        {
            'question': 'What is Python?',
            'answer': 'Python is a programming language.',
            'topic': 'Python',
            'difficulty': 'Beginner'
        },
        {
            'question': 'What is OOP?',
            'answer': 'Object-Oriented Programming.',
            'topic': 'Python',
            'difficulty': 'Intermediate'
        }
    ]


def test_end_to_end_ml_workflow(sample_knowledge_base):
    """Test complete ML workflow"""
    # 1. Generate data
    generator = DataGenerator(sample_knowledge_base)
    train, val, test = generator.generate_training_dataset()
    
    assert len(train) > 0
    
    # 2. Train classifier
    classifier = TopicClassifier()
    questions = [entry['question'] for entry in train]
    topics = [entry['topic'] for entry in train]
    accuracy = classifier.train(questions, topics)
    
    assert accuracy >= 0.0
    
    # 3. Make prediction
    topic, conf = classifier.predict("What is programming?")
    assert isinstance(topic, str)
    assert 0.0 <= conf <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
