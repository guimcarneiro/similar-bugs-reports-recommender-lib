from sklearn.feature_extraction.text import TfidfVectorizer as SklearnTfIdfVectorizer

class TfidfVectorizer():
    def __init__(self, corpus):
        self.vectorizer = SklearnTfIdfVectorizer()
        print(f'Fitting tfidfVectorizer with a corpus with size of {len(corpus)} docs...')
        self.vectorizer.fit(corpus)
    
    def transform(self, text):
        return self.vectorizer.transform([text])
        