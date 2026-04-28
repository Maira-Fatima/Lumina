"""
Comprehensive test runner for Lumina AI Study Companion
Runs all tests and reports results
"""

import sys
import os
import subprocess

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def run_test_file(test_file):
    """Run a test file using subprocess with UTF-8 encoding"""
    try:
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_path = os.path.join(project_root, "tests", test_file)
        
        # Set environment to use UTF-8 encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            cwd=project_root,
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr and "warning" not in result.stderr.lower():
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def run_all_tests():
    """Run all available tests"""
    
    print_header("🧪 LUMINA TEST SUITE - RUNNING ALL TESTS")
    
    results = {
        'passed': 0,
        'failed': 0,
        'total': 0
    }
    
    # Test 1: Integration Tests
    print_header("1️⃣  Integration Tests")
    if run_test_file("test_integration.py"):
        print("✅ Integration tests: PASSED")
        results['passed'] += 1
    else:
        print("❌ Integration tests: FAILED")
        results['failed'] += 1
    results['total'] += 1
    
    # Test 2: MCQ Tests
    print_header("2️⃣  MCQ Quiz Tests")
    if run_test_file("test_mcq.py"):
        print("✅ MCQ tests: PASSED")
        results['passed'] += 1
    else:
        print("❌ MCQ tests: FAILED")
        results['failed'] += 1
    results['total'] += 1
    
    # Test 3: Quiz and Recommendations
    print_header("3️⃣  Quiz & Recommendations Tests")
    if run_test_file("test_quiz_and_recommendations.py"):
        print("✅ Quiz & Recommendations: PASSED")
        results['passed'] += 1
    else:
        print("❌ Quiz & Recommendations: FAILED")
        results['failed'] += 1
    results['total'] += 1
    
    # Final Summary
    print_header("📊 FINAL TEST SUMMARY")
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    
    success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
        return True
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
