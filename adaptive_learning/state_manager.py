"""
State Manager Module - Central state management for all modules

This is the central hub that coordinates between:
- ML Module
- Expert System
- Adaptive Learning components
- User interface

Provides shared state access and persistence.
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict


class StateManager:
    """
    Central state manager for the Lumina AI Study Companion.
    
    Coordinates state between all modules:
    - User profile and preferences
    - Learning progress and mastery levels
    - Performance history
    - Current session state
    - Difficulty levels per topic
    
    Uses:
    - JSON for user profile and session state
    - SQLite for performance metrics and history
    """
    
    _instance = None  # Singleton pattern
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the state manager (only once)."""
        if self._initialized:
            return
        
        self.data_dir = 'data'
        self.profile_file = os.path.join(self.data_dir, 'user_profile.json')
        self.db_file = os.path.join(self.data_dir, 'performance.db')
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize state dictionaries
        self.user_profile: Dict = {}
        self.session_state: Dict = {}
        self.topic_mastery: Dict[str, str] = {}  # topic -> mastery level
        self.difficulty_levels: Dict[str, str] = {}  # topic -> difficulty level
        self.topic_question_count: Dict[str, int] = defaultdict(int)  # Track questions per topic
        self.topic_correct_count: Dict[str, int] = defaultdict(int)  # Track correct answers
        
        # Load existing data
        self._load_user_profile()
        self._init_database()
        
        # Current session tracking
        self.current_topic = "General"
        self.current_difficulty = "Beginner"
        self.quiz_mode = False
        self.questions_in_current_topic = 0
        self.correct_in_current_topic = 0
        
        self._initialized = True
        print("✓ State Manager initialized")
    
    def _load_user_profile(self):
        """Load user profile from JSON."""
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r') as f:
                data = json.load(f)
                self.user_profile = data.get('profile', {})
                self.topic_mastery = data.get('topic_mastery', {})
                self.difficulty_levels = data.get('difficulty_levels', {})
            print("✓ User profile loaded")
        else:
            # Create default profile
            self.user_profile = {
                'created_at': datetime.now().isoformat(),
                'total_questions': 0,
                'total_correct': 0,
                'total_study_time': 0,
                'level': 'Beginner',
                'preferences': {
                    'auto_difficulty': True,
                    'show_explanations': True,
                    'practice_mode': 'mixed'
                }
            }
            self.topic_mastery = {}
            self.difficulty_levels = {}
            self._save_user_profile()
    
    def _save_user_profile(self):
        """Save user profile to JSON."""
        data = {
            'profile': self.user_profile,
            'topic_mastery': self.topic_mastery,
            'difficulty_levels': self.difficulty_levels,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.profile_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def save_user_profile(self):
        """Public method to save user profile."""
        self._save_user_profile()
    
    def _init_database(self):
        """Initialize SQLite database for performance tracking."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Performance history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                topic TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                question TEXT,
                correct INTEGER NOT NULL,
                time_taken REAL,
                confidence REAL
            )
        ''')
        
        # Topic statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topic_stats (
                topic TEXT PRIMARY KEY,
                total_attempts INTEGER DEFAULT 0,
                total_correct INTEGER DEFAULT 0,
                avg_time REAL DEFAULT 0,
                last_practiced TEXT,
                mastery_level TEXT DEFAULT 'Not Started'
            )
        ''')
        
        # Session history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                start_time TEXT NOT NULL,
                end_time TEXT,
                total_questions INTEGER DEFAULT 0,
                total_correct INTEGER DEFAULT 0,
                topics_covered TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✓ Database initialized")
    
    # ==================== User Profile Methods ====================
    
    def load_user(self, user_id: str) -> bool:
        """
        Load user profile by user ID.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            bool: True if user loaded successfully, False otherwise
        """
        # For now, use the default profile system
        # In a multi-user system, this would load user-specific data
        self.user_profile['user_id'] = user_id
        return True
    
    def get_user_profile(self) -> Dict:
        """Get complete user profile."""
        return self.user_profile.copy()
    
    def update_profile(self, key: str, value: Any):
        """Update a user profile field."""
        self.user_profile[key] = value
        self._save_user_profile()
    
    def get_preference(self, key: str, default=None) -> Any:
        """Get a user preference."""
        return self.user_profile.get('preferences', {}).get(key, default)
    
    def set_preference(self, key: str, value: Any):
        """Set a user preference."""
        if 'preferences' not in self.user_profile:
            self.user_profile['preferences'] = {}
        self.user_profile['preferences'][key] = value
        self._save_user_profile()
    
    # ==================== Topic Mastery Methods ====================
    
    def set_topic_mastery(self, topic: str, level: str):
        """
        Set mastery level for a topic.
        
        Args:
            topic (str): Topic name
            level (str): Mastery level (Not Started/Learning/Proficient/Mastered)
        """
        self.topic_mastery[topic] = level
        self._save_user_profile()
        
        # Also update in database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO topic_stats (topic, mastery_level, last_practiced)
            VALUES (?, ?, ?)
        ''', (topic, level, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_topic_mastery(self, topic: str) -> str:
        """Get mastery level for a topic."""
        return self.topic_mastery.get(topic, 'Not Started')
    
    def get_all_mastery_levels(self) -> Dict[str, str]:
        """Get mastery levels for all topics."""
        return self.topic_mastery.copy()
    
    def get_mastered_topics(self) -> List[str]:
        """Get list of mastered topics."""
        return [topic for topic, level in self.topic_mastery.items() if level == 'Mastered']
    
    # ==================== Difficulty Management ====================
    
    def set_topic_difficulty(self, topic: str, difficulty: str):
        """Set current difficulty level for a topic."""
        self.difficulty_levels[topic] = difficulty
        self._save_user_profile()
    
    def get_topic_difficulty(self, topic: str) -> str:
        """Get current difficulty level for a topic."""
        return self.difficulty_levels.get(topic, 'Beginner')
    
    def get_all_difficulty_levels(self) -> Dict[str, str]:
        """Get difficulty levels for all topics."""
        return self.difficulty_levels.copy()
    
    # ==================== Session State Methods ====================
    
    def set_current_topic(self, topic: str):
        """Set the current active topic."""
        # If topic changes, reset question count for that topic
        if topic != self.current_topic:
            self.questions_in_current_topic = 0
            self.correct_in_current_topic = 0
        
        self.current_topic = topic
    
    def get_current_topic(self) -> str:
        """Get the current active topic."""
        return self.current_topic
    
    def set_current_difficulty(self, difficulty: str):
        """Set the current difficulty level."""
        self.current_difficulty = difficulty
    
    def get_current_difficulty(self) -> str:
        """Get the current difficulty level."""
        return self.current_difficulty
    
    def set_quiz_mode(self, active: bool):
        """Set whether quiz mode is active."""
        self.quiz_mode = active
    
    def is_quiz_mode(self) -> bool:
        """Check if quiz mode is active."""
        return self.quiz_mode
    
    def increment_topic_questions(self, topic: str = None):
        """Increment question count for a topic."""
        if topic is None:
            topic = self.current_topic
        
        self.topic_question_count[topic] += 1
        self.questions_in_current_topic += 1
    
    def increment_topic_correct(self, topic: str = None):
        """Increment correct answer count for a topic."""
        if topic is None:
            topic = self.current_topic
        
        self.topic_correct_count[topic] += 1
        self.correct_in_current_topic += 1
    
    def get_topic_question_count(self, topic: str = None) -> int:
        """Get number of questions answered in current topic session."""
        if topic is None:
            topic = self.current_topic
        return self.topic_question_count[topic]
    
    def get_topic_accuracy(self, topic: str = None) -> float:
        """Get accuracy for current topic session."""
        if topic is None:
            topic = self.current_topic
        
        total = self.topic_question_count[topic]
        if total == 0:
            return 0.0
        
        correct = self.topic_correct_count[topic]
        return (correct / total) * 100
    
    def reset_topic_session(self, topic: str = None):
        """Reset session counters for a topic."""
        if topic is None:
            topic = self.current_topic
        
        self.topic_question_count[topic] = 0
        self.topic_correct_count[topic] = 0
    
    # ==================== Performance Tracking ====================
    
    def record_performance(
        self,
        topic: str,
        difficulty: str,
        question: str,
        correct: bool,
        time_taken: float = 0.0,
        confidence: float = 0.0
    ):
        """
        Record a performance entry.
        
        Args:
            topic (str): Topic name
            difficulty (str): Difficulty level
            question (str): Question text
            correct (bool): Whether answer was correct
            time_taken (float): Time taken in seconds
            confidence (float): Confidence score (0-1)
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Insert performance record
        cursor.execute('''
            INSERT INTO performance_history
            (timestamp, topic, difficulty, question, correct, time_taken, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            topic,
            difficulty,
            question,
            1 if correct else 0,
            time_taken,
            confidence
        ))
        
        # Update topic statistics
        cursor.execute('''
            SELECT total_attempts, total_correct FROM topic_stats WHERE topic = ?
        ''', (topic,))
        
        row = cursor.fetchone()
        if row:
            total_attempts, total_correct = row
            total_attempts += 1
            total_correct += 1 if correct else 0
        else:
            total_attempts = 1
            total_correct = 1 if correct else 0
        
        cursor.execute('''
            INSERT OR REPLACE INTO topic_stats
            (topic, total_attempts, total_correct, last_practiced)
            VALUES (?, ?, ?, ?)
        ''', (topic, total_attempts, total_correct, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # Update profile stats
        self.user_profile['total_questions'] = self.user_profile.get('total_questions', 0) + 1
        if correct:
            self.user_profile['total_correct'] = self.user_profile.get('total_correct', 0) + 1
        self._save_user_profile()
    
    def get_performance_history(
        self,
        topic: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get performance history.
        
        Args:
            topic (str): Filter by topic (None = all topics)
            limit (int): Maximum records to return
            
        Returns:
            list: Performance records
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        if topic:
            cursor.execute('''
                SELECT timestamp, topic, difficulty, question, correct, time_taken, confidence
                FROM performance_history
                WHERE topic = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (topic, limit))
        else:
            cursor.execute('''
                SELECT timestamp, topic, difficulty, question, correct, time_taken, confidence
                FROM performance_history
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'timestamp': row[0],
                'topic': row[1],
                'difficulty': row[2],
                'question': row[3],
                'correct': bool(row[4]),
                'time_taken': row[5],
                'confidence': row[6]
            })
        
        return history
    
    def get_topic_stats(self, topic: str) -> Dict:
        """Get statistics for a topic."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT total_attempts, total_correct, avg_time, last_practiced, mastery_level
            FROM topic_stats
            WHERE topic = ?
        ''', (topic,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            success_rate = (row[1] / row[0] * 100) if row[0] > 0 else 0
            return {
                'topic': topic,
                'attempts': row[0],
                'correct': row[1],
                'success_rate': success_rate,
                'avg_time': row[2],
                'last_practiced': row[3],
                'mastery_level': row[4]
            }
        else:
            return {
                'topic': topic,
                'attempts': 0,
                'correct': 0,
                'success_rate': 0,
                'avg_time': 0,
                'last_practiced': None,
                'mastery_level': 'Not Started'
            }
    
    def get_all_topic_stats(self) -> List[Dict]:
        """Get statistics for all topics."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT topic, total_attempts, total_correct, mastery_level
            FROM topic_stats
            ORDER BY total_attempts DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        stats = []
        for row in rows:
            success_rate = (row[2] / row[1] * 100) if row[1] > 0 else 0
            stats.append({
                'topic': row[0],
                'attempts': row[1],
                'correct': row[2],
                'success_rate': success_rate,
                'mastery_level': row[3]
            })
        
        return stats
    
    def get_overall_stats(self) -> Dict:
        """Get overall performance statistics."""
        total_questions = self.user_profile.get('total_questions', 0)
        total_correct = self.user_profile.get('total_correct', 0)
        success_rate = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        mastered = len(self.get_mastered_topics())
        learning = len([m for m in self.topic_mastery.values() if m == 'Learning'])
        proficient = len([m for m in self.topic_mastery.values() if m == 'Proficient'])
        
        return {
            'total_questions': total_questions,
            'total_correct': total_correct,
            'success_rate': success_rate,
            'mastered_topics': mastered,
            'learning_topics': learning,
            'proficient_topics': proficient,
            'level': self.user_profile.get('level', 'Beginner')
        }
    
    # ==================== Utility Methods ====================
    
    def clear_session_state(self):
        """Clear current session state."""
        self.session_state = {}
        self.questions_in_current_topic = 0
        self.correct_in_current_topic = 0
        self.topic_question_count.clear()
        self.topic_correct_count.clear()
    
    def export_data(self, filepath: str):
        """Export all data to JSON file."""
        data = {
            'user_profile': self.user_profile,
            'topic_mastery': self.topic_mastery,
            'difficulty_levels': self.difficulty_levels,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"✓ Data exported to {filepath}")
    
    def __repr__(self):
        stats = self.get_overall_stats()
        return f"<StateManager: {stats['total_questions']} questions, {stats['mastered_topics']} mastered>"


# Global instance
def get_state_manager() -> StateManager:
    """Get the global state manager instance."""
    return StateManager()
