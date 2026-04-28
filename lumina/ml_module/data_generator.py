"""
Data Generator Module - Automatically generates synthetic training data

This module creates training datasets from the expanded knowledge base:
- Generates question variations using paraphrasing
- Creates synthetic samples with difficulty labels
- Applies 70/15/15 train/validation/test split
- Generates diverse question templates
"""

import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class DataGenerator:
    """
    Generates synthetic training data for ML models from knowledge base.
    
    Uses multiple strategies:
    1. Question template variations
    2. Paraphrasing techniques
    3. Synthetic performance history generation
    """
    
    def __init__(self, knowledge_base):
        """
        Initialize data generator with knowledge base.
        
        Args:
            knowledge_base (list): List of knowledge entries
        """
        self.knowledge_base = knowledge_base
        
        # Question variation templates
        self.question_templates = {
            'what': [
                "What is {concept}?",
                "What does {concept} mean?",
                "Can you explain what {concept} is?",
                "Could you tell me about {concept}?",
                "Define {concept}",
                "Explain {concept} to me"
            ],
            'how': [
                "How does {concept} work?",
                "How do you implement {concept}?",
                "How can I use {concept}?",
                "Explain how {concept} works",
                "Show me how to use {concept}"
            ],
            'why': [
                "Why is {concept} important?",
                "Why do we use {concept}?",
                "What's the purpose of {concept}?",
                "Why should I learn {concept}?"
            ],
            'difference': [
                "What's the difference between {concept1} and {concept2}?",
                "How do {concept1} and {concept2} differ?",
                "Compare {concept1} and {concept2}",
                "Explain the difference between {concept1} and {concept2}"
            ]
        }
    
    def generate_question_variations(self, entry, num_variations=5):
        """
        Generate variations of a question from a knowledge base entry.
        
        Args:
            entry (dict): Knowledge base entry
            num_variations (int): Number of variations to generate
            
        Returns:
            list: List of question variations
        """
        concept = entry['intent']
        base_question = entry['question']
        variations = [base_question]
        
        # Generate variations using templates
        template_type = random.choice(list(self.question_templates.keys()))
        templates = self.question_templates[template_type]
        
        for _ in range(min(num_variations - 1, len(templates))):
            template = random.choice(templates)
            
            if '{concept1}' in template and '{concept2}' in template:
                # Skip comparison templates for now
                continue
            
            if '{concept}' in template:
                variation = template.format(concept=concept)
                variations.append(variation)
        
        # Add simple variations
        simple_variations = [
            f"Tell me about {concept}",
            f"Explain {concept}",
            f"{concept} definition",
            f"I want to learn about {concept}",
            f"Help me understand {concept}"
        ]
        
        variations.extend(random.sample(simple_variations, min(3, len(simple_variations))))
        
        return list(set(variations))[:num_variations]
    
    def generate_training_dataset(self, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
        """
        Generate complete training, validation, and test datasets.
        
        Args:
            train_ratio (float): Proportion for training set
            val_ratio (float): Proportion for validation set
            test_ratio (float): Proportion for test set
            
        Returns:
            tuple: (train_df, val_df, test_df)
        """
        all_samples = []
        
        print("Generating training data from knowledge base...")
        
        for entry in self.knowledge_base:
            # Generate question variations
            variations = self.generate_question_variations(entry, num_variations=3)
            
            for question in variations:
                sample = {
                    'question': question,
                    'topic': entry['topic'],
                    'intent': entry['intent'],
                    'difficulty': entry.get('difficulty', 'Beginner'),
                    'answer': entry['answer']
                }
                all_samples.append(sample)
        
        # Convert to DataFrame
        df = pd.DataFrame(all_samples)
        
        # Shuffle the dataset
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Split into train, validation, test
        total_size = len(df)
        train_size = int(total_size * train_ratio)
        val_size = int(total_size * val_ratio)
        
        train_df = df[:train_size]
        val_df = df[train_size:train_size + val_size]
        test_df = df[train_size + val_size:]
        
        print(f"✓ Generated {total_size} total samples")
        print(f"✓ Train: {len(train_df)} | Validation: {len(val_df)} | Test: {len(test_df)}")
        
        return train_df, val_df, test_df
    
    def generate_performance_history(self, num_sessions=50, questions_per_session=20):
        """
        Generate synthetic performance history for training the performance predictor.
        
        Args:
            num_sessions (int): Number of learning sessions to simulate
            questions_per_session (int): Average questions per session
            
        Returns:
            list: Simulated performance history
        """
        performance_data = []
        topics = list(set([entry['topic'] for entry in self.knowledge_base]))
        difficulties = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
        difficulty_scores = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Expert': 4}
        
        # Simulate learning progression
        base_success_rate = 0.3  # Start low
        learning_rate = 0.01  # Gradual improvement
        
        current_date = datetime.now() - timedelta(days=num_sessions)
        
        for session in range(num_sessions):
            # Simulate improvement over time
            session_success_rate = min(0.95, base_success_rate + (session * learning_rate))
            
            # Add some randomness
            session_success_rate += random.uniform(-0.1, 0.1)
            session_success_rate = max(0.1, min(0.95, session_success_rate))
            
            num_questions = random.randint(
                max(1, questions_per_session - 5),
                questions_per_session + 5
            )
            
            for _ in range(num_questions):
                topic = random.choice(topics)
                
                # Difficulty increases over time
                if session < 10:
                    difficulty = random.choices(
                        difficulties,
                        weights=[0.7, 0.2, 0.08, 0.02]
                    )[0]
                elif session < 30:
                    difficulty = random.choices(
                        difficulties,
                        weights=[0.3, 0.4, 0.25, 0.05]
                    )[0]
                else:
                    difficulty = random.choices(
                        difficulties,
                        weights=[0.1, 0.3, 0.4, 0.2]
                    )[0]
                
                # Higher difficulty = lower success probability
                difficulty_modifier = 1.0 - (difficulty_scores[difficulty] - 1) * 0.15
                question_success_rate = session_success_rate * difficulty_modifier
                
                correct = random.random() < question_success_rate
                
                # Time taken (harder questions take longer)
                base_time = 20 + (difficulty_scores[difficulty] * 10)
                time_taken = base_time + random.uniform(-10, 20)
                
                record = {
                    'timestamp': current_date + timedelta(hours=random.randint(0, 23)),
                    'topic': topic,
                    'difficulty': difficulty,
                    'correct': correct,
                    'time_taken': max(5, time_taken)
                }
                
                performance_data.append(record)
            
            current_date += timedelta(days=1)
        
        print(f"✓ Generated {len(performance_data)} performance records")
        
        return performance_data
    
    def generate_predictor_training_data(self, num_samples=200):
        """
        Generate training data for the performance predictor.
        
        Args:
            num_samples (int): Number of training samples to generate
            
        Returns:
            list: Training samples with history and target
        """
        training_samples = []
        
        for _ in range(num_samples):
            # Generate a performance history
            history_length = random.randint(10, 100)
            performance_history = self.generate_performance_history(
                num_sessions=history_length // 20,
                questions_per_session=20
            )
            
            # Split history into past and future
            split_point = int(len(performance_history) * 0.8)
            past_history = performance_history[:split_point]
            future_history = performance_history[split_point:]
            
            # Calculate future success rate as target
            if future_history:
                correct = sum(1 for r in future_history if r['correct'])
                future_success_rate = correct / len(future_history)
            else:
                future_success_rate = 0.5
            
            sample = {
                'history': past_history,
                'future_success_rate': future_success_rate
            }
            
            training_samples.append(sample)
        
        print(f"✓ Generated {num_samples} predictor training samples")
        
        return training_samples
    
    def save_datasets(self, output_dir='ml_module/data'):
        """
        Generate and save all datasets to CSV files.
        
        Args:
            output_dir (str): Directory to save datasets
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate classification datasets
        train_df, val_df, test_df = self.generate_training_dataset()
        
        train_df.to_csv(f'{output_dir}/training_data.csv', index=False)
        val_df.to_csv(f'{output_dir}/validation_data.csv', index=False)
        test_df.to_csv(f'{output_dir}/test_data.csv', index=False)
        
        print(f"✓ Datasets saved to {output_dir}")
        
        # Generate performance prediction data
        predictor_data = self.generate_predictor_training_data(num_samples=200)
        
        # Save as pickle for complex structure
        import pickle
        with open(f'{output_dir}/predictor_training_data.pkl', 'wb') as f:
            pickle.dump(predictor_data, f)
        
        print(f"✓ Predictor training data saved")
        
        return train_df, val_df, test_df
