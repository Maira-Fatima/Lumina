from core.engine import QueryMatchingEngine
from core.topic_graph import SearchNavigationModule, build_topic_graph
from core.data_loader import download_nltk_data, combined_data, get_expanded_knowledge_base
import streamlit as st

@st.cache_resource
def load_ai_companion():
    """
    Loads, trains, and caches the AIStudyCompanion instance.
    This function runs only once and is cached by Streamlit.
    """
    print("Downloading NLTK data (if needed)...")
    download_nltk_data() # Ensure data is ready
    
    print("Initializing AI Study Companion...")
    # Load the expanded knowledge base (7,350+ entries)
    knowledge_base = get_expanded_knowledge_base()
    topic_graph = build_topic_graph(knowledge_base)
    tutor = AIStudyCompanion(knowledge_base, topic_graph)
    print("AI Companion is ready.")
    return tutor

class AIStudyCompanion:
    """
    Unified class that combines query matching, topic navigation, and adaptive learning.
    Integrates ML Module, Expert System, and Adaptive Learning for intelligent tutoring.
    """
    def __init__(self, dataset, topic_graph):
        self.engine = QueryMatchingEngine(dataset)
        self.navigator = SearchNavigationModule(topic_graph)
        self.engine.fit() # Train the model on init
        
        # Lazy loading of advanced modules to avoid circular imports
        self.ml_loaded = False
        self.expert_loaded = False
        self.adaptive_loaded = False
        
        self.topic_classifier = None
        self.difficulty_classifier = None
        self.knowledge_base = None
        self.inference_engine = None
        self.prereq_graph = None
        self.state_manager = None
        self.diff_manager = None
        self.rec_engine = None

    def _load_ml_module(self):
        """Lazy load ML module."""
        if not self.ml_loaded:
            try:
                from ml_module.classifier import TopicClassifier, DifficultyClassifier
                self.topic_classifier = TopicClassifier()
                self.difficulty_classifier = DifficultyClassifier()
                # Try to load pre-trained models
                try:
                    self.topic_classifier.load_model('ml_module/models/topic_classifier.pkl')
                    self.difficulty_classifier.load_model('ml_module/models/difficulty_classifier.pkl')
                except:
                    print("Note: Pre-trained models not found. Using basic matching.")
                self.ml_loaded = True
            except Exception as e:
                print(f"ML Module not available: {e}")

    def _load_expert_system(self):
        """Lazy load Expert System."""
        if not self.expert_loaded:
            try:
                from expert_system.knowledge_base import KnowledgeBase
                from expert_system.inference_engine import InferenceEngine
                from expert_system.prerequisite_graph import PrerequisiteGraph
                
                self.knowledge_base = KnowledgeBase()
                self.inference_engine = InferenceEngine(self.knowledge_base)
                self.prereq_graph = PrerequisiteGraph()
                self.expert_loaded = True
            except Exception as e:
                print(f"Expert System not available: {e}")

    def _load_adaptive_learning(self):
        """Lazy load Adaptive Learning module."""
        if not self.adaptive_loaded:
            try:
                from adaptive_learning.state_manager import StateManager
                from adaptive_learning.difficulty_manager import DifficultyManager
                from adaptive_learning.recommendation_engine import RecommendationEngine
                
                self.state_manager = StateManager()
                self.diff_manager = DifficultyManager(self.state_manager)
                self.rec_engine = RecommendationEngine(self.state_manager)
                self.adaptive_loaded = True
            except Exception as e:
                print(f"Adaptive Learning not available: {e}")

    def ask(self, query, user_id=None, record_performance=True):
        """
        Responds to user queries using advanced AI features:
        - Typo correction
        - Topic classification
        - Prerequisite checking
        - Performance tracking
        - Difficulty adjustment
        - Smart recommendations
        
        Args:
            query: User's question
            user_id: User identifier for personalization
            record_performance: Whether to track this interaction
            
        Returns:
            dict: {
                'answer': str,
                'corrected_query': str,
                'corrections': list,
                'suggestions': dict,
                'topic': str,
                'difficulty': str,
                'related_topics': list,
                'prerequisites': list,
                'prerequisites_met': bool,
                'recommendations': dict,
                'difficulty_adjusted': bool,
                'adjustment_reason': str
            }
        """
        # Load modules if needed
        self._load_ml_module()
        self._load_expert_system()
        
        if user_id and record_performance:
            self._load_adaptive_learning()
            if self.state_manager:
                self.state_manager.load_user(user_id)
        
        # Get response with typo correction
        result = self.engine.find_match(query)
        
        # Classify topic and difficulty using ML
        topic = None
        difficulty = None
        if self.ml_loaded and self.topic_classifier:
            try:
                topic, confidence = self.topic_classifier.predict(query)
                difficulty = self.difficulty_classifier.predict(query)
                result['topic'] = topic
                result['difficulty'] = difficulty
                result['topic_confidence'] = confidence
            except:
                # Fallback to keyword extraction
                topic = self.extract_topic_from_query(query)
                result['topic'] = topic
        else:
            topic = self.extract_topic_from_query(query)
            result['topic'] = topic
        
        # Get related topics
        matched_topic = result.get('topic', 'General')
        print(f"\nMatched Topic: {matched_topic}")
        related_topics = self.navigator.get_related_topics(matched_topic, method="bfs")
        result['related_topics'] = related_topics
        
        # Check prerequisites using Expert System
        if self.expert_loaded and self.prereq_graph and topic:
            prerequisites = self.prereq_graph.get_all_prerequisites(topic)
            result['prerequisites'] = prerequisites
            
            # Check if prerequisites are met
            prerequisites_met = True
            if self.state_manager:
                for prereq in prerequisites:
                    mastery = self.state_manager.get_topic_mastery(prereq)
                    if mastery < 70:  # 70% threshold for prerequisite mastery
                        prerequisites_met = False
                        break
            result['prerequisites_met'] = prerequisites_met
            
            # Update knowledge base with current state
            if self.state_manager and topic:
                mastery = self.state_manager.get_topic_mastery(topic)
                self.knowledge_base.set_topic_mastery(topic, mastery)
        
        # Record performance and adjust difficulty if enabled
        difficulty_adjusted = False
        adjustment_reason = ""
        if user_id and record_performance and self.adaptive_loaded and self.state_manager:
            # For now, assume correct answer (will be updated when user confirms)
            # This will be properly integrated in helper.py
            current_difficulty = self.state_manager.get_topic_difficulty(topic) if topic else "Intermediate"
            result['current_difficulty'] = current_difficulty
            
            # Check if difficulty adjustment needed
            if topic and self.diff_manager.should_adjust_difficulty(topic):
                action, new_diff, reason = self.diff_manager.calculate_difficulty_adjustment(topic)
                if action != "maintain":
                    difficulty_adjusted = True
                    adjustment_reason = reason
                    result['difficulty_adjusted'] = True
                    result['new_difficulty'] = new_diff
                    result['adjustment_reason'] = reason
        
        # Get recommendations
        if self.adaptive_loaded and self.rec_engine and topic:
            try:
                recommendations = self.rec_engine.get_recommendations(
                    current_topic=topic,
                    recent_performance=[]  # Will be populated from state manager
                )
                result['recommendations'] = recommendations
            except:
                result['recommendations'] = {}
        
        return result

    def extract_topic_from_query(self, query):
        """
        Extracts potential topic keywords from query.
        Enhanced to use Expert System's prerequisite graph if available.
        """
        # Try Expert System first
        if self.expert_loaded and self.prereq_graph:
            query_lower = query.lower()
            for topic in self.prereq_graph.graph.keys():
                if topic.lower() in query_lower:
                    return topic
        
        # Fallback to basic graph
        for topic in self.navigator.topic_graph.keys():
            if topic.lower() in query.lower():
                return topic
        return "General"
    
    def get_learning_path(self, topic, user_id=None):
        """
        Generate a personalized learning path for a topic.
        
        Args:
            topic: Target topic to learn
            user_id: User identifier for personalization
            
        Returns:
            list: Ordered list of topics to study
        """
        self._load_expert_system()
        self._load_adaptive_learning()
        
        if user_id and self.state_manager:
            self.state_manager.load_user(user_id)
        
        if self.expert_loaded and self.prereq_graph:
            # Get personalized path based on current mastery
            mastered_topics = set()
            if self.state_manager:
                # Get all topics with high mastery
                for t in self.prereq_graph.graph.keys():
                    if self.state_manager.get_topic_mastery(t) >= 70:
                        mastered_topics.add(t)
            
            path = self.prereq_graph.generate_learning_path(topic, mastered_topics)
            return path
        
        return [topic]
    
    def check_can_learn(self, topic, user_id=None):
        """
        Check if user has met prerequisites for a topic.
        
        Args:
            topic: Topic to check
            user_id: User identifier
            
        Returns:
            dict: {
                'can_learn': bool,
                'missing_prerequisites': list,
                'mastery_levels': dict
            }
        """
        self._load_expert_system()
        self._load_adaptive_learning()
        
        if user_id and self.state_manager:
            self.state_manager.load_user(user_id)
        
        result = {
            'can_learn': True,
            'missing_prerequisites': [],
            'mastery_levels': {}
        }
        
        if self.expert_loaded and self.prereq_graph:
            prerequisites = self.prereq_graph.get_all_prerequisites(topic)
            
            for prereq in prerequisites:
                mastery = 0
                if self.state_manager:
                    mastery = self.state_manager.get_topic_mastery(prereq)
                
                result['mastery_levels'][prereq] = mastery
                
                if mastery < 70:
                    result['can_learn'] = False
                    result['missing_prerequisites'].append(prereq)
        
        return result