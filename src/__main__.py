from data_loader import DataLoader;
from recommender import SimilarBugReportsRecommendationSystem;

def main():
    dl = DataLoader('data/dataset_curado.csv', max_items=5);

    data = dl.get_data();

    print(data[0].keys())

    for d in data:
        print(f',{d["pp_description"]} |||||||||||||||||| {d["description"]}')
        print('\n\n\n\n')

    #recommender = SimilarBugReportsRecommendationSystem(corpus=dl.get_data());

if __name__ == '__main__':
    main()
