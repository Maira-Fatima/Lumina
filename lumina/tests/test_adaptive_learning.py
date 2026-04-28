"""
Test Suite for Adaptive Learning Module

Tests cover:
- State Manager
- Difficulty Manager
- Recommendation Engine
- Performance Tracker
- Quiz Manager
"""

import pytest
import time
from datetime import datetime, timedelta
from adaptive_learning.state_manager import StateManager
from adaptive_learning.difficulty_manager import DifficultyManager
from adaptive_learning.recommendation_engine import RecommendationEngine
from adaptive_learning.performance_tracker import PerformanceTracker
from adaptive_learning.quiz_manager import QuizManager


class TestStateManager:
    """Tests for StateManager (Singleton)"""
    
    def test_singleton_pattern(self):
        """Test that only one instance exists"""
        state1 = StateManager()
        state2 = StateManager()
        assert state1 is state2
    
    def test_load_user(self):
        """Test user loading"""
        state = StateManager()
        state.load_user("test_user_123")
        assert state.user_profile['username'] == "test_user_123"
    
    def test_topic_mastery(self):
        """Test topic mastery management"""
        state = StateManager()
        state.load_user("test_user")
        
        state.set_topic_mastery("Python", 85)
        assert state.get_topic_mastery("Python") == 85
        
        # Test default value
        assert state.get_topic_mastery("NonExistent") == 0
    
    def test_topic_difficulty(self):
        """Test difficulty level management"""
        state = StateManager()
        state.load_user("test_user")
        
        state.set_topic_difficulty("Python", "Advanced")
        assert state.get_topic_difficulty("Python") == "Advanced"
        
        # Test default
        assert state.get_topic_difficulty("NonExistent") == "Intermediate"
    
    def test_record_performance(self):
        """Test performance recording"""
        state = StateManager()
        state.load_user("test_user")
        
        state.record_performance(
            topic="Python",
            difficulty="Intermediate",
            correct=True,
            time_taken=30.5,
            question="What is a list?"
        )
        
        # Check that it was recorded (would need to query database)
        history = state.get_performance_history(topic="Python", days=1)
        assert len(history) > 0
    
    def test_session_counters(self):
        """Test session counter management"""
        state = StateManager()
        state.load_user("test_user")
        
        state.increment_topic_questions("Python")
        state.increment_topic_questions("Python")
        state.increment_topic_correct("Python")
        
        assert state.get_topic_questions_since_adjustment("Python") == 2
        
        state.reset_topic_counters("Python")
        assert state.get_topic_questions_since_adjustment("Python") == 0
    
    def test_topic_stats(self):
        """Test topic statistics retrieval"""
        state = StateManager()
        state.load_user("test_user")
        
        # Record some performance
        for i in range(5):
            state.record_performance("Python", "Beginner", i % 2 == 0, 30.0, "Q")
        
        stats = state.get_topic_stats("Python")
        assert 'total_questions' in stats
        assert 'success_rate' in stats


class TestDifficultyManager:
    """Tests for DifficultyManager"""
    
    def test_initialization(self):
        """Test difficulty manager initialization"""
        state = StateManager()
        state.load_user("test_user")
        manager = DifficultyManager(state)
        assert manager.state is not None
    
    def test_should_adjust_check(self):
        """Test adjustment threshold check"""
        state = StateManager()
        state.load_user("test_user")
        manager = DifficultyManager(state)
        
        # Not enough questions
        assert manager.should_adjust_difficulty("Python") == False
        
        # Add 3 questions
        for _ in range(3):
            state.increment_topic_questions("Python")
        
        assert manager.should_adjust_difficulty("Python") == True
    
    def test_calculate_difficulty_increase(self):
        """Test difficulty increase calculation"""
        state = StateManager()
        state.load_user("test_user")
        manager = DifficultyManager(state)
        
        state.set_topic_difficulty("Python", "Beginner")
        
        # Simulate high success rate
        for i in range(3):
            state.record_performance("Python", "Beginner", True, 30.0, "Q")
            state.increment_topic_questions("Python")
            state.increment_topic_correct("Python")
        
        action, new_diff, reason = manager.calculate_difficulty_adjustment("Python")
        
        assert action == "increase"
        assert new_diff == "Intermediate"
        assert "increasing difficulty" in reason.lower()
    
    def test_calculate_difficulty_decrease(self):
        """Test difficulty decrease calculation"""
        state = StateManager()
        state.load_user("test_user")
        manager = DifficultyManager(state)
        
        state.set_topic_difficulty("Python", "Advanced")
        
        # Simulate low success rate
        for i in range(3):
            state.record_performance("Python", "Advanced", False, 30.0, "Q")
            state.increment_topic_questions("Python")
        
        action, new_diff, reason = manager.calculate_difficulty_adjustment("Python")
        
        assert action == "decrease"
        assert new_diff == "Intermediate"
    
    def test_apply_difficulty_adjustment(self):
        """Test applying difficulty adjustment"""
        state = StateManager()
        state.load_user("test_user")
        manager = DifficultyManager(state)
        
        state.set_topic_difficulty("Python", "Beginner")
        manager.apply_difficulty_adjustment("Python", "increase", "Intermediate")
        
        assert state.get_topic_difficulty("Python") == "Intermediate"
        assert state.get_topic_questions_since_adjustment("Python") == 0
    
    def test_boundary_conditions(self):
        """Test difficulty boundaries"""
        state = StateManager()
        state.load_user("test_user")
        manager = DifficultyManager(state)
        
        # Test can't go below Beginner
        state.set_topic_difficulty("Python", "Beginner")
        new_diff = manager._decrease_difficulty("Python")
        assert new_diff == "Beginner"
        
        # Test can't go above Expert
        state.set_topic_difficulty("Python", "Expert")
        new_diff = manager._increase_difficulty("Python")
        assert new_diff == "Expert"


class TestPerformanceTracker:
    """Tests for PerformanceTracker"""
    
    def test_initialization(self):
        """Test tracker initialization"""
        state = StateManager()
        state.load_user("test_user")
        tracker = PerformanceTracker(state)
        assert tracker.state is not None
    
    def test_calculate_success_rate(self):
        """Test success rate calculation"""
        state = StateManager()
        state.load_user("test_user")
        tracker = PerformanceTracker(state)
        
        # Record mixed performance
        for i in range(10):
            state.record_performance("Python", "Beginner", i < 7, 30.0, "Q")
        
        success_rate = tracker.calculate_success_rate("Python", days=7)
        assert 65.0 <= success_rate <= 75.0  # Should be around 70%
    
    def test_get_performance_trend(self):
        """Test trend analysis"""
        state = StateManager()
        state.load_user("test_user")
        tracker = PerformanceTracker(state)
        
        # Record some performance
        for i in range(5):
            state.record_performance("Python", "Beginner", True, 30.0, "Q")
        
        trend = tracker.get_performance_trend("Python", days=7)
        
        assert 'trend' in trend
        assert trend['trend'] in ['improving', 'declining', 'stable']
    
    def test_get_learning_summary(self):
        """Test learning summary generation"""
        state = StateManager()
        state.load_user("test_user")
        tracker = PerformanceTracker(state)
        
        # Record performance across multiple topics
        for topic in ["Python", "Java", "ML"]:
            for i in range(5):
                state.record_performance(topic, "Beginner", i % 2 == 0, 30.0, "Q")
        
        summary = tracker.get_learning_summary(days=30)
        
        assert 'total_questions' in summary
        assert 'overall_success_rate' in summary
        assert 'topics_studied' in summary


class TestRecommendationEngine:
    """Tests for RecommendationEngine"""
    
    def test_initialization(self):
        """Test recommendation engine initialization"""
        state = StateManager()
        state.load_user("test_user")
        engine = RecommendationEngine(state)
        assert engine.state is not None
    
    def test_get_recommendations(self):
        """Test recommendation generation"""
        state = StateManager()
        state.load_user("test_user")
        engine = RecommendationEngine(state)
        
        # Set some mastery levels
        state.set_topic_mastery("Python", 85)
        
        recommendations = engine.get_recommendations(
            current_topic="Python",
            recent_performance=[]
        )
        
        assert isinstance(recommendations, dict)
        # Note: Actual recommendations depend on loaded modules
    
    def test_suggest_next_topic(self):
        """Test next topic suggestion"""
        state = StateManager()
        state.load_user("test_user")
        engine = RecommendationEngine(state)
        
        state.set_topic_mastery("Python", 90)
        
        next_topic = engine.suggest_next_topic("Python")
        assert isinstance(next_topic, (str, type(None)))


class TestQuizManager:
    """Tests for QuizManager"""
    
    def test_initialization(self):
        """Test quiz manager initialization"""
        state = StateManager()
        state.load_user("test_user")
        manager = QuizManager(state)
        assert manager.state is not None
    
    def test_create_quiz(self):
        """Test quiz creation"""
        state = StateManager()
        state.load_user("test_user")
        manager = QuizManager(state)
        
        quiz_id = manager.create_quiz(
            topic="Python",
            difficulty="Beginner",
            num_questions=5,
            time_limit=300,
            mix_difficulties=False
        )
        
        assert quiz_id in manager.active_quizzes
        quiz = manager.active_quizzes[quiz_id]
        assert len(quiz['questions']) == 5
    
    def test_start_quiz(self):
        """Test quiz start"""
        state = StateManager()
        state.load_user("test_user")
        manager = QuizManager(state)
        
        quiz_id = manager.create_quiz("Python", "Beginner", 5)
        manager.start_quiz(quiz_id)
        
        quiz = manager.active_quizzes[quiz_id]
        assert 'start_time' in quiz
    
    def test_submit_answer(self):
        """Test answer submission"""
        state = StateManager()
        state.load_user("test_user")
        manager = QuizManager(state)
        
        quiz_id = manager.create_quiz("Python", "Beginner", 5)
        manager.start_quiz(quiz_id)
        
        manager.submit_answer(quiz_id, 0, "Answer", "Answer", True)
        
        quiz = manager.active_quizzes[quiz_id]
        assert len(quiz['user_answers']) == 1
    
    def test_complete_quiz(self):
        """Test quiz completion"""
        state = StateManager()
        state.load_user("test_user")
        manager = QuizManager(state)
        
        quiz_id = manager.create_quiz("Python", "Beginner", 5)
        manager.start_quiz(quiz_id)
        
        # Submit all answers
        for i in range(5):
            manager.submit_answer(quiz_id, i, "Answer", "Answer", i < 4)  # 4 correct
        
        results = manager.complete_quiz(quiz_id)
        
        assert results['score'] == 4
        assert results['total_questions'] == 5
        assert results['score_percentage'] == 80.0
        assert results['grade'] == 'B'
    
    def test_quiz_grading(self):
        """Test grading system"""
        state = StateManager()
        state.load_user("test_user")
        manager = QuizManager(state)
        
        assert manager._calculate_grade(95.0) == 'A'
        assert manager._calculate_grade(85.0) == 'B'
        assert manager._calculate_grade(75.0) == 'C'
        assert manager._calculate_grade(65.0) == 'D'
        assert manager._calculate_grade(55.0) == 'F'


@pytest.fixture
def setup_adaptive_learning_system():
    """Fixture for complete adaptive learning system"""
    state = StateManager()
    state.load_user("integration_test_user")
    
    diff_manager = DifficultyManager(state)
    rec_engine = RecommendationEngine(state)
    tracker = PerformanceTracker(state)
    quiz_manager = QuizManager(state)
    
    return state, diff_manager, rec_engine, tracker, quiz_manager


def test_end_to_end_adaptive_learning(setup_adaptive_learning_system):
    """Test complete adaptive learning workflow"""
    state, diff_manager, rec_engine, tracker, quiz_manager = setup_adaptive_learning_system
    
    # 1. Start with beginner difficulty
    state.set_topic_difficulty("Python", "Beginner")
    
    # 2. Record good performance
    for i in range(3):
        state.record_performance("Python", "Beginner", True, 25.0, f"Q{i}")
        state.increment_topic_questions("Python")
        state.increment_topic_correct("Python")
    
    # 3. Check if difficulty should adjust
    assert diff_manager.should_adjust_difficulty("Python") == True
    
    # 4. Calculate adjustment
    action, new_diff, reason = diff_manager.calculate_difficulty_adjustment("Python")
    assert action == "increase"
    
    # 5. Apply adjustment
    diff_manager.apply_difficulty_adjustment("Python", action, new_diff)
    assert state.get_topic_difficulty("Python") == new_diff
    
    # 6. Get performance stats
    success_rate = tracker.calculate_success_rate("Python", days=1)
    assert success_rate == 100.0
    
    # 7. Get recommendations
    recommendations = rec_engine.get_recommendations("Python", [])
    assert isinstance(recommendations, dict)


def test_quiz_lifecycle(setup_adaptive_learning_system):
    """Test complete quiz lifecycle"""
    state, _, _, _, quiz_manager = setup_adaptive_learning_system
    
    # 1. Create quiz
    quiz_id = quiz_manager.create_quiz(
        topic="Python",
        difficulty="Intermediate",
        num_questions=10,
        time_limit=600
    )
    
    # 2. Start quiz
    quiz_manager.start_quiz(quiz_id)
    
    # 3. Answer questions
    for i in range(10):
        is_correct = i < 8  # 80% correct
        quiz_manager.submit_answer(quiz_id, i, "Answer", "Answer", is_correct)
    
    # 4. Complete quiz
    results = quiz_manager.complete_quiz(quiz_id)
    
    # 5. Verify results
    assert results['score'] == 8
    assert results['score_percentage'] == 80.0
    assert results['grade'] == 'B'
    
    # 6. Check quiz summary
    summary = quiz_manager.get_quiz_summary(quiz_id)
    assert summary is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
