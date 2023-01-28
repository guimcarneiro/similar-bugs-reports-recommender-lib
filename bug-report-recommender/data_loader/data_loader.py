import pymongo

class DataLoader():
    def __init__(self, database='', host='', port=27017):
        DATABASE_URL = f"mongodb://{host}:{port}/"

        print(f'starting connection with database at: {DATABASE_URL}{database}')
        self.client = pymongo.MongoClient(DATABASE_URL)
        self.db     = self.client[database]

    def retrieve_all_bugs(self):
        db_bugs = self.db["bug"]
        
        bugs = []

        bugs_from_db = db_bugs.find({
            "tfidf_vector": {
                "$exists": True
            },
            "embeddings_vector": {
                "$exists": True
            }
        }, {
            "bg_number"       : True,
            "summary"         : True,
            "description"     : True,
            "product"         : True,
            "component"       : True,
            "platform"        : True,
            "type"            : True,
            "creation_time"   : True,
            "assigned_to"     : True,
        })

        for bug in bugs_from_db:
            bugs.append(bug)
        
        return bugs

    def retrieve_candidates(self, query):
        db_arcs = self.db["arc"]

        candidates_from_db = db_arcs.find({
            "from": query["bg_number"]
        })

        candidates = []
        for candidate in candidates_from_db:
            candidates.append(candidate)
        
        return candidates