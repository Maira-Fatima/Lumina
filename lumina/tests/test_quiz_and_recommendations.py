"""
Quick test for quiz and recommendations features
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_recommendations():
    print("=" * 60)
    print("Testing Recommendations...")
    print("=" * 60)
    
    try:
        from backend.helper import get_recommendations_for_user
        
        recs = get_recommendations_for_user("test_user", "Machine Learning")
        
        print(f"✓ Recommendations received")
        print(f"  Next topics: {recs.get('next_topics', [])}")
        print(f"  Practice topics: {recs.get('practice_topics', [])}")
        
        if 'next_topics' in recs and 'practice_topics' in recs:
            print("✓ Correct format returned")
            return True
        else:
            print("✗ Incorrect format")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quiz_creation():
    print("\n" + "=" * 60)
    print("Testing Quiz Creation...")
    print("=" * 60)
    
    try:
        from backend.helper import create_quiz
        
        quiz = create_quiz(
            user_id="test_user",
            topic="Machine Learning",
            difficulty="Intermediate",
            num_questions=5,
            time_limit=10
        )
        
        if quiz:
            print(f"✓ Quiz created")
            print(f"  Topic: {quiz.get('topic')}")
            print(f"  Questions: {len(quiz.get('questions', []))}")
            print(f"  Difficulty: {quiz.get('difficulty')}")
            
            if quiz.get('questions'):
                q = quiz['questions'][0]
                print(f"  Sample question: {q.get('question', '')[:60]}...")
                return True
            else:
                print("⚠ No questions in quiz")
                return False
        else:
            print("✗ Quiz creation failed")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_answer_checking():
    print("\n" + "=" * 60)
    print("Testing Answer Checking...")
    print("=" * 60)
    
    try:
        from backend.helper import check_quiz_answer
        
        # Test correct answer
        is_correct = check_quiz_answer(
            user_id="test_user",
            question="What is 2+2?",
            user_answer="4",
            correct_answer="4",
            topic="Math",
            difficulty="Beginner"
        )
        
        if is_correct:
            print("✓ Correct answer detected")
        else:
            print("✗ Failed to detect correct answer")
            return False
        
        # Test incorrect answer
        is_correct = check_quiz_answer(
            user_id="test_user",
            question="What is 2+2?",
            user_answer="5",
            correct_answer="4",
            topic="Math",
            difficulty="Beginner"
        )
        
        if not is_correct:
            print("✓ Incorrect answer detected")
            return True
        else:
            print("✗ Failed to detect incorrect answer")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "=" * 60)
    print("QUIZ & RECOMMENDATIONS TEST")
    print("=" * 60 + "\n")
    
    results = {
        "Recommendations": test_recommendations(),
        "Quiz Creation": test_quiz_creation(),
        "Answer Checking": test_answer_checking()
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
        print("\n🎉 All tests passed! Quiz and Recommendations are working.")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
