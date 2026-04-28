"""
Comprehensive integration test for the Lumina AI Study Companion
Tests all major components and identifies any bugs or errors
"""

import sys
import os

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_imports():
    """Test all critical imports"""
    print("=" * 60)
    print("Testing Imports...")
    print("=" * 60)
    
    try:
        from core.data_loader import get_expanded_knowledge_base, download_nltk_data
        print("✓ core.data_loader")
    except Exception as e:
        print(f"✗ core.data_loader: {e}")
        return False
    
    try:
        from core.engine import QueryMatchingEngine
        print("✓ core.engine")
    except Exception as e:
        print(f"✗ core.engine: {e}")
        return False
    
    try:
        from core.topic_graph import build_topic_graph, SearchNavigationModule
        print("✓ core.topic_graph")
    except Exception as e:
        print(f"✗ core.topic_graph: {e}")
        return False
    
    try:
        from core.ai_companion import AIStudyCompanion
        print("✓ core.ai_companion")
    except Exception as e:
        print(f"✗ core.ai_companion: {e}")
        return False
    
    try:
        from ml_module.classifier import TopicClassifier, DifficultyClassifier
        print("✓ ml_module.classifier")
    except Exception as e:
        print(f"✗ ml_module.classifier: {e}")
        return False
    
    try:
        from expert_system.knowledge_base import KnowledgeBase
        from expert_system.inference_engine import InferenceEngine
        print("✓ expert_system")
    except Exception as e:
        print(f"✗ expert_system: {e}")
        return False
    
    try:
        from adaptive_learning.state_manager import StateManager
        from adaptive_learning.difficulty_manager import DifficultyManager
        print("✓ adaptive_learning")
    except Exception as e:
        print(f"✗ adaptive_learning: {e}")
        return False
    
    try:
        from backend.helper import get_ai_response, get_user_stats
        print("✓ backend.helper")
    except Exception as e:
        print(f"✗ backend.helper: {e}")
        return False
    
    print("\n✓ All imports successful!\n")
    return True


def test_knowledge_base():
    """Test knowledge base loading"""
    print("=" * 60)
    print("Testing Knowledge Base...")
    print("=" * 60)
    
    try:
        from core.data_loader import get_expanded_knowledge_base
        kb = get_expanded_knowledge_base()
        
        if not kb:
            print("✗ Knowledge base is empty")
            return False
        
        print(f"✓ Knowledge base loaded: {len(kb)} entries")
        
        # Check structure
        if not isinstance(kb, list):
            print(f"✗ Knowledge base should be a list, got {type(kb)}")
            return False
        
        # Check first entry structure
        if kb:
            first_entry = kb[0]
            required_keys = ['question', 'answer', 'topic']
            missing_keys = [key for key in required_keys if key not in first_entry]
            if missing_keys:
                print(f"✗ Missing keys in entries: {missing_keys}")
                return False
            print(f"✓ Entry structure valid")
        
        # Count topics
        topics = set(entry.get('topic', 'Unknown') for entry in kb)
        print(f"✓ Topics covered: {len(topics)}")
        print(f"  Sample topics: {list(topics)[:5]}")
        
        return True
        
    except Exception as e:
        print(f"✗ Knowledge base test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_query_engine():
    """Test query matching engine"""
    print("\n" + "=" * 60)
    print("Testing Query Matching Engine...")
    print("=" * 60)
    
    try:
        from core.data_loader import get_expanded_knowledge_base
        from core.engine import QueryMatchingEngine
        
        kb = get_expanded_knowledge_base()
        engine = QueryMatchingEngine(kb)
        engine.fit()
        print("✓ Engine initialized and fitted")
        
        # Test queries
        test_queries = [
            "What is machine learning?",
            "BFS algorithm",
            "polymorphism in OOP",
            "neural networks"
        ]
        
        for query in test_queries:
            result = engine.find_match(query)
            similarity = result.get('similarity', 0)
            answer = result.get('answer', '')
            
            if similarity > 0:
                print(f"✓ Query: '{query}' -> Similarity: {similarity:.2f}")
            else:
                print(f"⚠ Query: '{query}' -> No match (similarity: {similarity:.2f})")
        
        return True
        
    except Exception as e:
        print(f"✗ Query engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ml_models():
    """Test ML model loading"""
    print("\n" + "=" * 60)
    print("Testing ML Models...")
    print("=" * 60)
    
    try:
        from ml_module.classifier import TopicClassifier, DifficultyClassifier
        
        tc = TopicClassifier()
        dc = DifficultyClassifier()
        print("✓ Classifiers instantiated")
        
        # Try to load models
        try:
            tc.load_model('ml_module/models/topic_classifier.pkl')
            print("✓ Topic classifier loaded")
        except:
            print("⚠ Topic classifier model not found (will use fallback)")
        
        try:
            dc.load_model('ml_module/models/difficulty_classifier.pkl')
            print("✓ Difficulty classifier loaded")
        except:
            print("⚠ Difficulty classifier model not found (will use fallback)")
        
        return True
        
    except Exception as e:
        print(f"✗ ML models test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_expert_system():
    """Test expert system"""
    print("\n" + "=" * 60)
    print("Testing Expert System...")
    print("=" * 60)
    
    try:
        from expert_system.knowledge_base import KnowledgeBase
        from expert_system.inference_engine import InferenceEngine
        from expert_system.prerequisite_graph import PrerequisiteGraph
        
        kb = KnowledgeBase()
        print("✓ Knowledge base initialized")
        
        ie = InferenceEngine(kb)
        print("✓ Inference engine initialized")
        
        pg = PrerequisiteGraph()
        print("✓ Prerequisite graph initialized")
        
        # Test prerequisite query
        prereqs = pg.get_all_prerequisites("Deep Learning")
        print(f"✓ Prerequisites for Deep Learning: {prereqs}")
        
        return True
        
    except Exception as e:
        print(f"✗ Expert system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_adaptive_learning():
    """Test adaptive learning module"""
    print("\n" + "=" * 60)
    print("Testing Adaptive Learning...")
    print("=" * 60)
    
    try:
        from adaptive_learning.state_manager import StateManager
        from adaptive_learning.difficulty_manager import DifficultyManager
        from adaptive_learning.recommendation_engine import RecommendationEngine
        
        sm = StateManager()
        print("✓ State manager initialized")
        
        # Test load_user method
        result = sm.load_user("test_user")
        if result:
            print("✓ load_user method works")
        else:
            print("⚠ load_user returned False")
        
        dm = DifficultyManager(sm)
        print("✓ Difficulty manager initialized")
        
        re = RecommendationEngine(sm)
        print("✓ Recommendation engine initialized")
        
        # Test basic functionality
        sm.set_topic_mastery("Python", "Learning")
        mastery = sm.get_topic_mastery("Python")
        print(f"✓ Topic mastery tracking works: Python = {mastery}%")
        
        return True
        
    except Exception as e:
        print(f"✗ Adaptive learning test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_backend_helper():
    """Test backend helper functions"""
    print("\n" + "=" * 60)
    print("Testing Backend Helper...")
    print("=" * 60)
    
    try:
        from backend.helper import get_ai_response
        
        # Test a simple query
        print("Testing get_ai_response with: 'What is Python?'")
        response, context, metadata = get_ai_response(
            "What is Python?",
            "General",
            user_id="test_user",
            record_performance=False
        )
        
        if response and len(response) > 0:
            print(f"✓ Got response: {response[:100]}...")
            print(f"✓ Context: {context}")
            print(f"✓ Metadata: {list(metadata.keys())}")
            return True
        else:
            print("✗ Empty response received")
            return False
        
    except Exception as e:
        print(f"✗ Backend helper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_companion():
    """Test full AI companion integration"""
    print("\n" + "=" * 60)
    print("Testing AI Companion Integration...")
    print("=" * 60)
    
    try:
        from core.data_loader import get_expanded_knowledge_base
        from core.topic_graph import build_topic_graph
        from core.ai_companion import AIStudyCompanion
        
        kb = get_expanded_knowledge_base()
        topic_graph = build_topic_graph(kb)
        companion = AIStudyCompanion(kb, topic_graph)
        print("✓ AI Companion instantiated")
        
        # Test ask method
        test_queries = [
            "What is machine learning?",
            "Explain BFS algorithm",
            "What is polymorphism?"
        ]
        
        for query in test_queries:
            result = companion.ask(query, user_id="test_user", record_performance=False)
            
            if result and 'answer' in result:
                answer = result['answer']
                topic = result.get('topic', 'Unknown')
                print(f"✓ Query: '{query[:30]}...' -> Topic: {topic}")
            else:
                print(f"⚠ Query: '{query[:30]}...' -> No result")
        
        return True
        
    except Exception as e:
        print(f"✗ AI Companion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("LUMINA INTEGRATION TEST SUITE")
    print("=" * 60 + "\n")
    
    results = {
        "Imports": test_imports(),
        "Knowledge Base": test_knowledge_base(),
        "Query Engine": test_query_engine(),
        "ML Models": test_ml_models(),
        "Expert System": test_expert_system(),
        "Adaptive Learning": test_adaptive_learning(),
        "Backend Helper": test_backend_helper(),
        "AI Companion": test_ai_companion()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! No bugs found.")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
