"""
Test Recommendations System
Verifies that recommendations are generated correctly for different scenarios
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.helper import get_recommendations_for_user
from adaptive_learning.state_manager import StateManager

def test_recommendations():
    """Test recommendations for a user with some progress"""
    print("\n" + "="*60)
    print("TESTING RECOMMENDATIONS SYSTEM")
    print("="*60)
    
    # Test with existing user
    username = "test_rec_user"
    print(f"\n1️⃣ Testing recommendations for user: {username}")
    
    # Create state and record some performance
    state = StateManager()
    state.load_user(username)
    
    # Simulate user activity
    state.record_performance("Python Basics", "easy", "Q1", True, 10.0, 0.8)
    state.record_performance("Python Basics", "medium", "Q2", True, 15.0, 0.7)
    state.record_performance("Python Basics", "medium", "Q3", False, 12.0, 0.5)
    state.record_performance("Data Structures", "easy", "Q4", True, 20.0, 0.9)
    state.record_performance("Data Structures", "hard", "Q5", False, 25.0, 0.4)
    state.record_performance("Machine Learning", "medium", "Q6", False, 18.0, 0.3)
    state.record_performance("Machine Learning", "medium", "Q7", False, 22.0, 0.3)
    state.save_user_profile()
    
    print("\n✅ Recorded sample performance:")
    print("   - Python Basics: 2/3 (66.7%)")
    print("   - Data Structures: 1/2 (50%)")
    print("   - Machine Learning: 0/2 (0%)")
    
    # Get recommendations
    print("\n2️⃣ Getting recommendations...")
    recs = get_recommendations_for_user(username, "Python Basics")
    
    print(f"\n📊 RECOMMENDATIONS RECEIVED:")
    print(f"   Next Topics: {len(recs.get('next_topics', []))} topics")
    print(f"   Practice Topics: {len(recs.get('practice_topics', []))} topics")
    
    if recs.get('next_topics'):
        print("\n📚 Next Topics to Learn:")
        for i, topic in enumerate(recs['next_topics'], 1):
            print(f"   {i}. {topic}")
    
    if recs.get('practice_topics'):
        print("\n💪 Topics to Practice:")
        for i, topic in enumerate(recs['practice_topics'], 1):
            print(f"   {i}. {topic}")
    
    # Test with new user (no history)
    print("\n" + "-"*60)
    new_user = "new_test_user"
    print(f"\n3️⃣ Testing recommendations for NEW user: {new_user}")
    
    new_recs = get_recommendations_for_user(new_user)
    
    print(f"\n📊 RECOMMENDATIONS FOR NEW USER:")
    if new_recs.get('next_topics'):
        print("\n📚 Suggested Starting Topics:")
        for i, topic in enumerate(new_recs['next_topics'], 1):
            print(f"   {i}. {topic}")
    
    if new_recs.get('practice_topics'):
        print("\n💪 Practice Suggestions:")
        for i, topic in enumerate(new_recs['practice_topics'], 1):
            print(f"   {i}. {topic}")
    
    # Verify recommendations are valid
    print("\n" + "="*60)
    print("VALIDATION")
    print("="*60)
    
    checks = []
    
    # Check 1: Recommendations exist
    has_recs = bool(recs.get('next_topics') or recs.get('practice_topics'))
    checks.append(("Recommendations generated", has_recs))
    
    # Check 2: New user gets recommendations
    has_new_recs = bool(new_recs.get('next_topics') or new_recs.get('practice_topics'))
    checks.append(("New user recommendations", has_new_recs))
    
    # Check 3: Topics are strings
    all_strings = all(isinstance(t, str) for t in recs.get('next_topics', []) + recs.get('practice_topics', []))
    checks.append(("Topics are strings", all_strings))
    
    # Check 4: No empty topics
    no_empty = all(t.strip() for t in recs.get('next_topics', []) + recs.get('practice_topics', []))
    checks.append(("No empty topics", no_empty))
    
    print()
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}: {'PASS' if passed else 'FAIL'}")
    
    all_passed = all(passed for _, passed in checks)
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ SUCCESS: All tests passed!")
        print("Recommendations system is working correctly!")
    else:
        print("❌ FAILURE: Some tests failed")
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = test_recommendations()
    sys.exit(0 if success else 1)
