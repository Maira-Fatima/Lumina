import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz, process

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Technical dictionary for typo correction
TECHNICAL_TERMS = {
    'neural network', 'machine learning', 'deep learning', 'backpropagation',
    'gradient descent', 'convolutional', 'recurrent', 'lstm', 'gru', 'transformer',
    'attention mechanism', 'reinforcement learning', 'supervised learning',
    'unsupervised learning', 'overfitting', 'underfitting', 'regularization',
    'dropout', 'batch normalization', 'activation function', 'loss function',
    'optimizer', 'hyperparameter', 'epoch', 'batch size', 'learning rate',
    'accuracy', 'precision', 'recall', 'f1 score', 'confusion matrix',
    'cross validation', 'feature engineering', 'data augmentation',
    'transfer learning', 'fine tuning', 'embedding', 'tokenization',
    'lemmatization', 'stemming', 'tf-idf', 'cosine similarity',
    'euclidean distance', 'k-nearest neighbors', 'decision tree',
    'random forest', 'support vector machine', 'naive bayes',
    'linear regression', 'logistic regression', 'clustering',
    'k-means', 'hierarchical clustering', 'dbscan', 'pca',
    'dimensionality reduction', 'autoencoder', 'gan', 'generative adversarial network',
    'object detection', 'semantic segmentation', 'natural language processing',
    'sentiment analysis', 'named entity recognition', 'question answering',
    'text classification', 'sequence to sequence', 'language model',
    'bert', 'gpt', 'word2vec', 'glove', 'elmo'
}

def correct_typos(text, confidence_threshold=90):
    """
    Corrects typos in text using fuzzy matching against technical dictionary.
    
    Args:
        text: Input text to correct
        confidence_threshold: Minimum confidence (0-100) to apply correction
        
    Returns:
        corrected_text: Text with typos corrected
        corrections: List of (original, corrected, confidence) tuples
    """
    words = text.lower().split()
    corrections = []
    corrected_words = []
    
    for word in words:
        # Check if word needs correction (not in common words)
        if len(word) > 3 and word not in stop_words:
            # Try fuzzy matching against technical terms
            best_match = process.extractOne(word, TECHNICAL_TERMS, scorer=fuzz.ratio)
            
            if best_match and best_match[1] >= confidence_threshold:
                match_term, confidence = best_match[0], best_match[1]
                if word != match_term:
                    corrections.append((word, match_term, confidence))
                    corrected_words.append(match_term)
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)
    
    corrected_text = ' '.join(corrected_words)
    return corrected_text, corrections

def suggest_corrections(text, num_suggestions=3):
    """
    Suggests possible corrections for ambiguous typos.
    
    Args:
        text: Input text
        num_suggestions: Number of suggestions to return per word
        
    Returns:
        suggestions: Dict of {word: [suggested_corrections]}
    """
    words = text.lower().split()
    suggestions = {}
    
    for word in words:
        if len(word) > 3 and word not in stop_words:
            matches = process.extract(word, TECHNICAL_TERMS, scorer=fuzz.ratio, limit=num_suggestions)
            # Only suggest if confidence is between 70-89 (ambiguous range)
            filtered_matches = [match for match in matches if 70 <= match[1] < 90]
            if filtered_matches and word not in TECHNICAL_TERMS:
                suggestions[word] = [match[0] for match in filtered_matches]
    
    return suggestions

def preprocess_text(text):
    """
    Cleans and prepares text data for vectorization.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    processed_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and word.isalpha()]
    return " ".join(processed_tokens)
