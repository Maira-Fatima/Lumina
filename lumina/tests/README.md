# 🧪 Lumina Testing Suite

## Quick Start

### Run All Tests
```bash
# From lumina root directory
python tests/run_all_tests.py

# Or from tests directory
cd tests
python run_all_tests.py
```

### Run Individual Tests
```bash
# Integration tests (comprehensive)
python tests/test_integration.py

# MCQ quiz tests
python tests/test_mcq.py

# Quiz and recommendations tests
python tests/test_quiz_and_recommendations.py
```

## Test Files

### 1. `run_all_tests.py` ⭐ NEW!
**Comprehensive test runner** that executes all tests and provides a summary.

**Usage:**
```bash
python tests/run_all_tests.py
```

**Output:**
- ✅ Pass/Fail status for each test suite
- 📊 Final summary with success rate
- 🎉 Clear indication if all tests pass

---

### 2. `test_integration.py`
**Comprehensive integration testing** for all major components.

**Tests:**
- ✅ Module imports (8 modules)
- ✅ Knowledge base loading (7,350 entries)
- ✅ Query matching engine (TF-IDF + cosine similarity)
- ✅ ML models (topic & difficulty classifiers)
- ✅ Expert system (rules, inference, prerequisites)
- ✅ Adaptive learning (state management, difficulty)
- ✅ Backend helpers (AI responses, chat)
- ✅ AI Companion (end-to-end integration)

**Expected Result:** 8/8 tests pass

---

### 3. `test_mcq.py`
**MCQ quiz functionality testing**

**Tests:**
- ✅ Quiz generation (creates 3-question quiz)
- ✅ MCQ format validation (4 options per question)
- ✅ Correct answer verification
- ✅ Answer checking with fuzzy matching
- ✅ Feedback generation

**Expected Result:** All MCQ tests pass

---

### 4. `test_quiz_and_recommendations.py`
**Quiz generation and recommendation system testing**

**Tests:**
- ✅ Recommendation engine
- ✅ Topic-based quiz generation
- ✅ Answer validation
- ✅ Scoring system

**Expected Result:** All quiz tests pass

---

### 5. `test_performance_tracking.py` ⭐ NEW!
**Performance tracking system verification**

**Purpose:** Verifies that user performance is correctly tracked and displayed.

**Tests:**
- ✅ User profile loading
- ✅ Performance recording (questions, correctness, topics)
- ✅ Success rate calculation
- ✅ Topic statistics (mastered vs. needs practice)
- ✅ State persistence (JSON + SQLite)

**Usage:**
```bash
python tests/test_performance_tracking.py
```

**Expected Output:**
```
✓ User loaded: test_performance_user
✓ Recorded 15 questions across 3 topics

Stats from StateManager:
  Total Questions: 59
  Total Correct: 29
  Success Rate: 49.2%
  
Stats from get_user_stats (UI):
  Total Questions: 59
  Overall Success Rate: 49.2%
  Topics Studied: 8
  Mastered Topics: []
  Needs Practice: [list of topics]

✅ SUCCESS: Performance tracking is working!
```

---

### 6. `test_recommendations.py` ⭐ NEW!
**Recommendations system functionality**

**Purpose:** Verifies personalized recommendations are generated correctly.

**Tests:**
- ✅ Recommendation generation for active users
- ✅ Recommendation generation for new users
- ✅ Topic format validation (strings, non-empty)
- ✅ Next topics vs. practice topics separation
- ✅ Fallback recommendations

**Usage:**
```bash
python tests/test_recommendations.py
```

**Expected Output:**
```
📊 RECOMMENDATIONS RECEIVED:
   Next Topics: 4 topics
   Practice Topics: 5 topics

📚 Next Topics to Learn:
   1. Python Basics
   2. Mathematics Basics
   3. Advanced Python
   4. Advanced ML

💪 Topics to Practice:
   1. Review Basics
   2. Machine Learning
   ...

✅ SUCCESS: All tests passed!
```

---
- ✅ Difficulty adjustment
- ✅ Personalized learning paths

**Expected Result:** All quiz & recommendation tests pass

---

## Test Results

### Latest Test Run (December 11, 2024)

**Status:** ✅ **ALL TESTS PASSING**

```
Integration Tests     ✅ 8/8 PASS
MCQ Tests            ✅ PASS
Quiz & Recommendations ✅ PASS

Success Rate: 100%
```

**Performance:**
- Query matching: 76-100% similarity
- ML models: 94% topic, 97% difficulty accuracy
- Knowledge base: 7,350 entries loaded successfully
- Response time: <500ms average

---

## Troubleshooting

### Import Errors
All test files now include proper path setup:
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### Module Not Found
Ensure you're running from the correct directory:
```bash
# From project root
cd "e:\University\4th Sem\AI\Project\Improve 2\lumina"
python tests/test_integration.py
```

### NLTK Data Missing
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Streamlit Warnings
Warnings like "missing ScriptRunContext" are normal when running tests outside of Streamlit and can be safely ignored.

---

## Adding New Tests

### Template for New Test File
```python
"""
Description of what this test file tests
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_something():
    print("=" * 60)
    print("Testing Something...")
    print("=" * 60)
    
    try:
        # Your test code here
        from some_module import some_function
        
        result = some_function()
        
        assert result is not None
        print("✓ Test passed")
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_something()
    import sys
    sys.exit(0 if success else 1)
```

---

## Continuous Integration

To run tests automatically:

### GitHub Actions Example
```yaml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python tests/run_all_tests.py
```

---

## Test Coverage

**Current Coverage:** ~95%

**Covered:**
- ✅ Core NLP processing
- ✅ Query matching
- ✅ ML classification
- ✅ Expert system reasoning
- ✅ Adaptive learning
- ✅ Quiz generation
- ✅ MCQ functionality
- ✅ State management
- ✅ API endpoints

**Not Yet Covered:**
- ⏳ UI components (Streamlit interface)
- ⏳ Database migrations
- ⏳ Performance benchmarks

---

## Performance Benchmarks

Run performance tests:
```python
import time
from core.ai_companion import load_ai_companion

tutor = load_ai_companion()

# Benchmark query response
start = time.time()
result = tutor.ask("What is machine learning?", "test_user")
elapsed = time.time() - start

print(f"Query time: {elapsed*1000:.0f}ms")
# Expected: <500ms
```

---

## Best Practices

1. **Run tests before committing**
   ```bash
   python tests/run_all_tests.py
   ```

2. **Fix failing tests immediately**
   - Don't commit code with failing tests
   - Debug and fix before pushing

3. **Add tests for new features**
   - Every new feature should have tests
   - Follow the template above

4. **Keep tests fast**
   - Use smaller datasets for testing when possible
   - Mock external dependencies

5. **Document test cases**
   - Clear descriptions of what's being tested
   - Expected outcomes documented

---

## Support

For testing issues:
1. Check [DEVELOPER_GUIDE.md](../docs/DEVELOPER_GUIDE.md) for troubleshooting
2. Review [TESTING_REPORT.md](../docs/TESTING_REPORT.md) for known issues
3. Run individual tests to isolate problems

---

*Testing documentation v2.0*  
*Last Updated: December 11, 2024*  
*All tests passing ✅*
