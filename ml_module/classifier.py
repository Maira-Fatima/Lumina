"""
Classifier Module - Implements Naive Bayes for topic and difficulty classification

This module provides two main classifiers:
1. TopicClassifier: Classifies user queries into topics (AI, ML, DSA, etc.)
2. DifficultyClassifier: Predicts the difficulty level of questions
"""

import os
import pickle
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from core.nlp_utils import preprocess_text


class TopicClassifier:
    """
    Classifies user queries into predefined topics using Naive Bayes.
    
    Uses TF-IDF vectorization and Multinomial Naive Bayes for classification.
    Achieves high accuracy by preprocessing text and using a comprehensive training dataset.
    """
    
    def __init__(self, model_path='ml_module/models/topic_classifier.pkl'):
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        self.classifier = MultinomialNB(alpha=0.1)
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
        # Try to load pre-trained model
        if os.path.exists(model_path):
            self.load_model()
    
    def train(self, questions, topics):
        """
        Train the topic classifier on questions and their corresponding topics.
        
        Args:
            questions (list): List of question strings
            topics (list): List of topic labels corresponding to questions
        """
        # Preprocess questions
        processed_questions = [preprocess_text(q) for q in questions]
        
        # Encode labels
        encoded_topics = self.label_encoder.fit_transform(topics)
        
        # Vectorize questions
        X = self.vectorizer.fit_transform(processed_questions)
        
        # Train classifier
        self.classifier.fit(X, encoded_topics)
        self.is_trained = True
        
        print(f"✓ Topic Classifier trained on {len(questions)} samples")
        print(f"✓ Topics: {list(self.label_encoder.classes_)}")
    
    def predict(self, question):
        """
        Predict the topic of a given question.
        
        Args:
            question (str): User question
            
        Returns:
            tuple: (predicted_topic, confidence_score)
        """
        if not self.is_trained:
            return "General", 0.5
        
        # Preprocess and vectorize
        processed = preprocess_text(question)
        X = self.vectorizer.transform([processed])
        
        # Predict
        prediction = self.classifier.predict(X)[0]
        probabilities = self.classifier.predict_proba(X)[0]
        confidence = max(probabilities)
        
        topic = self.label_encoder.inverse_transform([prediction])[0]
        
        return topic, confidence
    
    def predict_top_k(self, question, k=3):
        """
        Predict top K most likely topics for a question.
        
        Args:
            question (str): User question
            k (int): Number of top predictions to return
            
        Returns:
            list: List of tuples (topic, confidence)
        """
        if not self.is_trained:
            return [("General", 0.5)]
        
        processed = preprocess_text(question)
        X = self.vectorizer.transform([processed])
        
        probabilities = self.classifier.predict_proba(X)[0]
        top_k_indices = np.argsort(probabilities)[-k:][::-1]
        
        results = []
        for idx in top_k_indices:
            topic = self.label_encoder.inverse_transform([idx])[0]
            confidence = probabilities[idx]
            results.append((topic, confidence))
        
        return results
    
    def save_model(self):
        """Save the trained model to disk."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'label_encoder': self.label_encoder,
            'is_trained': self.is_trained
        }
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✓ Model saved to {self.model_path}")
    
    def load_model(self):
        """Load a pre-trained model from disk."""
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.classifier = model_data['classifier']
            self.label_encoder = model_data['label_encoder']
            self.is_trained = model_data['is_trained']
            
            print(f"✓ Model loaded from {self.model_path}")
        except Exception as e:
            print(f"⚠ Could not load model: {e}")
            self.is_trained = False


class DifficultyClassifier:
    """
    Classifies questions into difficulty levels: Beginner, Intermediate, Advanced, Expert.
    
    Uses similar approach to TopicClassifier but focuses on difficulty prediction.
    """
    
    def __init__(self, model_path='ml_module/models/difficulty_classifier.pkl'):
        self.model_path = model_path
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        self.classifier = MultinomialNB(alpha=0.1)
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
        # Try to load pre-trained model
        if os.path.exists(model_path):
            self.load_model()
    
    def train(self, questions, difficulties):
        """
        Train the difficulty classifier.
        
        Args:
            questions (list): List of question strings
            difficulties (list): List of difficulty labels (Beginner, Intermediate, Advanced, Expert)
        """
        # Preprocess questions
        processed_questions = [preprocess_text(q) for q in questions]
        
        # Encode labels
        encoded_difficulties = self.label_encoder.fit_transform(difficulties)
        
        # Vectorize questions
        X = self.vectorizer.fit_transform(processed_questions)
        
        # Train classifier
        self.classifier.fit(X, encoded_difficulties)
        self.is_trained = True
        
        print(f"✓ Difficulty Classifier trained on {len(questions)} samples")
        print(f"✓ Difficulty levels: {list(self.label_encoder.classes_)}")
    
    def predict(self, question):
        """
        Predict the difficulty level of a question.
        
        Args:
            question (str): Question text
            
        Returns:
            tuple: (predicted_difficulty, confidence_score)
        """
        if not self.is_trained:
            return "Beginner", 0.5
        
        # Preprocess and vectorize
        processed = preprocess_text(question)
        X = self.vectorizer.transform([processed])
        
        # Predict
        prediction = self.classifier.predict(X)[0]
        probabilities = self.classifier.predict_proba(X)[0]
        confidence = max(probabilities)
        
        difficulty = self.label_encoder.inverse_transform([prediction])[0]
        
        return difficulty, confidence
    
    def get_difficulty_score(self, difficulty):
        """
        Convert difficulty level to numeric score.
        
        Args:
            difficulty (str): Difficulty level
            
        Returns:
            int: Numeric score (1-4)
        """
        difficulty_map = {
            'Beginner': 1,
            'Intermediate': 2,
            'Advanced': 3,
            'Expert': 4
        }
        return difficulty_map.get(difficulty, 1)
    
    def save_model(self):
        """Save the trained model to disk."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'label_encoder': self.label_encoder,
            'is_trained': self.is_trained
        }
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✓ Model saved to {self.model_path}")
    
    def load_model(self):
        """Load a pre-trained model from disk."""
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.classifier = model_data['classifier']
            self.label_encoder = model_data['label_encoder']
            self.is_trained = model_data['is_trained']
            
            print(f"✓ Model loaded from {self.model_path}")
        except Exception as e:
            print(f"⚠ Could not load model: {e}")
            self.is_trained = False
