"""
Knowledge Base Module - Stores facts, rules, and domain knowledge

This module maintains the expert system's knowledge including:
- Facts about student progress and mastery
- Domain rules for AI/ML/DSA topics
- Prerequisite relationships
- Learning recommendations
"""

import json
import os
from typing import Dict, List, Any, Set


class KnowledgeBase:
    """
    Central repository for expert system knowledge.
    
    Maintains three types of knowledge:
    1. Facts: Current state (e.g., "student_mastered(BFS)")
    2. Rules: If-then logic (e.g., "IF mastered(BFS) THEN recommend(DFS)")
    3. Domain Knowledge: Topic relationships and prerequisites
    """
    
    def __init__(self, rules_dir='expert_system/rules'):
        """
        Initialize the knowledge base.
        
        Args:
            rules_dir (str): Directory containing rule JSON files
        """
        self.rules_dir = rules_dir
        self.facts: Set[str] = set()  # Current facts (e.g., "mastered_BFS")
        self.rules: List[Dict] = []  # Production rules
        self.domain_knowledge: Dict = {}  # Topic information
        self.user_state: Dict[str, Any] = {}  # Current user state
        
        # Load rules from files
        self._load_rules()
    
    def _load_rules(self):
        """Load all rules from JSON files."""
        if not os.path.exists(self.rules_dir):
            print(f"⚠ Rules directory not found: {self.rules_dir}")
            self._create_default_rules()
            return
        
        # Load prerequisite rules
        prereq_file = os.path.join(self.rules_dir, 'prerequisites.json')
        if os.path.exists(prereq_file):
            with open(prereq_file, 'r') as f:
                prereq_data = json.load(f)
                self.rules.extend(prereq_data.get('rules', []))
                print(f"✓ Loaded {len(prereq_data.get('rules', []))} prerequisite rules")
        
        # Load learning path rules
        path_file = os.path.join(self.rules_dir, 'learning_paths.json')
        if os.path.exists(path_file):
            with open(path_file, 'r') as f:
                path_data = json.load(f)
                self.domain_knowledge['learning_paths'] = path_data.get('paths', {})
                print(f"✓ Loaded {len(path_data.get('paths', {}))} learning paths")
        
        # Load recommendation rules
        rec_file = os.path.join(self.rules_dir, 'recommendations.json')
        if os.path.exists(rec_file):
            with open(rec_file, 'r') as f:
                rec_data = json.load(f)
                self.rules.extend(rec_data.get('rules', []))
                print(f"✓ Loaded {len(rec_data.get('rules', []))} recommendation rules")
    
    def _create_default_rules(self):
        """Create default rules if none exist."""
        os.makedirs(self.rules_dir, exist_ok=True)
        
        # Default prerequisite rules will be created by rule_manager
        print("⚠ Creating default rule files...")
    
    def add_fact(self, fact: str):
        """
        Add a fact to the knowledge base.
        
        Args:
            fact (str): Fact string (e.g., "mastered_BFS")
        """
        self.facts.add(fact)
    
    def remove_fact(self, fact: str):
        """Remove a fact from the knowledge base."""
        self.facts.discard(fact)
    
    def has_fact(self, fact: str) -> bool:
        """Check if a fact exists in the knowledge base."""
        return fact in self.facts
    
    def add_rule(self, rule: Dict):
        """
        Add a new rule to the knowledge base.
        
        Rule format:
        {
            'id': 'rule_1',
            'name': 'Recommend DFS after BFS',
            'conditions': ['mastered_BFS', 'not_mastered_DFS'],
            'actions': ['recommend_DFS'],
            'confidence': 0.9,
            'priority': 5
        }
        """
        self.rules.append(rule)
    
    def get_rules_by_type(self, rule_type: str) -> List[Dict]:
        """
        Get all rules of a specific type.
        
        Args:
            rule_type (str): Type of rules (e.g., 'prerequisite', 'recommendation')
            
        Returns:
            list: Matching rules
        """
        return [r for r in self.rules if r.get('type') == rule_type]
    
    def update_user_state(self, key: str, value: Any):
        """
        Update user state information.
        
        Args:
            key (str): State key (e.g., 'current_topic', 'difficulty_level')
            value: State value
        """
        self.user_state[key] = value
    
    def get_user_state(self, key: str, default=None) -> Any:
        """Get user state value."""
        return self.user_state.get(key, default)
    
    def set_topic_mastery(self, topic: str, level: str):
        """
        Set mastery level for a topic.
        
        Args:
            topic (str): Topic name
            level (str): Mastery level (Not Started/Learning/Proficient/Mastered)
        """
        self.update_user_state(f'mastery_{topic}', level)
        
        # Add corresponding facts
        if level == 'Mastered':
            self.add_fact(f'mastered_{topic}')
        elif level == 'Proficient':
            self.add_fact(f'proficient_{topic}')
        elif level == 'Learning':
            self.add_fact(f'learning_{topic}')
        else:
            self.add_fact(f'not_started_{topic}')
    
    def get_topic_mastery(self, topic: str) -> str:
        """Get mastery level for a topic."""
        return self.get_user_state(f'mastery_{topic}', 'Not Started')
    
    def get_mastered_topics(self) -> List[str]:
        """Get list of all mastered topics."""
        mastered = []
        for fact in self.facts:
            if fact.startswith('mastered_'):
                topic = fact.replace('mastered_', '')
                mastered.append(topic)
        return mastered
    
    def get_struggling_topics(self) -> List[str]:
        """Get list of topics where student is struggling."""
        struggling = []
        for fact in self.facts:
            if fact.startswith('struggling_'):
                topic = fact.replace('struggling_', '')
                struggling.append(topic)
        return struggling
    
    def check_conditions(self, conditions: List[str]) -> bool:
        """
        Check if all conditions in a list are satisfied.
        
        Args:
            conditions (list): List of condition strings
            
        Returns:
            bool: True if all conditions are met
        """
        for condition in conditions:
            # Handle if condition is a list (nested conditions)
            if isinstance(condition, list):
                # Check nested conditions recursively
                if not self.check_conditions(condition):
                    return False
                continue
            
            # Ensure condition is a string
            if not isinstance(condition, str):
                continue
                
            # Handle negation
            if condition.startswith('not_'):
                # Check if the positive fact does NOT exist
                positive_fact = condition[4:]  # Remove 'not_' prefix
                if positive_fact in self.facts:
                    return False
            else:
                # Check if fact exists
                if condition not in self.facts:
                    return False
        
        return True
    
    def query(self, query_str: str) -> bool:
        """
        Query the knowledge base.
        
        Args:
            query_str (str): Query string
            
        Returns:
            bool: Query result
        """
        # Simple query: check if fact exists
        return self.has_fact(query_str)
    
    def get_all_facts(self) -> Set[str]:
        """Get all current facts."""
        return self.facts.copy()
    
    def clear_facts(self):
        """Clear all facts (useful for new session)."""
        self.facts.clear()
    
    def save_state(self, filepath: str):
        """Save knowledge base state to file."""
        state = {
            'facts': list(self.facts),
            'user_state': self.user_state
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=4)
        
        print(f"✓ Knowledge base state saved to {filepath}")
    
    def load_state(self, filepath: str):
        """Load knowledge base state from file."""
        if not os.path.exists(filepath):
            print(f"⚠ State file not found: {filepath}")
            return
        
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.facts = set(state.get('facts', []))
        self.user_state = state.get('user_state', {})
        
        print(f"✓ Knowledge base state loaded from {filepath}")
    
    def __repr__(self):
        return f"<KnowledgeBase: {len(self.facts)} facts, {len(self.rules)} rules>"
