from sentence_transformers import util

from utils import calculate_cos_similarity

class SimilarBugReportsRecommendationSystem():
    def __init__(self, corpus):
        # TODO: separate in config file
        self.categoric_fields = ['product', 'component']

        # In-Memory and fill index
        self.reverse_index = self.__build_reverse_index(corpus)

        # Load configuration
        pass

    def __get_index_key(self, fields):
        index_key = ''
        for value in fields:
            index_key += f'{value}_'
        return index_key[:-1]

    def __build_reverse_index(self, corpus):
        reverse_index = {}

        # create categoric indexes
        for item in corpus:
            # retrieve values of categoric fields to create index keys
            index_field_values = []
            for field in self.categoric_fields:
                index_field_values.append(item[field])       
            index_key = self.__get_index_key(index_field_values)

            # create entry if it not exists and populates it
            if index_key not in reverse_index.keys():
                reverse_index[index_key] = { str(item['bg_number']): item }
                print(f'adding index to reverse_index: {index_key}')
            else:
                reverse_index[index_key][str(item['bg_number'])] = item
        
        return reverse_index
    
    def __calculate_score(self, ranking_obj):
        # TODO: enhance calculation
        TFIDF_WEIGHT = 0.5
        BERT_WEIGHT = 0.5

        return ((TFIDF_WEIGHT*ranking_obj['tfidf_score']) + (BERT_WEIGHT*ranking_obj['embedding_score']))/(TFIDF_WEIGHT + BERT_WEIGHT)

    def __format_result(self, item, score):
        # TODO: enhance formatation
        item_obj = {
            'bg_number': item['bg_number'],
            'summary': item['summary'],
            'description': item['description'],
            'product': item['product'],
            'component': item['component'],
        }

        obj = {
            'item': item_obj,
            'score': score
        }
        return obj


    def get_recommendations(self, item):
        # generate index_key for item
        item_categoric_field_values = []
        for field in self.categoric_fields:
            categoric_field_value = item[field]
            item_categoric_field_values.append(categoric_field_value)
        
        item_index_key = self.__get_index_key(item_categoric_field_values)

        # TODO: add multiplier depending of the match of categoric fields

        # retrieve items of index_key
        candidates_index = self.reverse_index[item_index_key]
        candidates = candidates_index.keys()

        # create ranking with similarity score using tfidf vector
        ranking = []
        for candidate in candidates:
            tfidf_score = calculate_cos_similarity(candidates_index[candidate]['tfidf_vector'], item['tfidf_vector'])
            embedding_score = calculate_cos_similarity([candidates_index[candidate]['bert_embeddings']], [item['bert_embeddings']])

            # TODO: separar separar iterações pois deve ter filtragem entre cos tfidf e cos embeddings
            # TODO: possibly apply cut on tfidf_ranking
            ranking_obj = {
                'bg_number': candidates_index[candidate]['bg_number'],
                'tfidf_score': tfidf_score,
                'embedding_score': embedding_score
            }
            # calculate and insert general score into ranking_obj
            ranking_obj['general_score'] = self.__calculate_score(ranking_obj)

            ranking.append(ranking_obj)
        
        # TODO: order by tfidf

        # ordering by general_score temporarily
        ranking = sorted(ranking, key=lambda d: d['general_score'], reverse=True)
        
        # keep only top K
        K = 5
        top_k_recommendations_from_ranking = ranking[:K]
        
        # build results
        result = []
        for recommendation in top_k_recommendations_from_ranking:
            i = candidates_index[str(recommendation['bg_number'])]
            s = recommendation['general_score']
            result.append(self.__format_result(i, s))
        
        return result