from pymongo import MongoClient

DATABASE = 'sports_hack'
COLLECTION = 'activities'
client = MongoClient('localhost', 27017)
db = client[DATABASE]
collection = db[COLLECTION]


def get_top_n_performers(users):
    """
    Ensure users with same goals are passed into this functiona
    """
    

def compare_friends(user, friends):
    top_n_performers = get_top_n_performers(friends + user)
