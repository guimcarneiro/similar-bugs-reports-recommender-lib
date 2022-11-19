
import pandas as pd

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import string

from vectorizer import TfidfVectorizer, BertVectorizer

class DataLoader():
    def __init__(self, data_file_path='', data_type='csv', max_items=-1):
        self.data = self.__process(
            self.__pre_process(
                self.__apply_format_rules(
                    self.__load(
                        data_file_path=data_file_path,
                        data_type=data_type,
                        max_items=max_items
                    )
                )
            )
        )
        self.data = self.data.to_dict('records')

    # load data from file
    def __load(self, data_file_path, data_type='csv', max_items=-1):
        if data_type == 'csv':
            print(f'loading data from {data_file_path}')
            df = pd.read_csv(data_file_path)
            if (max_items > 0 and max_items <= df.shape[0]):
                df = df[:max_items]

        print(f'data length: {df.shape[0]}')

        return df                
    
    # apply formatation and feature filtering
    def __apply_format_rules(self, dataframe):
        print('applying format rules...')
        dataframe = dataframe.astype({'bg_number': 'int32'})
        dataframe = dataframe.astype({'bg_number': 'str'})

        # when description is NaN, redefines it to summary
        self.__apply_nan_threatment(dataframe)

        # concat summary at the beginning of description
        # self.__apply_summary_and_description_concat(dataframe)

        return dataframe[['bg_number', 'product', 'component', 'description', 'summary']]

    def __apply_nan_threatment(self, dataframe):
        for i, row in dataframe.iterrows():
            if(type(row['description']) is not str):
                print(f'applying nan threatment to bg_number={row["bg_number"]}')
                dataframe.loc[i, 'description'] = row['summary']        

    def __apply_summary_and_description_concat(self, dataframe):
        for i, row in dataframe.iterrows():
            if (not row['description'] == row['summary']):
                print(f'applying summary and description concat to bg_number={row["bg_number"]}')
                dataframe.loc[i, 'description'] = row['summary'] + ' ' + row['description'] 

    # remove stopwords and punctuation
    def __pre_process(self, data):
        print('start pre processing...')

        nltk.download('stopwords')
        nltk.download('punkt')

        stop = set(stopwords.words('english') + list(string.punctuation))
        
        pre_processed_docs = []
        print(f'removing stopwords and punctuation...')
        for i, row in data.iterrows():
            print(f'{i}/{data.shape[0]} bg_number={row["bg_number"]}')
            doc = row['description']

            pre_processed_doc = " ".join([desc for desc in word_tokenize(doc.lower()) if desc not in stop])
            pre_processed_docs.append(pre_processed_doc)
        
        data['pp_description'] = pre_processed_docs

        return data

    # generate vectors and embeddings
    def __process(self, data):
        print('start processing...')

        tfidf_vectorizer = TfidfVectorizer(data['pp_description'].values.tolist())
        bert_vectorizer = BertVectorizer()

        tfidf_vectors = []
        bert_embeddings = []
        for i, row in data.iterrows():
            print(f'doc {i+1}/{data.shape[0]}')

            print(f'calculating tfidf vector for {row["bg_number"]}...')
            tfidf_vector = tfidf_vectorizer.transform(row['pp_description'])
            tfidf_vectors.append(tfidf_vector) 

            print(f'calculating embeddings for {row["bg_number"]}...')
            bert_embedding = bert_vectorizer.transform(row['description'])
            bert_embeddings.append(bert_embedding[0])

        data['tfidf_vector'] = tfidf_vectors
        data['bert_embeddings'] = bert_embeddings

        return data

    def get_data(self):
        return self.data

    def get_available_ids(self):
        return self.data['bg_number'].to_list()