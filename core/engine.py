import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.nlp_utils import preprocess_text, correct_typos, suggest_corrections

class QueryMatchingEngine:
    """
    An efficient engine to find the best-matching answer for a user query
    using TF-IDF vectorization and Cosine Similarity with typo correction.
    """
    def __init__(self, dataset):
        self.df = pd.DataFrame(dataset)
        self.df['processed_question'] = self.df['question'].apply(preprocess_text)
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None

    def fit(self):
        """
        Fits the vectorizer on the dataset's processed questions
        and creates the TF-IDF matrix. This prepares the engine for queries.
        """
        corpus = self.df['processed_question'].tolist()
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        print("Engine is trained and ready.")

    def find_match(self, user_query, threshold=0.2):
        """
        Finds the best matching answer for a user's query with typo correction.
        
        Returns:
            dict: {
                'answer': str,
                'corrected_query': str,
                'corrections': list,
                'suggestions': dict,
                'similarity': float,
                'matched_question': str
            }
        """
        if self.tfidf_matrix is None:
            raise RuntimeError("Engine has not been fitted. Please call .fit() first.")

        # Apply typo correction
        corrected_query, corrections = correct_typos(user_query, confidence_threshold=90)
        
        # Get suggestions for ambiguous typos
        suggestions = suggest_corrections(user_query)
        
        # Process the corrected query
        processed_query = preprocess_text(corrected_query)
        query_vector = self.vectorizer.transform([processed_query])

        similarities = cosine_similarity(query_vector, self.tfidf_matrix)
        best_match_index = np.argmax(similarities)
        max_similarity = similarities[0, best_match_index]
        matched_question = self.df.iloc[best_match_index]['question']

        print(f"\nUser Query: '{user_query}'")
        if corrections:
            print(f"-> Auto-corrected: '{corrected_query}'")
            for orig, corr, conf in corrections:
                print(f"   '{orig}' → '{corr}' (confidence: {conf}%)")
        if suggestions:
            print(f"-> Did you mean: {suggestions}")
        print(f"-> Processed Query: '{processed_query}'")
        print(f"-> Best match: '{matched_question}'")
        print(f"-> Similarity Score: {max_similarity:.4f}")

        result = {
            'corrected_query': corrected_query if corrections else user_query,
            'corrections': corrections,
            'suggestions': suggestions,
            'similarity': max_similarity,
            'matched_question': matched_question
        }

        if max_similarity > threshold:
            result['answer'] = self.df.iloc[best_match_index]['answer']
        else:
            result['answer'] = "I'm sorry, I couldn't find a confident answer in my knowledge base. Could you please rephrase your question?"
        
        return result
