"""
Machine Learning Module for Lumina AI Study Companion

This module provides machine learning capabilities including:
- Topic classification using Naive Bayes
- Difficulty level prediction
- Performance trend analysis using Linear Regression
- Automated training data generation
"""

from .classifier import TopicClassifier, DifficultyClassifier
from .predictor import PerformancePredictor
from .data_generator import DataGenerator
from .model_trainer import ModelTrainer

__all__ = [
    'TopicClassifier',
    'DifficultyClassifier',
    'PerformancePredictor',
    'DataGenerator',
    'ModelTrainer'
]
