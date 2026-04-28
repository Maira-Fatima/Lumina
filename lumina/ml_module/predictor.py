"""
Performance Predictor Module - Uses Linear Regression for performance trend analysis

This module predicts student performance trends based on historical data:
- Success rate prediction
- Learning progress estimation
- Performance trend analysis
"""

import os
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime


class PerformancePredictor:
    """
    Predicts student performance trends using Linear Regression.
    
    Analyzes historical performance data to predict:
    - Future success rates
    - Learning trajectory
    - Time to mastery for topics
    """
    
    def __init__(self, model_path='ml_module/models/performance_predictor.pkl'):
        self.model_path = model_path
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Try to load pre-trained model
        if os.path.exists(model_path):
            self.load_model()
    
    def prepare_features(self, performance_history):
        """
        Prepare features from performance history for prediction.
        
        Args:
            performance_history (list): List of performance records
                Each record: {
                    'timestamp': datetime,
                    'topic': str,
                    'difficulty': str,
                    'correct': bool,
                    'time_taken': float
                }
        
        Returns:
            np.array: Feature matrix
        """
        if not performance_history:
            return np.array([[0, 0, 0, 0, 0]])
        
        # Extract features
        total_questions = len(performance_history)
        correct_answers = sum(1 for record in performance_history if record.get('correct', False))
        success_rate = correct_answers / total_questions if total_questions > 0 else 0
        
        # Calculate average time taken
        avg_time = np.mean([record.get('time_taken', 30) for record in performance_history])
        
        # Calculate difficulty distribution
        difficulty_scores = []
        difficulty_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Expert': 4}
        for record in performance_history:
            difficulty_scores.append(difficulty_map.get(record.get('difficulty', 'Beginner'), 1))
        avg_difficulty = np.mean(difficulty_scores) if difficulty_scores else 1
        
        # Recent performance (last 10 questions)
        recent_records = performance_history[-10:]
        recent_correct = sum(1 for record in recent_records if record.get('correct', False))
        recent_success_rate = recent_correct / len(recent_records) if recent_records else 0
        
        features = np.array([[
            total_questions,
            success_rate,
            avg_time,
            avg_difficulty,
            recent_success_rate
        ]])
        
        return features
    
    def train(self, training_data):
        """
        Train the performance predictor.
        
        Args:
            training_data (list): List of training samples
                Each sample: {
                    'history': list of performance records,
                    'future_success_rate': float (target)
                }
        """
        if not training_data:
            print("⚠ No training data provided")
            return
        
        X = []
        y = []
        
        for sample in training_data:
            features = self.prepare_features(sample['history'])
            X.append(features[0])
            y.append(sample['future_success_rate'])
        
        X = np.array(X)
        y = np.array(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        print(f"✓ Performance Predictor trained on {len(training_data)} samples")
        print(f"✓ Model R² score: {self.model.score(X_scaled, y):.4f}")
    
    def predict_future_performance(self, performance_history):
        """
        Predict future success rate based on historical performance.
        
        Args:
            performance_history (list): List of past performance records
            
        Returns:
            float: Predicted future success rate (0-1)
        """
        if not self.is_trained:
            # Return current success rate as baseline
            if not performance_history:
                return 0.5
            correct = sum(1 for r in performance_history if r.get('correct', False))
            return correct / len(performance_history)
        
        features = self.prepare_features(performance_history)
        features_scaled = self.scaler.transform(features)
        
        prediction = self.model.predict(features_scaled)[0]
        
        # Clip prediction to valid range [0, 1]
        return max(0.0, min(1.0, prediction))
    
    def analyze_trend(self, performance_history, window_size=10):
        """
        Analyze performance trend over time.
        
        Args:
            performance_history (list): List of performance records
            window_size (int): Size of sliding window for trend calculation
            
        Returns:
            dict: Trend analysis results
        """
        if len(performance_history) < 2:
            return {
                'trend': 'insufficient_data',
                'slope': 0,
                'recent_performance': 0,
                'improvement': 0
            }
        
        # Calculate success rates over time
        success_rates = []
        for i in range(0, len(performance_history), window_size):
            window = performance_history[i:i+window_size]
            if window:
                correct = sum(1 for r in window if r.get('correct', False))
                rate = correct / len(window)
                success_rates.append(rate)
        
        if len(success_rates) < 2:
            return {
                'trend': 'insufficient_data',
                'slope': 0,
                'recent_performance': success_rates[0] if success_rates else 0,
                'improvement': 0
            }
        
        # Calculate trend using linear regression
        X = np.arange(len(success_rates)).reshape(-1, 1)
        y = np.array(success_rates)
        
        trend_model = LinearRegression()
        trend_model.fit(X, y)
        
        slope = trend_model.coef_[0]
        
        # Determine trend direction
        if slope > 0.05:
            trend = 'improving'
        elif slope < -0.05:
            trend = 'declining'
        else:
            trend = 'stable'
        
        recent_performance = success_rates[-1]
        improvement = recent_performance - success_rates[0]
        
        return {
            'trend': trend,
            'slope': slope,
            'recent_performance': recent_performance,
            'improvement': improvement,
            'success_rates_over_time': success_rates
        }
    
    def calculate_simple_success_rate(self, performance_history):
        """
        Calculate simple success rate: (correct / total) × 100
        
        Args:
            performance_history (list): List of performance records
            
        Returns:
            float: Success rate percentage
        """
        if not performance_history:
            return 0.0
        
        correct = sum(1 for record in performance_history if record.get('correct', False))
        total = len(performance_history)
        
        return (correct / total) * 100
    
    def get_topic_performance(self, performance_history, topic):
        """
        Calculate performance metrics for a specific topic.
        
        Args:
            performance_history (list): List of performance records
            topic (str): Topic name
            
        Returns:
            dict: Topic-specific performance metrics
        """
        topic_records = [r for r in performance_history if r.get('topic', '') == topic]
        
        if not topic_records:
            return {
                'attempts': 0,
                'success_rate': 0,
                'avg_time': 0,
                'mastery_level': 'Not Started'
            }
        
        correct = sum(1 for r in topic_records if r.get('correct', False))
        success_rate = (correct / len(topic_records)) * 100
        avg_time = np.mean([r.get('time_taken', 30) for r in topic_records])
        
        # Determine mastery level
        if success_rate >= 90 and len(topic_records) >= 10:
            mastery_level = 'Mastered'
        elif success_rate >= 75 and len(topic_records) >= 5:
            mastery_level = 'Proficient'
        elif success_rate >= 50:
            mastery_level = 'Learning'
        else:
            mastery_level = 'Struggling'
        
        return {
            'attempts': len(topic_records),
            'success_rate': success_rate,
            'avg_time': avg_time,
            'mastery_level': mastery_level
        }
    
    def save_model(self):
        """Save the trained model to disk."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
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
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.is_trained = model_data['is_trained']
            
            print(f"✓ Model loaded from {self.model_path}")
        except Exception as e:
            print(f"⚠ Could not load model: {e}")
            self.is_trained = False
