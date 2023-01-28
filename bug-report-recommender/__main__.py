import pymongo
from recommender import SimilarBugReportsRecommendationSystem;
from data_loader import DataLoader;

TEST_DATABASE = ''
TEST_DATABASE_HOST = ''
PORT = 27017

def get_mongo_conn(MONGO_URL, MONGO_DATABASE):
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DATABASE]
    return db

def retrieve_sample_bug_report(db):
    x = db["bug"].find_one({
        "sample_set": True
    }, {
        "bg_number"     : True,
        "summary"       : True,
        "description"   : True,
        "product"       : True,
        "component"     : True,
        "platform"      : True,
        "type"          : True,
        "creation_time" : True,
        "assigned_to"   : True,
    })

    return x

# Demonstração de utilização de lib com DataLoader

def main():
    db = get_mongo_conn(MONGO_URL=TEST_DATABASE, MONGO_DATABASE=TEST_DATABASE_HOST)

    data_loader = DataLoader(database=TEST_DATABASE, host=TEST_DATABASE_HOST, port=PORT)

    recommender = SimilarBugReportsRecommendationSystem(data_loader=data_loader);

    example = retrieve_sample_bug_report(db)

    print('INPUT:')
    print(f'id={example["bg_number"]}, summary={example["summary"]}, creation_time={example["creation_time"]}')

    print('-'*50)

    print('requesting recommendations...')
    results = recommender.get_recommendations(
        query=example,
        K=10
    )

    print('RESULTS:')
    for i, result in enumerate(results):
        print(f'[{i+1}] id={result["recommendation"]["bg_number"]} - score={result["score"]} : summary={result["recommendation"]["summary"]}, creat_time={result["recommendation"]["creation_time"]}, w_w_resolved={result["recommendation"]["when_changed_to_resolved"]}')
        print('-'*50)

if __name__ == '__main__':
    main()
