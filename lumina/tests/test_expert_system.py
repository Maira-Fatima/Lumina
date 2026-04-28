"""
Test Suite for Expert System Module

Tests cover:
- Knowledge Base operations
- Inference Engine (forward/backward chaining)
- Prerequisite Graph
- Rule Management
"""

import pytest
from expert_system.knowledge_base import KnowledgeBase
from expert_system.inference_engine import InferenceEngine
from expert_system.prerequisite_graph import PrerequisiteGraph
from expert_system.rule_manager import RuleManager


class TestKnowledgeBase:
    """Tests for KnowledgeBase"""
    
    def test_initialization(self):
        """Test knowledge base initialization"""
        kb = KnowledgeBase()
        assert kb.facts == set()
        assert kb.rules == []
    
    def test_add_fact(self):
        """Test adding facts"""
        kb = KnowledgeBase()
        kb.add_fact("Python", "mastery", 80)
        
        assert kb.has_fact("Python", "mastery")
        assert kb.get_fact_value("Python", "mastery") == 80
    
    def test_remove_fact(self):
        """Test removing facts"""
        kb = KnowledgeBase()
        kb.add_fact("Python", "mastery", 80)
        kb.remove_fact("Python", "mastery")
        
        assert not kb.has_fact("Python", "mastery")
    
    def test_topic_mastery(self):
        """Test topic mastery management"""
        kb = KnowledgeBase()
        kb.set_topic_mastery("Python", 85)
        
        assert kb.get_topic_mastery("Python") == 85
    
    def test_add_rule(self):
        """Test adding rules"""
        kb = KnowledgeBase()
        
        rule = {
            'name': 'test_rule',
            'conditions': [('Python', 'mastery', '>', 70)],
            'actions': [('recommend', 'Advanced Python')]
        }
        
        kb.add_rule(rule)
        assert len(kb.rules) == 1
    
    def test_check_conditions(self):
        """Test condition checking"""
        kb = KnowledgeBase()
        kb.add_fact("Python", "mastery", 80)
        
        conditions = [('Python', 'mastery', '>', 70)]
        assert kb.check_conditions(conditions) == True
        
        conditions = [('Python', 'mastery', '>', 90)]
        assert kb.check_conditions(conditions) == False
    
    def test_save_load_state(self, tmp_path):
        """Test state persistence"""
        kb = KnowledgeBase()
        kb.set_topic_mastery("Python", 85)
        kb.set_topic_mastery("Java", 70)
        
        # Save
        state_file = tmp_path / "kb_state.json"
        kb.save_state(str(state_file))
        
        # Load
        new_kb = KnowledgeBase()
        new_kb.load_state(str(state_file))
        
        assert new_kb.get_topic_mastery("Python") == 85
        assert new_kb.get_topic_mastery("Java") == 70


class TestInferenceEngine:
    """Tests for InferenceEngine"""
    
    def test_initialization(self):
        """Test inference engine initialization"""
        kb = KnowledgeBase()
        engine = InferenceEngine(kb)
        assert engine.kb is not None
    
    def test_forward_chaining_simple(self):
        """Test simple forward chaining"""
        kb = KnowledgeBase()
        kb.set_topic_mastery("Python", 80)
        
        rule = {
            'name': 'recommend_advanced',
            'conditions': [('Python', 'mastery', '>', 70)],
            'actions': [('recommend', 'Advanced Python')],
            'priority': 1,
            'confidence': 0.9
        }
        kb.add_rule(rule)
        
        engine = InferenceEngine(kb)
        inferred = engine.forward_chain()
        
        assert len(inferred) > 0
    
    def test_backward_chaining(self):
        """Test backward chaining"""
        kb = KnowledgeBase()
        kb.set_topic_mastery("Python", 80)
        
        rule = {
            'name': 'can_learn_django',
            'conditions': [('Python', 'mastery', '>', 70)],
            'actions': [('can_learn', 'Django')],
            'priority': 1,
            'confidence': 0.9
        }
        kb.add_rule(rule)
        
        engine = InferenceEngine(kb)
        goal = ('can_learn', 'Django')
        result, trace = engine.backward_chain(goal)
        
        assert isinstance(result, bool)
        assert isinstance(trace, list)
    
    def test_get_recommendations(self):
        """Test recommendation generation"""
        kb = KnowledgeBase()
        kb.set_topic_mastery("Python", 85)
        
        engine = InferenceEngine(kb)
        recommendations = engine.get_recommendations()
        
        assert isinstance(recommendations, list)
    
    def test_explain_reasoning(self):
        """Test reasoning explanation"""
        kb = KnowledgeBase()
        kb.set_topic_mastery("Python", 80)
        
        rule = {
            'name': 'test_rule',
            'conditions': [('Python', 'mastery', '>', 70)],
            'actions': [('recommend', 'Advanced Python')],
            'priority': 1,
            'confidence': 0.9
        }
        kb.add_rule(rule)
        
        engine = InferenceEngine(kb)
        engine.forward_chain()
        
        explanation = engine.explain_reasoning()
        assert isinstance(explanation, str)


class TestPrerequisiteGraph:
    """Tests for PrerequisiteGraph"""
    
    def test_initialization(self):
        """Test graph initialization"""
        graph = PrerequisiteGraph()
        assert len(graph.graph) > 0  # Should have default graph
    
    def test_add_prerequisite(self):
        """Test adding prerequisites"""
        graph = PrerequisiteGraph()
        graph.add_prerequisite("Topic A", "Topic B")
        
        assert "Topic A" in graph.graph
        assert "Topic B" in graph.graph["Topic A"]
    
    def test_get_direct_prerequisites(self):
        """Test getting direct prerequisites"""
        graph = PrerequisiteGraph()
        graph.add_prerequisite("Advanced Python", "Python Basics")
        
        prereqs = graph.get_direct_prerequisites("Advanced Python")
        assert "Python Basics" in prereqs
    
    def test_get_all_prerequisites(self):
        """Test transitive closure"""
        graph = PrerequisiteGraph()
        graph.add_prerequisite("C", "B")
        graph.add_prerequisite("B", "A")
        
        all_prereqs = graph.get_all_prerequisites("C")
        assert "A" in all_prereqs
        assert "B" in all_prereqs
    
    def test_has_prerequisite(self):
        """Test prerequisite checking"""
        graph = PrerequisiteGraph()
        graph.add_prerequisite("Advanced", "Basic")
        
        assert graph.has_prerequisite("Advanced", "Basic") == True
        assert graph.has_prerequisite("Basic", "Advanced") == False
    
    def test_can_learn(self):
        """Test learning eligibility"""
        graph = PrerequisiteGraph()
        graph.add_prerequisite("Advanced", "Basic")
        
        mastered = {"Basic"}
        assert graph.can_learn("Advanced", mastered) == True
        
        mastered = set()
        assert graph.can_learn("Advanced", mastered) == False
    
    def test_generate_learning_path(self):
        """Test learning path generation"""
        graph = PrerequisiteGraph()
        graph.add_prerequisite("C", "B")
        graph.add_prerequisite("B", "A")
        
        path = graph.generate_learning_path("C", mastered_topics=set())
        
        assert len(path) > 0
        assert path[-1] == "C"  # Target topic should be last
    
    def test_get_curriculum(self):
        """Test curriculum organization"""
        graph = PrerequisiteGraph()
        curriculum = graph.get_curriculum()
        
        assert 'Beginner' in curriculum
        assert 'Intermediate' in curriculum
        assert 'Advanced' in curriculum
        assert isinstance(curriculum['Beginner'], list)
    
    def test_circular_dependency_detection(self):
        """Test that circular dependencies are handled"""
        graph = PrerequisiteGraph()
        # This should not create infinite loop
        graph.add_prerequisite("A", "B")
        graph.add_prerequisite("B", "A")
        
        # Should complete without hanging
        prereqs = graph.get_all_prerequisites("A")
        assert isinstance(prereqs, list)


class TestRuleManager:
    """Tests for RuleManager"""
    
    def test_initialization(self):
        """Test rule manager initialization"""
        manager = RuleManager()
        assert len(manager.rules) == 0
    
    def test_generate_prerequisite_rules(self):
        """Test prerequisite rule generation"""
        manager = RuleManager()
        rules = manager.generate_prerequisite_rules()
        
        assert len(rules) > 0
        for rule in rules:
            assert 'name' in rule
            assert 'conditions' in rule
            assert 'actions' in rule
    
    def test_generate_learning_path_rules(self):
        """Test learning path rule generation"""
        manager = RuleManager()
        rules = manager.generate_learning_path_rules()
        
        assert len(rules) > 0
        for rule in rules:
            assert 'name' in rule
            assert 'path' in rule
            assert 'difficulty_order' in rule
    
    def test_generate_recommendation_rules(self):
        """Test recommendation rule generation"""
        manager = RuleManager()
        rules = manager.generate_recommendation_rules()
        
        assert len(rules) > 0
        for rule in rules:
            assert 'name' in rule
            assert 'conditions' in rule
            assert 'actions' in rule
    
    def test_add_custom_rule(self):
        """Test adding custom rules"""
        manager = RuleManager()
        
        rule = {
            'name': 'custom_rule',
            'conditions': [('test', 'condition', '>', 50)],
            'actions': [('test', 'action')],
            'priority': 1,
            'confidence': 0.8
        }
        
        manager.add_custom_rule(rule)
        assert 'custom_rule' in manager.rules
    
    def test_save_rules(self, tmp_path):
        """Test saving rules to file"""
        manager = RuleManager()
        rules = manager.generate_prerequisite_rules()
        
        rules_file = tmp_path / "test_rules.json"
        manager.save_rules(rules, str(rules_file))
        
        assert rules_file.exists()


@pytest.fixture
def setup_complete_expert_system():
    """Fixture for complete expert system setup"""
    kb = KnowledgeBase()
    kb.set_topic_mastery("Python", 85)
    kb.set_topic_mastery("Java", 60)
    
    engine = InferenceEngine(kb)
    graph = PrerequisiteGraph()
    
    return kb, engine, graph


def test_end_to_end_expert_system(setup_complete_expert_system):
    """Test complete expert system workflow"""
    kb, engine, graph = setup_complete_expert_system
    
    # 1. Check prerequisites
    target_topic = "Machine Learning"
    prereqs = graph.get_all_prerequisites(target_topic)
    assert isinstance(prereqs, list)
    
    # 2. Generate learning path
    mastered = {"Python"}
    path = graph.generate_learning_path(target_topic, mastered)
    assert len(path) > 0
    
    # 3. Get recommendations
    recommendations = engine.get_recommendations()
    assert isinstance(recommendations, list)


def test_expert_system_with_rules():
    """Test expert system with actual rules"""
    kb = KnowledgeBase()
    manager = RuleManager()
    
    # Generate and load rules
    prereq_rules = manager.generate_prerequisite_rules()
    for rule in prereq_rules[:3]:  # Test with first 3 rules
        kb.add_rule(rule)
    
    # Set some facts
    kb.set_topic_mastery("Python", 80)
    
    # Run inference
    engine = InferenceEngine(kb)
    inferred = engine.forward_chain()
    
    assert isinstance(inferred, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
