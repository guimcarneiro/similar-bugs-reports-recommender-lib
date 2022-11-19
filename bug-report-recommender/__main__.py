from recommender import SimilarBugReportsRecommendationSystem;
from data_loader import DataLoader

def main():
    data_path = '../data/dataset_apenas_firefox_e_general.csv'

    print(f'instanciating data loader from {data_path}');
    data_loader = DataLoader(data_file_path=data_path, data_type='csv', max_items=10)

    print('instanciating recommender');
    recommender = SimilarBugReportsRecommendationSystem(data_loader=data_loader);

    example = data_loader.get_data()[0];

    print('INPUT:')
    print(f'id={example["bg_number"]}, product={example["product"]}, component={example["component"]}, summary={example["summary"]}')

    print('-------------------------')

    results = recommender.get_recommendations(item=example)

    print('RESULTS:')
    for result in results:
        print(f'id={result["item"]["bg_number"]}, product={result["item"]["product"]}, component={result["item"]["component"]}, summary={result["item"]["summary"]}, score={result["score"]}')
        print('-------')

if __name__ == '__main__':
    main()
