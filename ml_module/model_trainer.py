"""
Model Trainer Module - Trains and evaluates all ML models

This module provides a unified interface for training:
- Topic Classifier
- Difficulty Classifier  
- Performance Predictor

Implements complete training pipeline with evaluation metrics.
"""

import os
import pickle
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from .classifier import TopicClassifier, DifficultyClassifier
from .predictor import PerformancePredictor
from .data_generator import DataGenerator


class ModelTrainer:
    """
    Unified trainer for all ML models in the system.
    
    Handles:
    - Data loading and preparation
    - Model training with cross-validation
    - Performance evaluation
    - Model persistence
    """
    
    def __init__(self, knowledge_base):
        """
        Initialize the model trainer.
        
        Args:
            knowledge_base (list): Expanded knowledge base
        """
        self.knowledge_base = knowledge_base
        self.data_generator = DataGenerator(knowledge_base)
        
        self.topic_classifier = TopicClassifier()
        self.difficulty_classifier = DifficultyClassifier()
        self.performance_predictor = PerformancePredictor()
    
    def train_all_models(self, regenerate_data=False):
        """
        Train all ML models in the system.
        
        Args:
            regenerate_data (bool): Whether to regenerate training data
        """
        print("\n" + "="*60)
        print("Starting ML Model Training Pipeline")
        print("="*60 + "\n")
        
        # Generate or load data
        if regenerate_data or not self._check_data_exists():
            print("Step 1: Generating training datasets...")
            train_df, val_df, test_df = self.data_generator.save_datasets()
        else:
            print("Step 1: Loading existing datasets...")
            train_df, val_df, test_df = self._load_datasets()
        
        print("\nStep 2: Training Topic Classifier...")
        self._train_topic_classifier(train_df, test_df)
        
        print("\nStep 3: Training Difficulty Classifier...")
        self._train_difficulty_classifier(train_df, test_df)
        
        print("\nStep 4: Training Performance Predictor...")
        self._train_performance_predictor()
        
        print("\n" + "="*60)
        print("✓ All models trained successfully!")
        print("="*60 + "\n")
    
    def _check_data_exists(self):
        """Check if training data files exist."""
        data_dir = 'ml_module/data'
        required_files = [
            'training_data.csv',
            'validation_data.csv',
            'test_data.csv',
            'predictor_training_data.pkl'
        ]
        
        for filename in required_files:
            if not os.path.exists(os.path.join(data_dir, filename)):
                return False
        
        return True
    
    def _load_datasets(self):
        """Load existing datasets from disk."""
        import pandas as pd
        
        data_dir = 'ml_module/data'
        
        train_df = pd.read_csv(f'{data_dir}/training_data.csv')
        val_df = pd.read_csv(f'{data_dir}/validation_data.csv')
        test_df = pd.read_csv(f'{data_dir}/test_data.csv')
        
        print(f"✓ Loaded datasets from {data_dir}")
        
        return train_df, val_df, test_df
    
    def _train_topic_classifier(self, train_df, test_df):
        """Train and evaluate the topic classifier."""
        # Prepare training data
        questions = train_df['question'].tolist()
        topics = train_df['topic'].tolist()
        
        # Train
        self.topic_classifier.train(questions, topics)
        
        # Evaluate on test set
        test_questions = test_df['question'].tolist()
        test_topics = test_df['topic'].tolist()
        
        predictions = []
        for question in test_questions:
            pred_topic, confidence = self.topic_classifier.predict(question)
            predictions.append(pred_topic)
        
        accuracy = accuracy_score(test_topics, predictions)
        
        print(f"\n📊 Topic Classifier Performance:")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"\n   Classification Report:")
        print(classification_report(test_topics, predictions, zero_division=0))
        
        # Save model
        self.topic_classifier.save_model()
    
    def _train_difficulty_classifier(self, train_df, test_df):
        """Train and evaluate the difficulty classifier."""
        # Prepare training data
        questions = train_df['question'].tolist()
        difficulties = train_df['difficulty'].tolist()
        
        # Train
        self.difficulty_classifier.train(questions, difficulties)
        
        # Evaluate on test set
        test_questions = test_df['question'].tolist()
        test_difficulties = test_df['difficulty'].tolist()
        
        predictions = []
        for question in test_questions:
            pred_difficulty, confidence = self.difficulty_classifier.predict(question)
            predictions.append(pred_difficulty)
        
        accuracy = accuracy_score(test_difficulties, predictions)
        
        print(f"\n📊 Difficulty Classifier Performance:")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"\n   Classification Report:")
        print(classification_report(test_difficulties, predictions, zero_division=0))
        
        # Save model
        self.difficulty_classifier.save_model()
    
    def _train_performance_predictor(self):
        """Train and evaluate the performance predictor."""
        # Load predictor training data
        data_path = 'ml_module/data/predictor_training_data.pkl'
        
        if not os.path.exists(data_path):
            print("⚠ Generating predictor training data...")
            training_data = self.data_generator.generate_predictor_training_data(num_samples=200)
            
            os.makedirs('ml_module/data', exist_ok=True)
            with open(data_path, 'wb') as f:
                pickle.dump(training_data, f)
        else:
            with open(data_path, 'rb') as f:
                training_data = pickle.load(f)
        
        # Split into train and test
        split_point = int(len(training_data) * 0.85)
        train_data = training_data[:split_point]
        test_data = training_data[split_point:]
        
        # Train
        self.performance_predictor.train(train_data)
        
        # Evaluate
        predictions = []
        actuals = []
        
        for sample in test_data:
            pred = self.performance_predictor.predict_future_performance(sample['history'])
            predictions.append(pred)
            actuals.append(sample['future_success_rate'])
        
        # Calculate metrics
        import numpy as np
        mse = np.mean([(p - a) ** 2 for p, a in zip(predictions, actuals)])
        mae = np.mean([abs(p - a) for p, a in zip(predictions, actuals)])
        
        print(f"\n📊 Performance Predictor Metrics:")
        print(f"   Mean Squared Error: {mse:.4f}")
        print(f"   Mean Absolute Error: {mae:.4f}")
        
        # Save model
        self.performance_predictor.save_model()
    
    def evaluate_models(self):
        """
        Comprehensive evaluation of all trained models.
        
        Returns:
            dict: Evaluation metrics for all models
        """
        if not self._check_data_exists():
            print("⚠ Training data not found. Please train models first.")
            return None
        
        print("\n" + "="*60)
        print("Model Evaluation Report")
        print("="*60 + "\n")
        
        # Load test data
        _, _, test_df = self._load_datasets()
        
        # Evaluate topic classifier
        test_questions = test_df['question'].tolist()
        test_topics = test_df['topic'].tolist()
        
        topic_predictions = [
            self.topic_classifier.predict(q)[0] for q in test_questions
        ]
        
        topic_accuracy = accuracy_score(test_topics, topic_predictions)
        
        print(f"✓ Topic Classifier Accuracy: {topic_accuracy:.4f}")
        
        # Evaluate difficulty classifier
        test_difficulties = test_df['difficulty'].tolist()
        
        difficulty_predictions = [
            self.difficulty_classifier.predict(q)[0] for q in test_questions
        ]
        
        difficulty_accuracy = accuracy_score(test_difficulties, difficulty_predictions)
        
        print(f"✓ Difficulty Classifier Accuracy: {difficulty_accuracy:.4f}")
        
        print("\n" + "="*60 + "\n")
        
        return {
            'topic_accuracy': topic_accuracy,
            'difficulty_accuracy': difficulty_accuracy
        }


def quick_train():
    """
    Quick training function for testing.
    Loads knowledge base and trains all models.
    """
    print("Loading knowledge base...")
    from core.data_loader import get_expanded_knowledge_base
    
    knowledge_base = get_expanded_knowledge_base()
    
    print(f"✓ Loaded {len(knowledge_base)} knowledge entries\n")
    
    trainer = ModelTrainer(knowledge_base)
    trainer.train_all_models(regenerate_data=True)
    
    # Evaluate
    trainer.evaluate_models()


if __name__ == "__main__":
    quick_train()
