"""
Expert System Module for Lumina AI Study Companion

This module implements an advanced rule-based expert system with:
- Knowledge base with facts and rules
- Inference engine (forward and backward chaining)
- Prerequisite dependency tracking
- Personalized learning path generation
"""

from .knowledge_base import KnowledgeBase
from .inference_engine import InferenceEngine
from .rule_manager import RuleManager
from .prerequisite_graph import PrerequisiteGraph

__all__ = [
    'KnowledgeBase',
    'InferenceEngine',
    'RuleManager',
    'PrerequisiteGraph'
]
