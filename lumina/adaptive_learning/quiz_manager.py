"""
Quiz Manager - Quiz generation, execution, and scoring

Provides comprehensive quiz functionality:
- Timed quizzes
- Custom question count and difficulty
- Mixed difficulty support
- Quiz scoring and review
- Wrong answer analysis
"""

import random
from typing import List, Dict, Optional
from datetime import datetime
from .state_manager import StateManager


class QuizManager:
    """
    Manages quiz creation, execution, and scoring.
    
    Features:
    - Generate quizzes from knowledge base
    - Timed quiz mode
    - Multiple difficulty levels
    - Comprehensive scoring
    - Wrong answer review
    """
    
    def __init__(self, state_manager: StateManager = None):
        """Initialize quiz manager."""
        self.state = state_manager or StateManager()
        self.current_quiz: Optional[Dict] = None
        self.quiz_start_time: Optional[datetime] = None
    
    def create_quiz(
        self,
        topic: str = None,
        difficulty: str = None,
        num_questions: int = 10,
        time_limit: Optional[int] = None,
        mix_difficulty: bool = False
    ) -> Dict:
        """
        Create a new quiz.
        
        Args:
            topic (str): Topic for quiz (None = mixed topics)
            difficulty (str): Difficulty level (None = current level)
            num_questions (int): Number of questions
            time_limit (int): Time limit in minutes (None = untimed)
            mix_difficulty (bool): Mix difficulty levels
            
        Returns:
            dict: Quiz configuration
        """
        from core.data_loader import get_expanded_knowledge_base
        
        kb = get_expanded_knowledge_base()
        
        # Filter questions
        filtered = kb
        if topic:
            filtered = [q for q in filtered if q.get('topic') == topic]
        
        if difficulty and not mix_difficulty:
            filtered = [q for q in filtered if q.get('difficulty') == difficulty]
        
        # Select random questions
        if len(filtered) < num_questions:
            num_questions = len(filtered)
        
        selected = random.sample(filtered, num_questions)
        
        # Generate MCQ options for each question
        for q in selected:
            if 'options' not in q:
                q['options'] = self._generate_mcq_options(q, filtered)
        
        # Create quiz structure
        quiz = {
            'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'topic': topic or 'Mixed Topics',
            'difficulty': difficulty or 'Mixed',
            'num_questions': num_questions,
            'time_limit': time_limit,
            'questions': selected,
            'answers': [],
            'started_at': None,
            'completed_at': None,
            'score': None
        }
        
        self.current_quiz = quiz
        self.state.set_quiz_mode(True)
        
        return quiz
    
    def _generate_mcq_options(self, question: Dict, all_questions: List[Dict]) -> List[str]:
        """
        Generate 4 MCQ options for a question (1 correct + 3 distractors).
        
        Args:
            question: The question to generate options for
            all_questions: All available questions to pick distractors from
            
        Returns:
            list: 4 options with the correct answer randomly positioned
        """
        correct_answer = question['answer']
        topic = question.get('topic', 'General')
        
        # Shorten answers to make them suitable for MCQ options
        def shorten_answer(ans: str, max_words: int = 50) -> str:
            """Shorten long answers for MCQ display."""
            sentences = ans.split('.')
            if len(sentences) > 0 and sentences[0].strip():
                # Take first sentence
                first_sent = sentences[0].strip()
                words = first_sent.split()
                if len(words) > max_words:
                    return ' '.join(words[:max_words]) + '...'
                return first_sent + '.'
            return ans[:200] + '...' if len(ans) > 200 else ans
        
        correct_short = shorten_answer(correct_answer)
        
        # Get potential distractors from same topic
        same_topic_questions = [q for q in all_questions 
                               if q.get('topic') == topic and q['answer'] != correct_answer]
        
        distractors = []
        
        # Pick 3 random distractors
        if len(same_topic_questions) >= 3:
            distractor_qs = random.sample(same_topic_questions, 3)
            distractors = [shorten_answer(d['answer']) for d in distractor_qs]
        elif len(same_topic_questions) > 0:
            # Use available same-topic questions
            distractors = [shorten_answer(q['answer']) for q in same_topic_questions]
            # Fill remaining with other topics
            other_questions = [q for q in all_questions 
                             if q.get('topic') != topic and q['answer'] != correct_answer]
            if len(other_questions) >= (3 - len(distractors)):
                additional = random.sample(other_questions, 3 - len(distractors))
                distractors.extend([shorten_answer(d['answer']) for d in additional])
        else:
            # If not enough same-topic questions, use any other questions
            other_questions = [q for q in all_questions if q['answer'] != correct_answer]
            if len(other_questions) >= 3:
                distractor_qs = random.sample(other_questions, 3)
                distractors = [shorten_answer(d['answer']) for d in distractor_qs]
        
        # Ensure we have exactly 3 distractors
        while len(distractors) < 3:
            distractors.append("None of the above")
        
        distractors = distractors[:3]
        
        # Combine correct answer with distractors
        options = [correct_short] + distractors
        
        # Shuffle options
        random.shuffle(options)
        
        return options
    
    def start_quiz(self) -> bool:
        """Start the current quiz."""
        if not self.current_quiz:
            return False
        
        self.current_quiz['started_at'] = datetime.now().isoformat()
        self.quiz_start_time = datetime.now()
        return True
    
    def submit_answer(
        self,
        question_index: int,
        user_answer: str,
        time_taken: float = 0.0
    ) -> Dict:
        """
        Submit an answer for a question.
        
        Args:
            question_index (int): Question index
            user_answer (str): User's answer
            time_taken (float): Time taken for this question
            
        Returns:
            dict: Answer result
        """
        if not self.current_quiz:
            return {'error': 'No active quiz'}
        
        question = self.current_quiz['questions'][question_index]
        correct_answer = question['answer']
        
        # Simple correctness check (could be enhanced)
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        
        answer_record = {
            'question_index': question_index,
            'question': question['question'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'time_taken': time_taken,
            'topic': question['topic'],
            'difficulty': question['difficulty']
        }
        
        self.current_quiz['answers'].append(answer_record)
        
        # Record performance
        self.state.record_performance(
            topic=question['topic'],
            difficulty=question['difficulty'],
            question=question['question'],
            correct=is_correct,
            time_taken=time_taken
        )
        
        return answer_record
    
    def complete_quiz(self) -> Dict:
        """Complete and score the current quiz."""
        if not self.current_quiz:
            return {'error': 'No active quiz'}
        
        self.current_quiz['completed_at'] = datetime.now().isoformat()
        
        # Calculate score
        total = len(self.current_quiz['questions'])
        correct = sum(1 for a in self.current_quiz['answers'] if a['is_correct'])
        score_percentage = (correct / total) * 100 if total > 0 else 0
        
        # Calculate time taken
        if self.quiz_start_time:
            time_elapsed = (datetime.now() - self.quiz_start_time).total_seconds() / 60
        else:
            time_elapsed = 0
        
        # Calculate average time per question
        avg_time = time_elapsed / total if total > 0 else 0
        
        score_data = {
            'total_questions': total,
            'correct_answers': correct,
            'wrong_answers': total - correct,
            'score_percentage': score_percentage,
            'time_elapsed_minutes': time_elapsed,
            'avg_time_per_question': avg_time,
            'grade': self._calculate_grade(score_percentage)
        }
        
        self.current_quiz['score'] = score_data
        self.state.set_quiz_mode(False)
        
        return score_data
    
    def get_wrong_answers(self) -> List[Dict]:
        """Get all wrong answers for review."""
        if not self.current_quiz:
            return []
        
        return [a for a in self.current_quiz['answers'] if not a['is_correct']]
    
    def get_quiz_summary(self) -> Dict:
        """Get comprehensive quiz summary."""
        if not self.current_quiz or not self.current_quiz.get('score'):
            return {'error': 'Quiz not completed'}
        
        score = self.current_quiz['score']
        wrong = self.get_wrong_answers()
        
        # Topic breakdown
        topic_stats = {}
        for answer in self.current_quiz['answers']:
            topic = answer['topic']
            if topic not in topic_stats:
                topic_stats[topic] = {'total': 0, 'correct': 0}
            
            topic_stats[topic]['total'] += 1
            if answer['is_correct']:
                topic_stats[topic]['correct'] += 1
        
        # Calculate topic success rates
        for topic in topic_stats:
            total = topic_stats[topic]['total']
            correct = topic_stats[topic]['correct']
            topic_stats[topic]['success_rate'] = (correct / total) * 100
        
        # Find weak areas
        weak_topics = [
            topic for topic, stats in topic_stats.items()
            if stats['success_rate'] < 60
        ]
        
        summary = {
            'quiz_id': self.current_quiz['id'],
            'topic': self.current_quiz['topic'],
            'difficulty': self.current_quiz['difficulty'],
            'score': score,
            'wrong_count': len(wrong),
            'topic_breakdown': topic_stats,
            'weak_areas': weak_topics,
            'recommendations': self._generate_quiz_recommendations(topic_stats, weak_topics)
        }
        
        return summary
    
    def compare_with_previous(self, topic: str = None) -> Dict:
        """Compare current quiz with previous attempts."""
        if not self.current_quiz:
            return {'error': 'No active quiz'}
        
        current_score = self.current_quiz['score']['score_percentage']
        
        # Get historical performance
        if topic:
            stats = self.state.get_topic_stats(topic)
            previous_rate = stats['success_rate']
        else:
            overall = self.state.get_overall_stats()
            previous_rate = overall['success_rate']
        
        improvement = current_score - previous_rate
        
        return {
            'current_score': current_score,
            'previous_average': previous_rate,
            'improvement': improvement,
            'status': 'improved' if improvement > 0 else 'declined' if improvement < 0 else 'stable'
        }
    
    def _calculate_grade(self, percentage: float) -> str:
        """Calculate letter grade from percentage."""
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    def _generate_quiz_recommendations(
        self,
        topic_stats: Dict,
        weak_topics: List[str]
    ) -> List[str]:
        """Generate recommendations based on quiz performance."""
        recommendations = []
        
        if weak_topics:
            recommendations.append(f"Focus on: {', '.join(weak_topics[:3])}")
            recommendations.append("Review fundamental concepts in weak areas")
        
        for topic, stats in topic_stats.items():
            if stats['success_rate'] >= 90:
                recommendations.append(f"Excellent performance in {topic}! Ready for advanced topics")
        
        if not recommendations:
            recommendations.append("Great job! Keep practicing to maintain your level")
        
        return recommendations
    
    def export_quiz_results(self, filepath: str):
        """Export quiz results to file."""
        if not self.current_quiz:
            return
        
        import json
        with open(filepath, 'w') as f:
            json.dump(self.current_quiz, f, indent=4)
        
        print(f"✓ Quiz results exported to {filepath}")
