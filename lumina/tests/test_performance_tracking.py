"""
Quick test to verify performance tracking is working
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from adaptive_learning.state_manager import StateManager
from adaptive_learning.performance_tracker import PerformanceTracker
from backend.helper import get_user_stats

print("=" * 70)
print("Testing Performance Tracking")
print("=" * 70)

# Initialize state
state = StateManager()
state.load_user("test_performance_user")

print(f"\n✓ User loaded: test_performance_user")

# Record some performance
topics = ["Python", "Machine Learning", "Data Structures"]
for topic in topics:
    for i in range(5):
        is_correct = i < 4  # 80% success rate
        state.record_performance(
            topic=topic,
            difficulty="Intermediate",
            question=f"Question {i+1} about {topic}",
            correct=is_correct,
            time_taken=30.0
        )
        state.increment_topic_questions(topic)
        if is_correct:
            state.increment_topic_correct(topic)

print(f"✓ Recorded 15 questions across 3 topics")

# Get overall stats using state manager
overall = state.get_overall_stats()
print(f"\n📊 Stats from StateManager:")
print(f"  Total Questions: {overall['total_questions']}")
print(f"  Total Correct: {overall['total_correct']}")
print(f"  Success Rate: {overall['success_rate']:.1f}%")
print(f"  Mastered Topics: {overall['mastered_topics']}")

# Get stats using helper function (what the UI uses)
stats = get_user_stats("test_performance_user", days=30)
print(f"\n📊 Stats from get_user_stats (UI):")
print(f"  Total Questions: {stats.get('total_questions', 0)}")
print(f"  Total Correct: {stats.get('total_correct', 0)}")
print(f"  Overall Success Rate: {stats.get('overall_success_rate', 0):.1f}%")
print(f"  Topics Studied: {stats.get('topics_studied', 0)}")
print(f"  Mastered Topics: {stats.get('mastered_topics', [])}")
print(f"  Needs Practice: {stats.get('needs_practice', [])}")

# Get topic-specific stats
all_topics = state.get_all_topic_stats()
print(f"\n📚 Per-Topic Stats:")
for topic_stat in all_topics:
    if topic_stat['attempts'] > 0:
        print(f"  {topic_stat['topic']}: {topic_stat['success_rate']:.1f}% ({topic_stat['correct']}/{topic_stat['attempts']})")

print("\n" + "=" * 70)
if stats.get('total_questions', 0) > 0:
    print("✅ SUCCESS: Performance tracking is working!")
else:
    print("❌ FAILURE: Performance tracking not recording data")
print("=" * 70)
