from core.ai_companion import load_ai_companion
import time

# Cache the tutor instance globally
_tutor_cache = None

def get_ai_response(user_input, current_context, user_id=None, record_performance=True):
    """
    Enhanced AI response with typo correction, adaptive learning, and recommendations.
    
    Args:
        user_input: User's question
        current_context: Current topic context
        user_id: User identifier for personalization
        record_performance: Whether to track this interaction
        
    Returns:
        tuple: (response_md, new_context, metadata)
    """
    # 1. Get the cached AI companion instance
    global _tutor_cache
    if _tutor_cache is None:
        _tutor_cache = load_ai_companion()
    tutor = _tutor_cache
    
    # 2. Call the enhanced backend
    start_time = time.time()
    result = tutor.ask(user_input, user_id=user_id, record_performance=record_performance)
    time_taken = time.time() - start_time
    
    # 3. Extract components from result
    answer = result.get("answer", "I'm sorry, I couldn't process your request.")
    related = result.get("related_topics", [])
    corrected_query = result.get("corrected_query", user_input)
    corrections = result.get("corrections", [])
    suggestions = result.get("suggestions", {})
    topic = result.get("topic", "General")
    difficulty = result.get("difficulty", "Intermediate")
    current_difficulty = result.get("current_difficulty", "Intermediate")
    prerequisites = result.get("prerequisites", [])
    prerequisites_met = result.get("prerequisites_met", True)
    recommendations = result.get("recommendations", {})
    difficulty_adjusted = result.get("difficulty_adjusted", False)
    adjustment_reason = result.get("adjustment_reason", "")
    
    # 4. Use the AI's topic extraction for context
    new_context = topic
    if new_context == "General" and "sorry" not in answer.lower():
        new_context = current_context
    
    # 5. Build enhanced markdown response
    response_md = ""
    
    # Show typo corrections if any
    if corrections:
        response_md += "**🔍 Auto-corrected your query:**\n"
        for orig, corr, conf in corrections:
            response_md += f"- '{orig}' → '{corr}' (confidence: {conf}%)\n"
        response_md += f"\n*Understanding: \"{corrected_query}\"*\n\n"
    
    # Show suggestions for ambiguous typos
    if suggestions:
        response_md += "**💡 Did you mean:**\n"
        for word, suggestion_list in suggestions.items():
            response_md += f"- '{word}' → {', '.join(suggestion_list[:2])}\n"
        response_md += "\n"
    
    # Show prerequisite warnings
    if not prerequisites_met and prerequisites:
        response_md += "**⚠️ Prerequisites Notice:**\n"
        response_md += f"To fully understand *{topic}*, you should first master:\n"
        for prereq in prerequisites[:3]:  # Show top 3
            response_md += f"- {prereq}\n"
        response_md += "\n"
    
    # Main answer
    response_md += answer
    
    # Show current difficulty level
    if topic != "General":
        response_md += f"\n\n**📊 Current Level:** {current_difficulty} | **Topic:** {topic}"
    
    # Show difficulty adjustment if occurred
    if difficulty_adjusted:
        new_diff = result.get("new_difficulty", current_difficulty)
        response_md += f"\n\n**🎯 Difficulty Adjusted!**\n"
        response_md += f"Moving from {current_difficulty} → {new_diff}\n"
        response_md += f"*{adjustment_reason}*"
    
    # Add related topics if available
    if "I'm sorry" not in answer and related and len(related) > 1:
        response_md += f"\n\n**🔗 Related Concepts:**\n"
        for item in related[1:4]:  # Show up to 3 related concepts
            response_md += f"- {item}\n"
    
    # Add recommendations
    if recommendations:
        if recommendations.get('next_topics'):
            response_md += f"\n\n**📚 Next Topics to Study:**\n"
            for next_topic in recommendations['next_topics'][:3]:
                response_md += f"- {next_topic}\n"
        
        if recommendations.get('practice_topics'):
            response_md += f"\n**💪 Practice These Topics:**\n"
            for practice_topic in recommendations['practice_topics'][:2]:
                response_md += f"- {practice_topic}\n"
    
    # 6. Prepare metadata for tracking
    metadata = {
        'topic': topic,
        'difficulty': difficulty,
        'current_difficulty': current_difficulty,
        'time_taken': time_taken,
        'corrected_query': corrected_query,
        'corrections_made': len(corrections) > 0,
        'prerequisites_met': prerequisites_met,
        'difficulty_adjusted': difficulty_adjusted,
        'recommendations': recommendations
    }
    
    return response_md, new_context, metadata


def record_interaction(user_id, topic, difficulty, correct, time_taken, question):
    """
    Record user interaction for performance tracking.
    
    Args:
        user_id: User identifier
        topic: Question topic
        difficulty: Question difficulty
        correct: Whether answer was correct
        time_taken: Time in seconds
        question: Question text
    """
    try:
        from adaptive_learning.state_manager import StateManager
        from adaptive_learning.difficulty_manager import DifficultyManager
        
        state = StateManager()
        state.load_user(user_id)
        
        # Record performance
        state.record_performance(topic, difficulty, correct, time_taken, question)
        
        # Update counters
        state.increment_topic_questions(topic)
        if correct:
            state.increment_topic_correct(topic)
        
        # Check for difficulty adjustment
        diff_manager = DifficultyManager(state)
        if diff_manager.should_adjust_difficulty(topic):
            action, new_diff, reason = diff_manager.calculate_difficulty_adjustment(topic)
            if action != "maintain":
                diff_manager.apply_difficulty_adjustment(topic, action, new_diff)
                return True, new_diff, reason
        
        state.save_user_profile()
        return False, None, None
        
    except Exception as e:
        print(f"Error recording interaction: {e}")
        return False, None, None


def get_user_stats(user_id, topic=None, days=7):
    """
    Get user performance statistics.
    
    Args:
        user_id: User identifier
        topic: Specific topic (optional)
        days: Number of days to analyze
        
    Returns:
        dict: Statistics dictionary
    """
    try:
        from adaptive_learning.state_manager import StateManager
        from adaptive_learning.performance_tracker import PerformanceTracker
        
        state = StateManager()
        state.load_user(user_id)
        tracker = PerformanceTracker(state)
        
        if topic:
            # Topic-specific stats
            success_rate = tracker.calculate_success_rate(topic, days)
            trend = tracker.get_performance_trend(topic, days)
            stats = state.get_topic_stats(topic)
            
            return {
                'topic': topic,
                'success_rate': success_rate,
                'trend': trend,
                'stats': stats
            }
        else:
            # Overall stats
            summary = tracker.get_learning_summary(days)
            
            # Ensure all expected keys are present
            if not summary:
                overall = state.get_overall_stats()
                summary = {
                    'total_questions': overall.get('total_questions', 0),
                    'total_correct': overall.get('total_correct', 0),
                    'overall_success_rate': overall.get('success_rate', 0),
                    'topics_studied': 0,
                    'mastered_topics': [],
                    'needs_practice': []
                }
            
            return summary
            
    except Exception as e:
        print(f"Error getting user stats: {e}")
        import traceback
        traceback.print_exc()
        return {
            'total_questions': 0,
            'total_correct': 0,
            'overall_success_rate': 0,
            'topics_studied': 0,
            'mastered_topics': [],
            'needs_practice': []
        }


def get_recommendations_for_user(user_id, current_topic=None):
    """
    Get personalized recommendations for user.
    
    Args:
        user_id: User identifier
        current_topic: Current topic being studied
        
    Returns:
        dict: Recommendations with next_topics and practice_topics
    """
    try:
        from adaptive_learning.state_manager import StateManager
        from adaptive_learning.recommendation_engine import RecommendationEngine
        
        state = StateManager()
        state.load_user(user_id)
        rec_engine = RecommendationEngine(state)
        
        # Get context based on performance
        stats = state.get_overall_stats()
        context = 'general'
        if stats.get('total_questions', 0) > 5 and stats.get('success_rate', 0) < 50:
            context = 'struggling'
        elif stats.get('success_rate', 0) > 85:
            context = 'mastery'
        
        # Get recommendations
        recommendations = rec_engine.get_recommendations(
            context=context,
            max_recommendations=10
        )
        
        # Transform to expected format
        next_topics = []
        practice_topics = []
        
        for rec in recommendations:
            rec_type = rec.get('type', '')
            topic = rec.get('topic', '')
            reason = rec.get('reason', '')
            
            # Only add if topic is not empty
            if topic and topic.strip():
                if rec_type == 'next_topic':
                    next_topics.append(f"{topic}")
                elif rec_type in ['practice', 'support', 'difficulty']:
                    # Add reason for practice topics
                    practice_topics.append(f"{topic}")
        
        # Remove duplicates while preserving order
        next_topics = list(dict.fromkeys(next_topics))
        practice_topics = list(dict.fromkeys(practice_topics))
        
        # Add current topic to practice if provided and not already there
        if current_topic and current_topic not in practice_topics and current_topic not in next_topics:
            practice_topics.insert(0, current_topic)
        
        # Ensure we have at least some recommendations
        if not next_topics and not practice_topics:
            next_topics = ['Python Basics', 'Data Structures', 'Algorithms']
            practice_topics = ['Review fundamentals']
        
        return {
            'next_topics': next_topics[:5],
            'practice_topics': practice_topics[:5]
        }
        
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        import traceback
        traceback.print_exc()
        
        # Return fallback recommendations
        return {
            'next_topics': ['Python Basics', 'Data Structures', 'Machine Learning'],
            'practice_topics': ['Review fundamentals', 'Practice problem-solving']
        }


def create_quiz(user_id, topic, difficulty, num_questions, time_limit=None):
    """
    Create a new quiz for the user.
    
    Args:
        user_id: User identifier
        topic: Topic for the quiz
        difficulty: Difficulty level
        num_questions: Number of questions
        time_limit: Time limit in minutes
        
    Returns:
        dict: Quiz configuration
    """
    try:
        from adaptive_learning.state_manager import StateManager
        from adaptive_learning.quiz_manager import QuizManager
        
        state = StateManager()
        state.load_user(user_id)
        quiz_mgr = QuizManager(state)
        
        quiz = quiz_mgr.create_quiz(
            topic=topic if topic != "General" else None,
            difficulty=difficulty,
            num_questions=num_questions,
            time_limit=time_limit,
            mix_difficulty=False
        )
        
        return quiz
        
    except Exception as e:
        print(f"Error creating quiz: {e}")
        import traceback
        traceback.print_exc()
        return None


def check_quiz_answer(user_id, question, user_answer, correct_answer, topic, difficulty):
    """
    Check if a quiz answer is correct and record performance.
    
    Args:
        user_id: User identifier
        question: Question text
        user_answer: User's answer (could be shortened MCQ option)
        correct_answer: Correct answer (full answer)
        topic: Question topic
        difficulty: Question difficulty
        
    Returns:
        bool: True if correct
    """
    try:
        from adaptive_learning.state_manager import StateManager
        
        # For MCQ, check if user answer is contained in correct answer or vice versa
        # This handles shortened options matching full answers
        user_lower = user_answer.strip().lower()
        correct_lower = correct_answer.strip().lower()
        
        # Check exact match first
        is_correct = user_lower == correct_lower
        
        # If not exact match, check if shortened answer matches start of full answer
        if not is_correct:
            # Check if user answer is the beginning of correct answer (for shortened MCQ options)
            is_correct = correct_lower.startswith(user_lower) or user_lower.startswith(correct_lower)
        
        # Record performance
        state = StateManager()
        state.load_user(user_id)
        state.record_performance(
            topic=topic,
            difficulty=difficulty,
            question=question,
            correct=is_correct,
            time_taken=0.0
        )
        
        # Update counters for tracking
        state.increment_topic_questions(topic)
        if is_correct:
            state.increment_topic_correct(topic)
        
        return is_correct
        
    except Exception as e:
        print(f"Error checking answer: {e}")
        return False


def generate_chat_title(messages):
    """Generates a short, descriptive title from the first user prompt."""
    if messages:
        first_prompt = messages[0].get("content", "Untitled Chat")
        max_len = 35
        title = (first_prompt[:max_len] + '...') if len(first_prompt) > max_len else first_prompt
        return title
    return "Untitled Chat"