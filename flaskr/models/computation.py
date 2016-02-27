from pymongo import MongoClient
import sys

sys.path.append("../../../")
import goal_evaluation

DATABASE = 'sports_hack'
COLLECTION = 'users'
client = MongoClient('localhost', 27017)
db = client[DATABASE]
collection = db[COLLECTION]


def get_top_n_performers(users, days=29):
    """
    Ensure users with same goals are passed into this functiona
    """
    user_score_dict = {}
    for user in users:
        user_doc = collection.find_one({"username": user})
        metric_file_path = user_doc['metric_file_path']
        print metric_file_path
        df = goal_evaluation.read_input_data(metric_file_path)
        ts = goal_evaluation.create_time_series(df)
        ts_featured = goal_evaluation.feature_engineer(ts, df)
        user_score = ts_featured['4_week_avg'][-1]
        user_score_dict[user] = user_score
    return user_score_dict


def compare_friends(user, friends):
    top_n_performers = get_top_n_performers(friends + user, 29)


def main():
    users = ['utkarsh', 'siddhanth']
    print get_top_n_performers(users, 30)


if __name__ == '__main__':
    main()
