"""
Difficulty Manager Module - Adaptive difficulty adjustment

Adjusts question difficulty based on:
- Performance in current topic (after 3 questions)
- Success rate threshold (>80% → increase, <50% → decrease)
- Learning trajectory
"""

from typing import Dict, Tuple
from .state_manager import StateManager


class DifficultyManager:
    """
    Manages adaptive difficulty adjustment for questions.
    
    Rules:
    - After every 3 questions in same topic, consider adjustment
    - Success rate > 80% → increase difficulty
    - Success rate < 50% → decrease difficulty
    - 50-80% → maintain current level
    """
    
    DIFFICULTY_ORDER = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
    QUESTIONS_BEFORE_ADJUSTMENT = 3
    INCREASE_THRESHOLD = 80.0  # 80% success rate
    DECREASE_THRESHOLD = 50.0  # 50% success rate
    
    def __init__(self, state_manager: StateManager = None):
        """
        Initialize difficulty manager.
        
        Args:
            state_manager (StateManager): State manager instance
        """
        self.state = state_manager or StateManager()
    
    def should_adjust_difficulty(self, topic: str = None) -> bool:
        """
        Check if difficulty should be adjusted for current topic.
        
        Args:
            topic (str): Topic to check (None = current topic)
            
        Returns:
            bool: True if adjustment should occur
        """
        question_count = self.state.get_topic_question_count(topic)
        return question_count >= self.QUESTIONS_BEFORE_ADJUSTMENT
    
    def calculate_difficulty_adjustment(
        self,
        topic: str = None
    ) -> Tuple[str, str, str]:
        """
        Calculate recommended difficulty adjustment.
        
        Args:
            topic (str): Topic to adjust
            
        Returns:
            tuple: (action, new_difficulty, reason)
                action: 'increase', 'decrease', 'maintain'
                new_difficulty: Recommended difficulty level
                reason: Explanation for adjustment
        """
        if topic is None:
            topic = self.state.get_current_topic()
        
        current_difficulty = self.state.get_topic_difficulty(topic)
        accuracy = self.state.get_topic_accuracy(topic)
        
        # Determine action
        if accuracy >= self.INCREASE_THRESHOLD:
            action = 'increase'
            new_difficulty = self._increase_difficulty(current_difficulty)
            reason = f"Great job! {accuracy:.1f}% accuracy - advancing to {new_difficulty}"
        
        elif accuracy < self.DECREASE_THRESHOLD:
            action = 'decrease'
            new_difficulty = self._decrease_difficulty(current_difficulty)
            reason = f"Let's practice more at {new_difficulty} level ({accuracy:.1f}% accuracy)"
        
        else:
            action = 'maintain'
            new_difficulty = current_difficulty
            reason = f"Good progress! Continuing at {current_difficulty} level"
        
        return action, new_difficulty, reason
    
    def apply_difficulty_adjustment(self, topic: str = None) -> Dict:
        """
        Apply difficulty adjustment for a topic.
        
        Args:
            topic (str): Topic to adjust
            
        Returns:
            dict: Adjustment result
        """
        if topic is None:
            topic = self.state.get_current_topic()
        
        action, new_difficulty, reason = self.calculate_difficulty_adjustment(topic)
        
        if action != 'maintain':
            # Update difficulty
            self.state.set_topic_difficulty(topic, new_difficulty)
            self.state.set_current_difficulty(new_difficulty)
        
        # Reset counters for this topic
        self.state.reset_topic_session(topic)
        
        return {
            'action': action,
            'previous_difficulty': self.state.get_topic_difficulty(topic),
            'new_difficulty': new_difficulty,
            'reason': reason,
            'accuracy': self.state.get_topic_accuracy(topic)
        }
    
    def _increase_difficulty(self, current: str) -> str:
        """Increase difficulty by one level."""
        try:
            current_index = self.DIFFICULTY_ORDER.index(current)
            next_index = min(current_index + 1, len(self.DIFFICULTY_ORDER) - 1)
            return self.DIFFICULTY_ORDER[next_index]
        except ValueError:
            return 'Intermediate'
    
    def _decrease_difficulty(self, current: str) -> str:
        """Decrease difficulty by one level."""
        try:
            current_index = self.DIFFICULTY_ORDER.index(current)
            prev_index = max(current_index - 1, 0)
            return self.DIFFICULTY_ORDER[prev_index]
        except ValueError:
            return 'Beginner'
    
    def get_appropriate_difficulty(self, topic: str) -> str:
        """
        Get appropriate difficulty for a topic based on history.
        
        Args:
            topic (str): Topic name
            
        Returns:
            str: Recommended difficulty level
        """
        stats = self.state.get_topic_stats(topic)
        
        if stats['attempts'] == 0:
            return 'Beginner'
        
        success_rate = stats['success_rate']
        mastery = stats['mastery_level']
        
        # Determine difficulty based on mastery and performance
        if mastery == 'Mastered':
            return 'Expert'
        elif mastery == 'Proficient':
            return 'Advanced'
        elif mastery == 'Learning':
            if success_rate >= 70:
                return 'Intermediate'
            else:
                return 'Beginner'
        else:
            return 'Beginner'
    
    def get_difficulty_distribution(self) -> Dict[str, int]:
        """Get distribution of topics across difficulty levels."""
        distribution = {level: 0 for level in self.DIFFICULTY_ORDER}
        
        for difficulty in self.state.get_all_difficulty_levels().values():
            if difficulty in distribution:
                distribution[difficulty] += 1
        
        return distribution
