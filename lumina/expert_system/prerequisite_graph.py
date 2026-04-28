"""
Prerequisite Graph Module - Manages topic dependencies and learning paths

This module tracks complex prerequisite chains:
- Builds directed acyclic graph (DAG) of topic dependencies
- Validates learning paths
- Suggests missing prerequisites
- Generates personalized curriculum
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import deque, defaultdict


class PrerequisiteGraph:
    """
    Manages prerequisite relationships between topics.
    
    Example: To learn Neural Networks, you need:
    - Linear Algebra
    - Calculus
    - Python
    - Basic Machine Learning
    """
    
    def __init__(self):
        """Initialize the prerequisite graph."""
        self.graph: Dict[str, List[str]] = defaultdict(list)  # topic -> prerequisites
        self.reverse_graph: Dict[str, List[str]] = defaultdict(list)  # topic -> dependents
        self.topic_metadata: Dict[str, Dict] = {}  # Additional info per topic
        
        # Build default prerequisite graph
        self._build_default_graph()
    
    def _build_default_graph(self):
        """Build comprehensive prerequisite graph for AI topics."""
        
        # === Foundational Topics ===
        self.add_prerequisite("Python Basics", [])
        self.add_prerequisite("Mathematics Basics", [])
        
        # === Data Structures & Algorithms ===
        self.add_prerequisite("Arrays", ["Python Basics"])
        self.add_prerequisite("Linked Lists", ["Python Basics", "Arrays"])
        self.add_prerequisite("Stacks and Queues", ["Arrays"])
        self.add_prerequisite("Trees", ["Linked Lists"])
        self.add_prerequisite("Binary Search Trees", ["Trees"])
        self.add_prerequisite("Graphs", ["Trees"])
        self.add_prerequisite("Hash Tables", ["Arrays"])
        
        # === Search Algorithms ===
        self.add_prerequisite("Linear Search", ["Arrays"])
        self.add_prerequisite("Binary Search", ["Arrays", "Mathematics Basics"])
        self.add_prerequisite("BFS", ["Graphs", "Stacks and Queues"])
        self.add_prerequisite("DFS", ["Graphs", "Stacks and Queues"])
        self.add_prerequisite("Dijkstra's Algorithm", ["Graphs", "BFS"])
        self.add_prerequisite("A* Search", ["Dijkstra's Algorithm", "Heuristics"])
        self.add_prerequisite("Heuristics", ["BFS", "DFS"])
        
        # === Mathematics for AI ===
        self.add_prerequisite("Linear Algebra", ["Mathematics Basics"])
        self.add_prerequisite("Calculus", ["Mathematics Basics"])
        self.add_prerequisite("Probability", ["Mathematics Basics"])
        self.add_prerequisite("Statistics", ["Probability"])
        
        # === Machine Learning Fundamentals ===
        self.add_prerequisite("Introduction to ML", ["Python Basics", "Statistics"])
        self.add_prerequisite("Supervised Learning", ["Introduction to ML", "Linear Algebra"])
        self.add_prerequisite("Unsupervised Learning", ["Introduction to ML"])
        self.add_prerequisite("Linear Regression", ["Supervised Learning", "Calculus"])
        self.add_prerequisite("Logistic Regression", ["Linear Regression", "Probability"])
        self.add_prerequisite("Decision Trees", ["Supervised Learning"])
        self.add_prerequisite("Random Forest", ["Decision Trees"])
        self.add_prerequisite("SVM", ["Supervised Learning", "Linear Algebra"])
        self.add_prerequisite("KNN", ["Supervised Learning"])
        self.add_prerequisite("Naive Bayes", ["Supervised Learning", "Probability"])
        self.add_prerequisite("K-Means", ["Unsupervised Learning", "Linear Algebra"])
        self.add_prerequisite("PCA", ["Unsupervised Learning", "Linear Algebra"])
        
        # === Deep Learning ===
        self.add_prerequisite("Neural Networks", [
            "Linear Algebra",
            "Calculus",
            "Python Basics",
            "Supervised Learning"
        ])
        self.add_prerequisite("Backpropagation", ["Neural Networks", "Calculus"])
        self.add_prerequisite("CNN", ["Neural Networks", "Linear Algebra"])
        self.add_prerequisite("RNN", ["Neural Networks"])
        self.add_prerequisite("LSTM", ["RNN", "Backpropagation"])
        self.add_prerequisite("GRU", ["RNN"])
        self.add_prerequisite("Transformers", ["LSTM", "Attention Mechanism"])
        self.add_prerequisite("Attention Mechanism", ["Neural Networks"])
        self.add_prerequisite("GANs", ["Neural Networks", "CNN"])
        self.add_prerequisite("Autoencoders", ["Neural Networks"])
        
        # === Natural Language Processing ===
        self.add_prerequisite("Text Preprocessing", ["Python Basics"])
        self.add_prerequisite("Tokenization", ["Text Preprocessing"])
        self.add_prerequisite("Word Embeddings", ["Neural Networks", "Tokenization"])
        self.add_prerequisite("Word2Vec", ["Word Embeddings"])
        self.add_prerequisite("BERT", ["Transformers", "Word Embeddings"])
        self.add_prerequisite("GPT", ["Transformers"])
        self.add_prerequisite("NER", ["Text Preprocessing", "Supervised Learning"])
        self.add_prerequisite("Sentiment Analysis", ["Text Preprocessing", "Supervised Learning"])
        
        # === Computer Vision ===
        self.add_prerequisite("Image Processing", ["Python Basics", "Linear Algebra"])
        self.add_prerequisite("Edge Detection", ["Image Processing"])
        self.add_prerequisite("Image Classification", ["CNN"])
        self.add_prerequisite("Object Detection", ["CNN"])
        self.add_prerequisite("YOLO", ["Object Detection"])
        self.add_prerequisite("R-CNN", ["Object Detection"])
        self.add_prerequisite("Image Segmentation", ["CNN"])
        
        # === Reinforcement Learning ===
        self.add_prerequisite("RL Fundamentals", ["Probability", "Python Basics"])
        self.add_prerequisite("MDP", ["RL Fundamentals"])
        self.add_prerequisite("Q-Learning", ["MDP"])
        self.add_prerequisite("SARSA", ["Q-Learning"])
        self.add_prerequisite("DQN", ["Q-Learning", "Neural Networks"])
        self.add_prerequisite("Policy Gradients", ["RL Fundamentals", "Calculus"])
        self.add_prerequisite("Actor-Critic", ["Policy Gradients", "Q-Learning"])
        
        # === Expert Systems ===
        self.add_prerequisite("Knowledge Representation", ["Python Basics"])
        self.add_prerequisite("Propositional Logic", ["Knowledge Representation"])
        self.add_prerequisite("First-Order Logic", ["Propositional Logic"])
        self.add_prerequisite("Inference Rules", ["Propositional Logic"])
        self.add_prerequisite("Forward Chaining", ["Inference Rules"])
        self.add_prerequisite("Backward Chaining", ["Inference Rules"])
        self.add_prerequisite("Fuzzy Logic", ["Probability"])
        
        # === OOP (Object-Oriented Programming) ===
        self.add_prerequisite("OOP Basics", ["Python Basics"])
        self.add_prerequisite("Encapsulation", ["OOP Basics"])
        self.add_prerequisite("Inheritance", ["OOP Basics"])
        self.add_prerequisite("Polymorphism", ["Inheritance"])
        
        # === Database ===
        self.add_prerequisite("Database Basics", ["Python Basics"])
        self.add_prerequisite("SQL", ["Database Basics"])
        self.add_prerequisite("Relational Model", ["Database Basics"])
        self.add_prerequisite("Normalization", ["Relational Model"])
        
        # Add metadata for important topics
        self._add_topic_metadata()
    
    def _add_topic_metadata(self):
        """Add additional metadata for topics."""
        # Add difficulty levels, estimated time, importance
        metadata_map = {
            "Python Basics": {"difficulty": "Beginner", "time_hours": 20, "importance": "Critical"},
            "Neural Networks": {"difficulty": "Advanced", "time_hours": 40, "importance": "Critical"},
            "Transformers": {"difficulty": "Expert", "time_hours": 60, "importance": "High"},
            "BFS": {"difficulty": "Intermediate", "time_hours": 5, "importance": "High"},
            "DFS": {"difficulty": "Intermediate", "time_hours": 5, "importance": "High"},
            # Add more as needed
        }
        
        for topic, metadata in metadata_map.items():
            self.topic_metadata[topic] = metadata
    
    def add_prerequisite(self, topic: str, prerequisites: List[str]):
        """
        Add a topic with its prerequisites.
        
        Args:
            topic (str): Topic name
            prerequisites (list): List of prerequisite topics
        """
        self.graph[topic] = prerequisites
        
        # Update reverse graph
        for prereq in prerequisites:
            self.reverse_graph[prereq].append(topic)
    
    def get_prerequisites(self, topic: str) -> List[str]:
        """
        Get direct prerequisites for a topic.
        
        Args:
            topic (str): Topic name
            
        Returns:
            list: Direct prerequisites
        """
        return self.graph.get(topic, [])
    
    def get_all_prerequisites(self, topic: str) -> List[str]:
        """
        Get all prerequisites (transitive closure) for a topic.
        
        Args:
            topic (str): Topic name
            
        Returns:
            list: All prerequisites in learning order
        """
        if topic not in self.graph:
            return []
        
        visited = set()
        result = []
        
        def dfs(current):
            if current in visited:
                return
            visited.add(current)
            
            for prereq in self.graph.get(current, []):
                dfs(prereq)
            
            if current != topic:
                result.append(current)
        
        dfs(topic)
        return result
    
    def get_missing_prerequisites(self, topic: str, mastered_topics: Set[str]) -> List[str]:
        """
        Find prerequisites that are not yet mastered.
        
        Args:
            topic (str): Target topic
            mastered_topics (set): Topics already mastered
            
        Returns:
            list: Missing prerequisites
        """
        all_prereqs = self.get_all_prerequisites(topic)
        missing = [p for p in all_prereqs if p not in mastered_topics]
        return missing
    
    def can_learn(self, topic: str, mastered_topics: Set[str]) -> bool:
        """
        Check if a student can learn a topic based on mastered prerequisites.
        
        Args:
            topic (str): Topic to check
            mastered_topics (set): Already mastered topics
            
        Returns:
            bool: True if all direct prerequisites are mastered
        """
        direct_prereqs = self.get_prerequisites(topic)
        return all(prereq in mastered_topics for prereq in direct_prereqs)
    
    def get_next_topics(self, mastered_topics: Set[str]) -> List[str]:
        """
        Get topics that can be learned next (all prerequisites met).
        
        Args:
            mastered_topics (set): Already mastered topics
            
        Returns:
            list: Topics ready to learn
        """
        next_topics = []
        
        for topic in self.graph.keys():
            if topic not in mastered_topics:
                if self.can_learn(topic, mastered_topics):
                    next_topics.append(topic)
        
        return next_topics
    
    def generate_learning_path(
        self,
        goal_topic: str,
        mastered_topics: Set[str] = None
    ) -> List[str]:
        """
        Generate a personalized learning path from current state to goal.
        
        Args:
            goal_topic (str): Target topic
            mastered_topics (set): Already mastered topics
            
        Returns:
            list: Ordered learning path
        """
        if mastered_topics is None:
            mastered_topics = set()
        
        # Get all prerequisites for goal
        all_prereqs = self.get_all_prerequisites(goal_topic)
        
        # Filter out already mastered
        needed = [t for t in all_prereqs if t not in mastered_topics]
        
        # Add goal at the end
        if goal_topic not in mastered_topics:
            needed.append(goal_topic)
        
        return needed
    
    def get_topic_depth(self, topic: str) -> int:
        """
        Calculate the depth of a topic in the prerequisite tree.
        
        Args:
            topic (str): Topic name
            
        Returns:
            int: Depth (0 = no prerequisites)
        """
        if topic not in self.graph or not self.graph[topic]:
            return 0
        
        max_depth = 0
        for prereq in self.graph[topic]:
            depth = self.get_topic_depth(prereq) + 1
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def get_curriculum(
        self,
        domain: str = "AI",
        mastered_topics: Set[str] = None
    ) -> Dict[str, List[str]]:
        """
        Generate a structured curriculum for a domain.
        
        Args:
            domain (str): Domain (AI, ML, DL, etc.)
            mastered_topics (set): Already mastered topics
            
        Returns:
            dict: Curriculum organized by level
        """
        if mastered_topics is None:
            mastered_topics = set()
        
        # Get all topics
        all_topics = list(self.graph.keys())
        
        # Filter by domain (simplified - could be more sophisticated)
        if domain == "ML":
            keywords = ["ML", "Machine Learning", "Regression", "Classification", 
                       "Clustering", "SVM", "KNN", "Naive Bayes", "Decision", "Forest"]
        elif domain == "DL":
            keywords = ["Neural", "CNN", "RNN", "LSTM", "GRU", "Transformer",
                       "GAN", "Autoencoder", "Deep Learning"]
        elif domain == "NLP":
            keywords = ["NLP", "Text", "Word", "BERT", "GPT", "Token", "Sentiment"]
        elif domain == "CV":
            keywords = ["Image", "Vision", "CNN", "YOLO", "R-CNN", "Segmentation"]
        else:  # AI - all topics
            keywords = []
        
        if keywords:
            domain_topics = [
                t for t in all_topics
                if any(keyword.lower() in t.lower() for keyword in keywords)
            ]
        else:
            domain_topics = all_topics
        
        # Organize by depth
        curriculum = defaultdict(list)
        
        for topic in domain_topics:
            if topic not in mastered_topics:
                depth = self.get_topic_depth(topic)
                level = "Beginner" if depth <= 1 else \
                       "Intermediate" if depth <= 3 else \
                       "Advanced" if depth <= 5 else "Expert"
                curriculum[level].append(topic)
        
        return dict(curriculum)
    
    def validate_path(self, learning_path: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate if a learning path satisfies all prerequisites.
        
        Args:
            learning_path (list): Proposed learning path
            
        Returns:
            tuple: (is_valid, violations)
        """
        mastered = set()
        violations = []
        
        for topic in learning_path:
            prereqs = self.get_prerequisites(topic)
            
            for prereq in prereqs:
                if prereq not in mastered:
                    violations.append(
                        f"Cannot learn '{topic}' before '{prereq}'"
                    )
            
            mastered.add(topic)
        
        is_valid = len(violations) == 0
        return is_valid, violations
    
    def get_topic_info(self, topic: str) -> Dict:
        """
        Get comprehensive information about a topic.
        
        Args:
            topic (str): Topic name
            
        Returns:
            dict: Topic information
        """
        return {
            'topic': topic,
            'prerequisites': self.get_prerequisites(topic),
            'all_prerequisites': self.get_all_prerequisites(topic),
            'depth': self.get_topic_depth(topic),
            'enables': self.reverse_graph.get(topic, []),
            'metadata': self.topic_metadata.get(topic, {})
        }
