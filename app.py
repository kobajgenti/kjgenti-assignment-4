from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
import numpy as np

app = Flask(__name__)

# Load the 20 newsgroups dataset
newsgroups = fetch_20newsgroups(subset='all')

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(newsgroups.data)

# Perform LSA
n_components = 100
lsa = TruncatedSVD(n_components=n_components)
X_lsa = lsa.fit_transform(X)

# Normalize the LSA vectors
X_lsa_normalized = normalize(X_lsa)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    
    # Transform the query using TF-IDF and LSA
    query_vec = vectorizer.transform([query])
    query_lsa = lsa.transform(query_vec)
    query_lsa_normalized = normalize(query_lsa)

    # Compute cosine similarity
    similarities = np.dot(X_lsa_normalized, query_lsa_normalized.T).flatten()
    
    # Get top 5 most similar documents
    top_indices = similarities.argsort()[-5:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            'document': newsgroups.data[idx][:200] + '...',  # Truncate for brevity
            'similarity': float(similarities[idx])
        })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)