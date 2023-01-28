from sklearn.metrics.pairwise import cosine_similarity

def calculate_cos_similarity(vector_a, vector_b):
    return cosine_similarity(vector_a, vector_b)[0][0]

def calculate_categoric_fields_similarity(query, doc, categoric_fields):
    x = 0.0
    
    for categoric_field in categoric_fields:
        if (query[categoric_field] == doc[categoric_field]):
            x += 0.5

    return (x/len(categoric_fields))
