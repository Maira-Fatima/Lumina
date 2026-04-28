"""
Rule Manager Module - Creates and manages expert system rules

This module generates comprehensive rules for:
- Prerequisite checking
- Learning recommendations
- Difficulty adaptation
- Performance-based guidance
"""

import json
import os
from typing import List, Dict


class RuleManager:
    """
    Manages creation and organization of expert system rules.
    
    Generates rules for:
    - Prerequisite validation
    - Topic recommendations based on mastery
    - Difficulty adjustment
    - Struggle detection and support
    """
    
    def __init__(self, rules_dir='expert_system/rules'):
        """
        Initialize the rule manager.
        
        Args:
            rules_dir (str): Directory to store rule files
        """
        self.rules_dir = rules_dir
        os.makedirs(rules_dir, exist_ok=True)
    
    def generate_all_rules(self):
        """Generate all rule files."""
        print("Generating expert system rules...")
        
        self.generate_prerequisite_rules()
        self.generate_learning_path_rules()
        self.generate_recommendation_rules()
        
        print("✓ All rules generated successfully")
    
    def generate_prerequisite_rules(self):
        """Generate prerequisite checking rules."""
        rules = {
            "rules": [
                # Basic prerequisite rules
                {
                    "id": "prereq_1",
                    "type": "prerequisite",
                    "name": "Check Python before ML",
                    "conditions": ["not_mastered_Python Basics", "attempting_Introduction to ML"],
                    "actions": ["recommend_Python Basics"],
                    "confidence": 0.95,
                    "priority": 10,
                    "reason": "Python is essential for Machine Learning"
                },
                {
                    "id": "prereq_2",
                    "type": "prerequisite",
                    "name": "Check Linear Algebra before Neural Networks",
                    "conditions": ["not_mastered_Linear Algebra", "attempting_Neural Networks"],
                    "actions": ["recommend_Linear Algebra"],
                    "confidence": 0.95,
                    "priority": 10,
                    "reason": "Linear Algebra is fundamental for Neural Networks"
                },
                {
                    "id": "prereq_3",
                    "type": "prerequisite",
                    "name": "Check Calculus before Neural Networks",
                    "conditions": ["not_mastered_Calculus", "attempting_Neural Networks"],
                    "actions": ["recommend_Calculus"],
                    "confidence": 0.95,
                    "priority": 10,
                    "reason": "Calculus is needed for backpropagation"
                },
                {
                    "id": "prereq_4",
                    "type": "prerequisite",
                    "name": "Check BFS before A*",
                    "conditions": ["not_mastered_BFS", "attempting_A* Search"],
                    "actions": ["recommend_BFS"],
                    "confidence": 0.9,
                    "priority": 9,
                    "reason": "Understanding BFS helps with A* algorithm"
                },
                {
                    "id": "prereq_5",
                    "type": "prerequisite",
                    "name": "Check supervised learning before deep learning",
                    "conditions": ["not_mastered_Supervised Learning", "attempting_Neural Networks"],
                    "actions": ["recommend_Supervised Learning"],
                    "confidence": 0.9,
                    "priority": 9,
                    "reason": "Basic ML concepts are needed before deep learning"
                },
                # Advanced prerequisite chains
                {
                    "id": "prereq_6",
                    "type": "prerequisite",
                    "name": "Check RNN before LSTM",
                    "conditions": ["not_mastered_RNN", "attempting_LSTM"],
                    "actions": ["recommend_RNN"],
                    "confidence": 0.95,
                    "priority": 10,
                    "reason": "LSTM is an advanced RNN architecture"
                },
                {
                    "id": "prereq_7",
                    "type": "prerequisite",
                    "name": "Check CNN before object detection",
                    "conditions": ["not_mastered_CNN", "attempting_Object Detection"],
                    "actions": ["recommend_CNN"],
                    "confidence": 0.95,
                    "priority": 10,
                    "reason": "Object detection builds on CNN knowledge"
                },
                {
                    "id": "prereq_8",
                    "type": "prerequisite",
                    "name": "Check transformers before BERT",
                    "conditions": ["not_mastered_Transformers", "attempting_BERT"],
                    "actions": ["recommend_Transformers"],
                    "confidence": 0.95,
                    "priority": 10,
                    "reason": "BERT is based on transformer architecture"
                }
            ]
        }
        
        filepath = os.path.join(self.rules_dir, 'prerequisites.json')
        with open(filepath, 'w') as f:
            json.dump(rules, f, indent=4)
        
        print(f"✓ Created {len(rules['rules'])} prerequisite rules")
    
    def generate_learning_path_rules(self):
        """Generate learning path structures."""
        paths = {
            "paths": {
                "Machine Learning Beginner": [
                    "Python Basics",
                    "Mathematics Basics",
                    "Statistics",
                    "Introduction to ML",
                    "Supervised Learning",
                    "Linear Regression",
                    "Logistic Regression",
                    "Decision Trees"
                ],
                "Machine Learning Intermediate": [
                    "Random Forest",
                    "SVM",
                    "KNN",
                    "Naive Bayes",
                    "Unsupervised Learning",
                    "K-Means",
                    "PCA"
                ],
                "Deep Learning Path": [
                    "Linear Algebra",
                    "Calculus",
                    "Supervised Learning",
                    "Neural Networks",
                    "Backpropagation",
                    "CNN",
                    "RNN",
                    "LSTM",
                    "Transformers"
                ],
                "NLP Specialist": [
                    "Text Preprocessing",
                    "Tokenization",
                    "Neural Networks",
                    "Word Embeddings",
                    "Word2Vec",
                    "RNN",
                    "LSTM",
                    "Transformers",
                    "BERT",
                    "GPT"
                ],
                "Computer Vision Path": [
                    "Linear Algebra",
                    "Image Processing",
                    "CNN",
                    "Image Classification",
                    "Object Detection",
                    "YOLO",
                    "R-CNN",
                    "Image Segmentation"
                ],
                "Reinforcement Learning Path": [
                    "Probability",
                    "Python Basics",
                    "RL Fundamentals",
                    "MDP",
                    "Q-Learning",
                    "SARSA",
                    "Policy Gradients",
                    "Actor-Critic",
                    "DQN"
                ],
                "AI Foundations": [
                    "Python Basics",
                    "Mathematics Basics",
                    "Arrays",
                    "Graphs",
                    "BFS",
                    "DFS",
                    "A* Search",
                    "Knowledge Representation",
                    "Inference Rules"
                ]
            },
            "path_metadata": {
                "Machine Learning Beginner": {
                    "description": "Start your ML journey with foundational concepts",
                    "estimated_weeks": 8,
                    "difficulty": "Beginner"
                },
                "Deep Learning Path": {
                    "description": "Master neural networks and modern deep learning",
                    "estimated_weeks": 16,
                    "difficulty": "Advanced"
                },
                "NLP Specialist": {
                    "description": "Become an expert in natural language processing",
                    "estimated_weeks": 14,
                    "difficulty": "Advanced"
                },
                "Computer Vision Path": {
                    "description": "Learn image processing and computer vision",
                    "estimated_weeks": 12,
                    "difficulty": "Advanced"
                }
            }
        }
        
        filepath = os.path.join(self.rules_dir, 'learning_paths.json')
        with open(filepath, 'w') as f:
            json.dump(paths, f, indent=4)
        
        print(f"✓ Created {len(paths['paths'])} learning paths")
    
    def generate_recommendation_rules(self):
        """Generate recommendation rules."""
        rules = {
            "rules": [
                # Progression rules
                {
                    "id": "rec_1",
                    "type": "recommendation",
                    "name": "Recommend DFS after BFS mastery",
                    "conditions": ["mastered_BFS", "not_mastered_DFS"],
                    "actions": ["recommend_DFS"],
                    "confidence": 0.9,
                    "priority": 8,
                    "reason": "DFS is a natural next step after mastering BFS"
                },
                {
                    "id": "rec_2",
                    "type": "recommendation",
                    "name": "Recommend advanced search after basics",
                    "conditions": ["mastered_BFS", "mastered_DFS", "not_mastered_A* Search"],
                    "actions": ["recommend_A* Search"],
                    "confidence": 0.85,
                    "priority": 7,
                    "reason": "Ready for advanced search algorithms"
                },
                {
                    "id": "rec_3",
                    "type": "recommendation",
                    "name": "Recommend Neural Networks after ML basics",
                    "conditions": [
                        "mastered_Supervised Learning",
                        "mastered_Linear Algebra",
                        "mastered_Calculus",
                        "not_mastered_Neural Networks"
                    ],
                    "actions": ["recommend_Neural Networks"],
                    "confidence": 0.9,
                    "priority": 8,
                    "reason": "All prerequisites met for deep learning"
                },
                {
                    "id": "rec_4",
                    "type": "recommendation",
                    "name": "Recommend CNN after Neural Networks",
                    "conditions": ["mastered_Neural Networks", "not_mastered_CNN"],
                    "actions": ["recommend_CNN"],
                    "confidence": 0.9,
                    "priority": 8,
                    "reason": "CNN is the next step in deep learning"
                },
                # Struggle support rules
                {
                    "id": "rec_5",
                    "type": "recommendation",
                    "name": "Review basics when struggling",
                    "conditions": ["struggling_Neural Networks", "proficient_Supervised Learning"],
                    "actions": ["recommend_review_Linear Algebra", "recommend_review_Calculus"],
                    "confidence": 0.8,
                    "priority": 9,
                    "reason": "Reviewing math fundamentals may help"
                },
                {
                    "id": "rec_6",
                    "type": "recommendation",
                    "name": "Provide easier alternatives",
                    "conditions": ["struggling_A* Search", "mastered_BFS"],
                    "actions": ["recommend_practice_BFS", "recommend_Dijkstra's Algorithm"],
                    "confidence": 0.75,
                    "priority": 7,
                    "reason": "Build confidence with intermediate topics"
                },
                # Advanced recommendations
                {
                    "id": "rec_7",
                    "type": "recommendation",
                    "name": "Recommend specialization",
                    "conditions": [
                        "mastered_Neural Networks",
                        "mastered_CNN",
                        "mastered_RNN"
                    ],
                    "actions": ["recommend_choose_specialization"],
                    "confidence": 0.8,
                    "priority": 6,
                    "reason": "Ready to specialize in NLP, CV, or RL"
                },
                {
                    "id": "rec_8",
                    "type": "recommendation",
                    "name": "Recommend Transformers",
                    "conditions": [
                        "mastered_LSTM",
                        "mastered_Attention Mechanism",
                        "not_mastered_Transformers"
                    ],
                    "actions": ["recommend_Transformers"],
                    "confidence": 0.9,
                    "priority": 8,
                    "reason": "Ready for state-of-the-art architectures"
                },
                # Practice recommendations
                {
                    "id": "rec_9",
                    "type": "recommendation",
                    "name": "Suggest practice after theory",
                    "conditions": ["proficient_Decision Trees", "low_practice_count"],
                    "actions": ["recommend_practice_problems"],
                    "confidence": 0.85,
                    "priority": 7,
                    "reason": "Practice reinforces theoretical knowledge"
                },
                {
                    "id": "rec_10",
                    "type": "recommendation",
                    "name": "Recommend projects",
                    "conditions": ["mastered_CNN", "mastered_RNN", "no_projects"],
                    "actions": ["recommend_build_project"],
                    "confidence": 0.8,
                    "priority": 6,
                    "reason": "Projects solidify learning"
                }
            ]
        }
        
        filepath = os.path.join(self.rules_dir, 'recommendations.json')
        with open(filepath, 'w') as f:
            json.dump(rules, f, indent=4)
        
        print(f"✓ Created {len(rules['rules'])} recommendation rules")
    
    def add_custom_rule(self, rule: Dict, rule_type: str = 'recommendations'):
        """
        Add a custom rule to the system.
        
        Args:
            rule (dict): Rule definition
            rule_type (str): Type of rule file to add to
        """
        filepath = os.path.join(self.rules_dir, f'{rule_type}.json')
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
        else:
            data = {"rules": []}
        
        data["rules"].append(rule)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"✓ Added custom rule to {rule_type}")


def initialize_expert_system():
    """Initialize the expert system with default rules."""
    rule_manager = RuleManager()
    rule_manager.generate_all_rules()
    print("✓ Expert system initialized")


if __name__ == "__main__":
    initialize_expert_system()
