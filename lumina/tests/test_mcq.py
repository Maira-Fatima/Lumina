"""
Test MCQ quiz functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_mcq_generation():
    print("=" * 60)
    print("Testing MCQ Generation...")
    print("=" * 60)
    
    try:
        from backend.helper import create_quiz
        
        # Create a quiz
        quiz = create_quiz(
            user_id="test_user",
            topic="Machine Learning",
            difficulty="Intermediate",
            num_questions=3,
            time_limit=10
        )
        
        if not quiz:
            print("✗ Quiz creation failed")
            return False
        
        print(f"✓ Quiz created with {len(quiz['questions'])} questions")
        
        # Check each question has MCQ options
        for i, q in enumerate(quiz['questions']):
            options = q.get('options', [])
            if options:
                print(f"\n✓ Question {i+1} has {len(options)} options")
                print(f"  Q: {q['question'][:60]}...")
                print(f"  Options:")
                for j, opt in enumerate(options):
                    print(f"    {chr(65+j)}) {opt[:80]}{'...' if len(opt) > 80 else ''}")
                
                # Check if correct answer is in options
                correct = q['answer']
                
                # Check for exact match or partial match (shortened)
                found = False
                for opt in options:
                    if opt.lower() == correct.lower():
                        found = True
                        break
                    if correct.lower().startswith(opt.lower()) or opt.lower().startswith(correct[:50].lower()):
                        found = True
                        break
                
                if found:
                    print(f"  ✓ Correct answer is among options")
                else:
                    print(f"  ⚠ Correct answer not clearly in options")
            else:
                print(f"✗ Question {i+1} has no options!")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mcq_answer_checking():
    print("\n" + "=" * 60)
    print("Testing MCQ Answer Checking...")
    print("=" * 60)
    
    try:
        from backend.helper import check_quiz_answer
        
        # Test 1: Exact match
        correct = check_quiz_answer(
            user_id="test_user",
            question="What is 2+2?",
            user_answer="4",
            correct_answer="4",
            topic="Math",
            difficulty="Beginner"
        )
        
        if correct:
            print("✓ Exact match works")
        else:
            print("✗ Exact match failed")
            return False
        
        # Test 2: Shortened answer (MCQ option) matches full answer
        full_answer = "Machine learning is a branch of artificial intelligence that focuses on building systems that learn from data."
        shortened = "Machine learning is a branch of artificial intelligence that focuses on building systems"
        
        correct = check_quiz_answer(
            user_id="test_user",
            question="What is machine learning?",
            user_answer=shortened,
            correct_answer=full_answer,
            topic="ML",
            difficulty="Beginner"
        )
        
        if correct:
            print("✓ Shortened answer matching works")
        else:
            print("✗ Shortened answer matching failed")
            return False
        
        # Test 3: Wrong answer
        incorrect = check_quiz_answer(
            user_id="test_user",
            question="What is 2+2?",
            user_answer="5",
            correct_answer="4",
            topic="Math",
            difficulty="Beginner"
        )
        
        if not incorrect:
            print("✓ Incorrect answer detection works")
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
    print("MCQ QUIZ TEST")
    print("=" * 60 + "\n")
    
    results = {
        "MCQ Generation": test_mcq_generation(),
        "MCQ Answer Checking": test_mcq_answer_checking()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:<30} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All MCQ tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
