from sklearn.metrics.pairwise import cosine_similarity

def calculate_cos_similarity(vector_a, vector_b):
    return cosine_similarity(vector_a, vector_b)[0][0]