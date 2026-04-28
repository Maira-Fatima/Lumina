"""
Performance Tracker - Time-series performance analysis

Tracks and analyzes:
- Success rates over time
- Learning trends
- Topic progression
- Time-series data
"""

import sqlite3
from typing import List, Dict
from datetime import datetime, timedelta
from .state_manager import StateManager


class PerformanceTracker:
    """
    Tracks and analyzes student performance over time.
    
    Provides:
    - Time-series performance data
    - Trend analysis
    - Progress visualization data
    - Success rate calculations
    """
    
    def __init__(self, state_manager: StateManager = None):
        """Initialize performance tracker."""
        self.state = state_manager or StateManager()
    
    def calculate_success_rate(self, topic: str = None) -> float:
        """
        Calculate success rate: (correct / total) × 100
        
        Args:
            topic (str): Topic to calculate for (None = overall)
            
        Returns:
            float: Success rate percentage
        """
        if topic:
            stats = self.state.get_topic_stats(topic)
            return stats['success_rate']
        else:
            overall = self.state.get_overall_stats()
            return overall['success_rate']
    
    def get_performance_trend(
        self,
        topic: str = None,
        days: int = 7
    ) -> Dict:
        """
        Get performance trend over time.
        
        Args:
            topic (str): Topic to analyze (None = all topics)
            days (int): Number of days to analyze
            
        Returns:
            dict: Trend data with time series
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        history = self.state.get_performance_history(topic, limit=1000)
        
        # Filter by date
        recent_history = [
            h for h in history
            if datetime.fromisoformat(h['timestamp']) > cutoff_date
        ]
        
        if not recent_history:
            return {
                'trend': 'insufficient_data',
                'data_points': 0,
                'success_rate': 0
            }
        
        # Calculate daily success rates
        daily_data = {}
        for entry in recent_history:
            date = entry['timestamp'][:10]  # YYYY-MM-DD
            if date not in daily_data:
                daily_data[date] = {'total': 0, 'correct': 0}
            
            daily_data[date]['total'] += 1
            if entry['correct']:
                daily_data[date]['correct'] += 1
        
        # Calculate success rates
        time_series = []
        for date, data in sorted(daily_data.items()):
            rate = (data['correct'] / data['total']) * 100
            time_series.append({
                'date': date,
                'success_rate': rate,
                'total': data['total']
            })
        
        # Determine trend
        if len(time_series) < 2:
            trend = 'stable'
        else:
            first_rate = time_series[0]['success_rate']
            last_rate = time_series[-1]['success_rate']
            change = last_rate - first_rate
            
            if change > 10:
                trend = 'improving'
            elif change < -10:
                trend = 'declining'
            else:
                trend = 'stable'
        
        return {
            'trend': trend,
            'data_points': len(time_series),
            'time_series': time_series,
            'overall_rate': sum(d['success_rate'] for d in time_series) / len(time_series)
        }
    
    def get_topic_progress(self) -> List[Dict]:
        """Get progress for all topics."""
        return self.state.get_all_topic_stats()
    
    def get_learning_summary(self, days: int = 30) -> Dict:
        """
        Get comprehensive learning summary.
        
        Args:
            days (int): Days to summarize
            
        Returns:
            dict: Learning summary with all stats
        """
        trend = self.get_performance_trend(days=days)
        overall = self.state.get_overall_stats()
        all_topics = self.state.get_all_topic_stats()
        
        # Get mastered and needs practice topics
        mastered = []
        needs_practice = []
        
        for topic_stat in all_topics:
            mastery_level = topic_stat.get('mastery_level', 'Learning')
            topic_name = topic_stat.get('topic', '')
            success_rate = topic_stat.get('success_rate', 0)
            
            if mastery_level == 'Mastered':
                mastered.append(topic_name)
            elif success_rate < 60:
                needs_practice.append(topic_name)
        
        # Count unique topics studied
        topics_studied = len([t for t in all_topics if t.get('attempts', 0) > 0])
        
        return {
            'period_days': days,
            'total_questions': overall['total_questions'],
            'total_correct': overall.get('total_correct', 0),
            'overall_success_rate': overall['success_rate'],
            'success_rate': overall['success_rate'],  # Backwards compatibility
            'trend': trend['trend'],
            'topics_studied': topics_studied,
            'mastered_topics': mastered,
            'needs_practice': needs_practice,
            'learning_topics': overall['learning_topics'],
            'proficient_topics': overall.get('proficient_topics', 0),
            'time_series': trend.get('time_series', [])
        }
