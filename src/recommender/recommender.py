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
                reverse_index[index_key] = {[item['bg_number']]: item}
            else:
                reverse_index[index_key][item['bg_number']] = item
        
        return reverse_index
