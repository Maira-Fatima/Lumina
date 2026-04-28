import nltk
from nltk.corpus import stopwords

def download_nltk_data():
    """Downloads necessary NLTK models."""
    try:
        stopwords.words('english')
        print("NLTK data already available.")
    except LookupError:
        print("Downloading NLTK resources...")
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        print("Downloads complete.")
    return True


def get_expanded_knowledge_base():
    """
    Get the expanded knowledge base with 7,500+ entries.
    Loads from cache file for performance.
    """
    import json
    import os
    
    cache_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base_cache.json')
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                kb = json.load(f)
            print(f"✓ Loaded {len(kb)} entries from knowledge base cache")
            return kb
        except Exception as e:
            print(f"⚠ Error loading knowledge base cache: {e}")
            print("⚠ Using fallback knowledge base")
            return combined_data
    else:
        print("⚠ Knowledge base cache not found, using fallback")
        return combined_data


combined_data = [
    # OOP Data
    {"topic": "OOP", "intent": "Object-Oriented Programming", "question": "What is Object-Oriented Programming (OOP)?", "answer": "Object-Oriented Programming (OOP) is a programming methodology that views a program as consisting of objects that interact with each other. It combines data and the functions that operate on that data into a single unit called an object."},
    {"topic": "OOP", "intent": "Encapsulation", "question": "What is encapsulation in OOP?", "answer": "Encapsulation groups software into a unit with a well-defined interface, making it easy to use. It involves making instance variables private and providing public methods for access, a principle also known as information hiding."},
    {"topic": "OOP", "intent": "Inheritance", "question": "Explain the concept of inheritance.", "answer": "Inheritance allows a new class (derived class) to be created from an existing class (base class), inheriting its members. The new class can then extend or replace the functionality of the base class."},
    {"topic": "OOP", "intent": "Polymorphism", "question": "What is polymorphism?", "answer": "Polymorphism, meaning 'many forms', lets you program in the general rather than the specific. It allows objects of different classes that share a superclass to be processed as if they are all objects of the superclass."},

    # DSA Data
    {"topic": "DSA", "intent": "Array", "question": "What is an array data structure?", "answer": "An array is a list of data elements stored in a contiguous block of memory, which allows for very fast O(1) reading of any element by calculating its memory address from its index."},
    {"topic": "DSA", "intent": "Linked List", "question": "What is a linked list and how does it differ from an array?", "answer": "A linked list is a node-based data structure where data can be scattered in memory. Each node contains data and a pointer to the next node, allowing for efficient O(1) insertions and deletions at the beginning of the list."},
    {"topic": "DSA", "intent": "Hash Table", "question": "What is a hash table and why is it fast for lookups?", "answer": "A hash table stores key-value pairs and uses a hash function to convert a key into a numerical index. This allows for lookups, on average, to be performed in O(1) time, as the key directly points to the value's location."},
    {"topic": "DSA", "intent": "Binary Search", "question": "What is binary search and what is its time complexity?", "answer": "Binary search is an efficient algorithm for finding an item from a sorted array. It repeatedly divides the search interval in half. Its time complexity is O(log N)."},

    # AI Data
    {"topic": "AI", "intent": "Definition of AI", "question": "What is Artificial Intelligence?", "answer": "Artificial Intelligence is a field focused on creating systems that can mimic human intelligence. Key topics include Agents, Problem-Solving, Searching, Knowledge Representation, and Automated Planning."},
    {"topic": "AI", "intent": "Search Algorithms", "question": "What are the main types of search algorithms in AI?", "answer": "AI search algorithms are categorized as uninformed (blind) search (like BFS, DFS) and informed (heuristic) search (like A* Search), which uses problem-specific knowledge to find solutions more efficiently."},
    {"topic": "AI", "intent": "Game Theory", "question": "What is Min-Max in game theory?", "answer": "Minimax is a backtracking algorithm for two-player games like Chess. It finds the optimal move by exploring the game tree, where one player (maximizer) tries to maximize their score and the other (minimizer) tries to minimize it."},

    # Machine Learning Data
    {"topic": "ML", "intent": "Supervised Learning", "question": "What is supervised learning?", "answer": "Supervised learning is a paradigm where a model learns from labeled data, consisting of input features and correct outputs. Common techniques include Decision Trees, Naive Bayes, KNN, and Linear Regression."},
    {"topic": "ML", "intent": "Unsupervised Learning", "question": "What is unsupervised learning?", "answer": "Unsupervised learning is used for clustering problems to find hidden patterns in unlabeled data. Common techniques include K-means, Principle Component Analysis (PCA), and Agglomerative Clustering."},
    {"topic": "ML", "intent": "Reinforcement Learning", "question": "Explain reinforcement learning.", "answer": "In reinforcement learning, an agent learns to make decisions by performing actions in an environment to maximize a cumulative reward. Key algorithms include Q-Learning and Monte Carlo methods."},

    # Data Mining Data
    {"topic": "Data Mining", "intent": "Definition of Data Mining", "question": "What is data mining?", "answer": "Data mining is the process of automatically discovering useful information and novel patterns in large data repositories. It is a key part of the Knowledge Discovery in Databases (KDD) process."},
    {"topic": "Data Mining", "intent": "Data Preprocessing", "question": "Why is data preprocessing important?", "answer": "Data preprocessing transforms raw data into a suitable format for analysis. It includes cleaning data to remove noise, fusing data from multiple sources, and selecting relevant features."},
    {"topic": "Data Mining", "intent": "Classification", "question": "What is classification in data mining?", "answer": "Classification is a predictive task that assigns a discrete class label to new, unseen data based on a model built from a labeled training set."},
    {"topic": "Data Mining", "intent": "Cluster Analysis", "question": "What is cluster analysis?", "answer": "Cluster analysis is a descriptive task that groups observations into clusters, such that observations in the same cluster are more similar to each other than to those in other clusters."},
    {"topic": "Data Mining", "intent": "Association Analysis", "question": "What is association analysis?", "answer": "Association analysis discovers patterns describing strongly associated features, often as implication rules. Market Basket Analysis is a classic example, finding items frequently bought together."},

    # Database Data
    {"topic": "Database", "intent": "Relational Model", "question": "What is the relational model?", "answer": "The relational model represents data in tables (relations) with rows and columns. Key concepts include domains, attributes, keys, schema, and integrity constraints."},
    {"topic": "Database", "intent": "Normalization", "question": "What is normalization in databases?", "answer": "Normalization is the process of organizing tables in a relational database to minimize data redundancy and prevent data anomalies. It involves progressing through normal forms like 1NF, 2NF, and 3NF."},
    {"topic": "Database", "intent": "SQL", "question": "What is SQL?", "answer": "SQL (Structured Query Language) is the standard language for managing relational databases. It includes sub-languages like DDL (for defining data structures) and DML (for manipulating data)."}
]