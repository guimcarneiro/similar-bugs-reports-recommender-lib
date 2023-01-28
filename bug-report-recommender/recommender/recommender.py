# Retrieves all bug reports available for recommendations
# Creates in-memory index of cached bugs
# Using query received, retrieve similarity arcs and calculate similarity score
# sorts ranking using score, returning only top-k

class SimilarBugReportsRecommendationSystem():
    def __init__(self, data_loader):
        self.data = data_loader

        print("creating and populating cached bugs index...")
        self.cached_bugs_index = self._construct_cached_bugs_index(self.data.retrieve_all_bugs())
    
    def _construct_cached_bugs_index(self, bugs):
        index = {}

        for bug in bugs:
            if bug["bg_number"] not in index.keys():
                index[bug["bg_number"]] = bug
        
        return index

    def _calculate_score(self, tfidf_score, embeddings_score, categoric_score):
        return (tfidf_score + embeddings_score) * categoric_score

    def get_recommendations(self, query, K=10):
        ranking = []

        candidates = self.data.available_candidates(query)
        for candidate in candidates:
            candidate_score = self._calculate_score(tfidf_score=candidate["cos_similarity_tfidf"],
                                                    embeddings_score=candidate["cos_similarity_word_embeddings"],
                                                    categoric_score=candidate["categoric_similarity"])
            candidate_obj = {
                "bg_number": candidate["bg_number"],
                "score": candidate_score
            }
            ranking.append(candidate_obj)

        ranking.sort(key=lambda r: r["score"], reverse=True)

        ranking = ranking[:K]

        recommendations = [{ "score": r["score"], "item": self.cached_bugs_index[r["bg_number"]] } for r in ranking]

        return recommendations