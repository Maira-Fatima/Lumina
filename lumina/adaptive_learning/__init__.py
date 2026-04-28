"""
Adaptive Learning Module for Lumina AI Study Companion

This module provides adaptive learning capabilities:
- Central state management for all modules
- Dynamic difficulty adjustment
- Intelligent recommendation engine
- Performance tracking with time-series data
- Quiz generation and management
"""

from .state_manager import StateManager
from .difficulty_manager import DifficultyManager
from .recommendation_engine import RecommendationEngine
from .performance_tracker import PerformanceTracker
from .quiz_manager import QuizManager

__all__ = [
    'StateManager',
    'DifficultyManager',
    'RecommendationEngine',
    'PerformanceTracker',
    'QuizManager'
]
