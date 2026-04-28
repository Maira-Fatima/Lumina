"""
Inference Engine Module - Implements forward and backward chaining reasoning

This module provides advanced reasoning capabilities:
- Forward chaining: Data-driven reasoning (facts → conclusions)
- Backward chaining: Goal-driven reasoning (goal → required facts)
- Conflict resolution strategies
- Confidence-based reasoning
"""

from typing import List, Dict, Set, Tuple, Optional
from .knowledge_base import KnowledgeBase


class InferenceEngine:
    """
    Reasoning engine that applies rules to derive new knowledge.
    
    Implements:
    - Forward Chaining: Apply rules to derive new facts until no more can be inferred
    - Backward Chaining: Work backwards from goal to find required facts
    - Conflict Resolution: Priority and confidence-based rule selection
    """
    
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialize the inference engine.
        
        Args:
            knowledge_base (KnowledgeBase): Knowledge base to reason over
        """
        self.kb = knowledge_base
        self.inference_trace: List[str] = []  # Track reasoning steps
        self.max_iterations = 100  # Prevent infinite loops
    
    def forward_chain(self, max_depth: int = 10) -> List[str]:
        """
        Forward chaining: Apply rules until no new facts can be derived.
        
        Data-driven reasoning:
        1. Check all rules
        2. If rule conditions are satisfied, apply actions
        3. Repeat until no new facts are derived
        
        Args:
            max_depth (int): Maximum inference depth
            
        Returns:
            list: Newly derived facts
        """
        self.inference_trace = []
        new_facts = []
        iterations = 0
        
        while iterations < max_depth:
            facts_added_this_iteration = False
            
            # Sort rules by priority (higher priority first)
            sorted_rules = sorted(
                self.kb.rules,
                key=lambda r: r.get('priority', 0),
                reverse=True
            )
            
            for rule in sorted_rules:
                if self._can_apply_rule(rule):
                    # Apply rule actions
                    applied_facts = self._apply_rule(rule)
                    
                    if applied_facts:
                        new_facts.extend(applied_facts)
                        facts_added_this_iteration = True
                        
                        # Record inference step
                        self.inference_trace.append(
                            f"Applied rule '{rule.get('name', rule.get('id'))}' "
                            f"→ Added facts: {applied_facts}"
                        )
            
            # Stop if no new facts were derived
            if not facts_added_this_iteration:
                break
            
            iterations += 1
        
        return new_facts
    
    def backward_chain(self, goal: str) -> Tuple[bool, List[str]]:
        """
        Backward chaining: Work backwards from goal to determine if it can be proven.
        
        Goal-driven reasoning:
        1. Check if goal is already a fact
        2. Find rules that can derive the goal
        3. Recursively check if rule conditions can be satisfied
        
        Args:
            goal (str): Goal fact to prove
            
        Returns:
            tuple: (is_provable, required_facts)
        """
        self.inference_trace = []
        visited = set()
        
        is_provable, required = self._backward_chain_recursive(goal, visited)
        
        return is_provable, required
    
    def _backward_chain_recursive(
        self,
        goal: str,
        visited: Set[str],
        depth: int = 0
    ) -> Tuple[bool, List[str]]:
        """
        Recursive backward chaining helper.
        
        Args:
            goal (str): Current goal to prove
            visited (set): Already visited goals (prevent cycles)
            depth (int): Current recursion depth
            
        Returns:
            tuple: (is_provable, required_facts)
        """
        # Prevent infinite recursion
        if depth > 10 or goal in visited:
            return False, []
        
        visited.add(goal)
        
        # Base case: goal is already a fact
        if self.kb.has_fact(goal):
            self.inference_trace.append(f"✓ Goal '{goal}' is already a fact")
            return True, []
        
        # Find rules that can derive this goal
        applicable_rules = self._find_rules_with_action(goal)
        
        if not applicable_rules:
            self.inference_trace.append(f"✗ No rules can derive '{goal}'")
            return False, []
        
        # Try each applicable rule
        for rule in applicable_rules:
            conditions = rule.get('conditions', [])
            all_conditions_met = True
            required_facts = []
            
            # Check if all conditions can be satisfied
            for condition in conditions:
                # Handle negation
                if condition.startswith('not_'):
                    positive_fact = condition[4:]
                    if self.kb.has_fact(positive_fact):
                        all_conditions_met = False
                        break
                else:
                    # Check if condition is a fact or can be derived
                    if not self.kb.has_fact(condition):
                        # Try to derive this condition
                        can_derive, sub_required = self._backward_chain_recursive(
                            condition,
                            visited.copy(),
                            depth + 1
                        )
                        
                        if can_derive:
                            required_facts.extend(sub_required)
                        else:
                            required_facts.append(condition)
                            all_conditions_met = False
            
            if all_conditions_met or required_facts:
                rule_name = rule.get('name', rule.get('id'))
                self.inference_trace.append(
                    f"Rule '{rule_name}' can derive '{goal}' "
                    f"if conditions met: {conditions}"
                )
                return True, list(set(required_facts))
        
        return False, []
    
    def _can_apply_rule(self, rule: Dict) -> bool:
        """
        Check if a rule's conditions are satisfied.
        
        Args:
            rule (dict): Rule to check
            
        Returns:
            bool: True if rule can be applied
        """
        conditions = rule.get('conditions', [])
        return self.kb.check_conditions(conditions)
    
    def _apply_rule(self, rule: Dict) -> List[str]:
        """
        Apply a rule by executing its actions.
        
        Args:
            rule (dict): Rule to apply
            
        Returns:
            list: New facts added
        """
        actions = rule.get('actions', [])
        new_facts = []
        
        for action in actions:
            # Parse action
            if action.startswith('add_fact_'):
                fact = action.replace('add_fact_', '')
                if not self.kb.has_fact(fact):
                    self.kb.add_fact(fact)
                    new_facts.append(fact)
            elif action.startswith('recommend_'):
                # Add recommendation as a fact
                recommendation = action
                if not self.kb.has_fact(recommendation):
                    self.kb.add_fact(recommendation)
                    new_facts.append(recommendation)
            else:
                # Generic action: add as fact
                if not self.kb.has_fact(action):
                    self.kb.add_fact(action)
                    new_facts.append(action)
        
        return new_facts
    
    def _find_rules_with_action(self, action: str) -> List[Dict]:
        """
        Find all rules that have a specific action.
        
        Args:
            action (str): Action to search for
            
        Returns:
            list: Rules that can produce this action
        """
        matching_rules = []
        
        for rule in self.kb.rules:
            actions = rule.get('actions', [])
            
            # Check if action matches
            if action in actions or f'add_fact_{action}' in actions:
                matching_rules.append(rule)
        
        return matching_rules
    
    def explain_reasoning(self, conclusion: str) -> str:
        """
        Explain how a conclusion was reached.
        
        Args:
            conclusion (str): Fact to explain
            
        Returns:
            str: Explanation of reasoning chain
        """
        # Try backward chaining to find reasoning path
        is_provable, required = self.backward_chain(conclusion)
        
        explanation = f"Reasoning for '{conclusion}':\n\n"
        
        if is_provable:
            explanation += "✓ This conclusion can be derived.\n\n"
            explanation += "Reasoning trace:\n"
            for step in self.inference_trace:
                explanation += f"  {step}\n"
            
            if required:
                explanation += f"\nRequired facts: {required}"
        else:
            explanation += "✗ This conclusion cannot be derived from current knowledge.\n\n"
            explanation += "Missing information:\n"
            for step in self.inference_trace:
                explanation += f"  {step}\n"
        
        return explanation
    
    def resolve_conflicts(self, applicable_rules: List[Dict]) -> Dict:
        """
        Resolve conflicts when multiple rules are applicable.
        
        Conflict resolution strategies:
        1. Priority: Higher priority rules fire first
        2. Confidence: Higher confidence rules preferred
        3. Specificity: More specific rules (more conditions) preferred
        
        Args:
            applicable_rules (list): List of applicable rules
            
        Returns:
            dict: Selected rule
        """
        if not applicable_rules:
            return None
        
        # Sort by priority, then confidence, then specificity
        sorted_rules = sorted(
            applicable_rules,
            key=lambda r: (
                r.get('priority', 0),
                r.get('confidence', 0.5),
                len(r.get('conditions', []))
            ),
            reverse=True
        )
        
        return sorted_rules[0]
    
    def get_recommendations(self, context: Dict = None) -> List[Dict]:
        """
        Generate recommendations based on current knowledge state.
        
        Args:
            context (dict): Additional context for recommendations
            
        Returns:
            list: Recommended actions with confidence scores
        """
        recommendations = []
        
        # Apply forward chaining to derive recommendations
        self.forward_chain(max_depth=5)
        
        # Extract recommendation facts
        for fact in self.kb.get_all_facts():
            if fact.startswith('recommend_'):
                topic = fact.replace('recommend_', '')
                
                # Find the rule that generated this recommendation
                confidence = 0.7  # Default confidence
                reason = "Based on your progress"
                
                for rule in self.kb.rules:
                    if fact in rule.get('actions', []):
                        confidence = rule.get('confidence', 0.7)
                        reason = rule.get('reason', reason)
                        break
                
                recommendations.append({
                    'topic': topic,
                    'confidence': confidence,
                    'reason': reason
                })
        
        # Sort by confidence
        recommendations.sort(key=lambda r: r['confidence'], reverse=True)
        
        return recommendations
    
    def get_inference_trace(self) -> List[str]:
        """Get the reasoning trace from last inference."""
        return self.inference_trace.copy()
    
    def clear_trace(self):
        """Clear the inference trace."""
        self.inference_trace = []
