from sentence_transformers import SentenceTransformer
from utils import BERT

class BertVectorizer():
    def __init__(self):
        print(f'instanciating bert...')
        self.vectorizer = SentenceTransformer(BERT)

    def transform(self, docs):
        vectorized_docs = [ self.vectorizer.encode(doc) for doc in docs ]
        return vectorized_docs