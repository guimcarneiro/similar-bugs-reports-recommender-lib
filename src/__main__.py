from data_loader import DataLoader;
from recommender import SimilarBugReportsRecommendationSystem;

def main():
    print('instanciating data loader');
    dl = DataLoader('data/dataset_apenas_firefox_e_general.csv', max_items=20);

    data = dl.get_data();

    print('instanciating recommender');
    recommender = SimilarBugReportsRecommendationSystem(corpus=dl.get_data());

    input_data = data[1]

    results = recommender.get_recommendations(input_data)

    print('INPUT:')
    print(f'id={input_data["bg_number"]}, product={input_data["product"]}, component={input_data["component"]}, summary={input_data["summary"]}')

    print('-------------------------')

    print('RESULTS:')
    for result in results:
        print(f'id={result["item"]["bg_number"]}, product={result["item"]["product"]}, component={result["item"]["component"]}, summary={result["item"]["summary"]}, score={result["score"]}')

if __name__ == '__main__':
    main()
