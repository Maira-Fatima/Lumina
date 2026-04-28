"""
Recommendation Engine - Intelligent learning recommendations

Integrates:
- ML Module predictions
- Expert System reasoning
- Performance trends
- User preferences
"""

from typing import List, Dict, Optional
from .state_manager import StateManager


class RecommendationEngine:
    """
    Generates intelligent learning recommendations.
    
    Combines multiple sources:
    - Expert system rules
    - ML predictions
    - Performance analysis
    - Prerequisite validation
    """
    
    def __init__(self, state_manager: StateManager = None):
        """Initialize recommendation engine."""
        self.state = state_manager or StateManager()
    
    def get_recommendations(
        self,
        context: str = 'general',
        max_recommendations: int = 5
    ) -> List[Dict]:
        """
        Get personalized recommendations.
        
        Args:
            context (str): Context ('general', 'struggling', 'mastery', 'quiz')
            max_recommendations (int): Maximum recommendations to return
            
        Returns:
            list: Recommended actions with reasons
        """
        recommendations = []
        
        # Get current learning state
        mastered_topics = self.state.get_mastered_topics()
        all_topics = self.state.get_all_topic_stats()
        stats = self.state.get_overall_stats()
        
        # Load modules on demand
        try:
            from expert_system import KnowledgeBase, InferenceEngine, PrerequisiteGraph
            
            # Initialize expert system
            kb = KnowledgeBase()
            engine = InferenceEngine(kb)
            prereq_graph = PrerequisiteGraph()
            
            # Update knowledge base with current state
            for topic in mastered_topics:
                kb.set_topic_mastery(topic, 'Mastered')
            
            # Get expert system recommendations
            expert_recs = engine.get_recommendations()
            recommendations.extend(expert_recs)
            
            # Get next learnable topics
            next_topics = prereq_graph.get_next_topics(set(mastered_topics))
            
            for topic in next_topics[:3]:
                recommendations.append({
                    'type': 'next_topic',
                    'topic': topic,
                    'confidence': 0.8,
                    'reason': 'All prerequisites met - ready to learn'
                })
            
        except Exception as e:
            print(f"⚠ Could not load expert system: {e}")
        
        # Add performance-based recommendations
        if stats['total_questions'] > 0:
            if stats['success_rate'] < 60:
                recommendations.append({
                    'type': 'practice',
                    'topic': 'Review Basics',
                    'confidence': 0.9,
                    'reason': 'Consider reviewing fundamental concepts'
                })
            elif stats['success_rate'] > 85:
                recommendations.append({
                    'type': 'next_topic',
                    'topic': 'Advanced Topics',
                    'confidence': 0.85,
                    'reason': 'You\'re doing great! Try more challenging topics'
                })
        
        # Add topic-specific recommendations from user history
        for topic_stat in all_topics:
            topic = topic_stat.get('topic', '')
            success_rate = topic_stat.get('success_rate', 0)
            attempts = topic_stat.get('attempts', 0)
            
            if attempts >= 3:
                if success_rate < 60:
                    recommendations.append({
                        'type': 'practice',
                        'topic': topic,
                        'confidence': 0.8,
                        'reason': f'Practice more {topic} - current: {success_rate:.0f}%'
                    })
                elif success_rate >= 80:
                    recommendations.append({
                        'type': 'next_topic',
                        'topic': f'Advanced {topic}',
                        'confidence': 0.75,
                        'reason': f'Strong grasp of {topic} - ready for advanced topics'
                    })
        
        # Fallback recommendations for new users
        if not recommendations:
            beginner_topics = ['Python Basics', 'Data Structures', 'Algorithms', 'Machine Learning']
            for topic in beginner_topics[:3]:
                recommendations.append({
                    'type': 'next_topic',
                    'topic': topic,
                    'confidence': 0.7,
                    'reason': 'Great topic to start your learning journey'
                })
        
        if context == 'struggling':
            recommendations.insert(0, {
                'type': 'support',
                'topic': self.state.get_current_topic() or 'Current Topic',
                'confidence': 0.85,
                'reason': 'Try easier questions or review prerequisites'
            })
        
        # Sort by confidence
        recommendations.sort(key=lambda r: r.get('confidence', 0), reverse=True)
        
        return recommendations[:max_recommendations]
    
    def suggest_next_topic(self) -> Optional[Dict]:
        """Suggest the best next topic to learn."""
        try:
            from expert_system import PrerequisiteGraph
            
            prereq_graph = PrerequisiteGraph()
            mastered = set(self.state.get_mastered_topics())
            next_topics = prereq_graph.get_next_topics(mastered)
            
            if next_topics:
                return {
                    'topic': next_topics[0],
                    'reason': 'Recommended next step in your learning path'
                }
        except:
            pass
        
        return None
    
    def get_practice_recommendations(self, topic: str) -> List[str]:
        """Get practice recommendations for a topic."""
        stats = self.state.get_topic_stats(topic)
        recommendations = []
        
        if stats['success_rate'] < 70:
            recommendations.append(f"Practice more {topic} fundamentals")
            recommendations.append(f"Review {topic} concepts")
        
        if stats['attempts'] < 5:
            recommendations.append(f"Try more {topic} questions")
        
        if not recommendations:
            recommendations.append(f"You're doing well with {topic}!")
        
        return recommendations
