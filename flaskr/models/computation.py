from pymongo import MongoClient
import sys
import numpy as np
import operator

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
        df = goal_evaluation.read_input_data_secondary(metric_file_path)
        ts = goal_evaluation.create_time_series(df)
        ts_featured = goal_evaluation.feature_engineer(ts, df)
        user_score = ts_featured['2_week_avg'][-1:].values
        ts_featured['2_week_avg']
        if np.isnan(user_score[0]):
            user_score = 0
        else:
            user_score = user_score[0]
        user_score_dict[user.encode('ascii')] = user_score
    sorted_x = sorted(user_score_dict.items(), key=operator.itemgetter(1))
    return sorted_x[-3:]


def get_bottom_performers(users):
    user_score_dict = {}
    for user in users:
        user_doc = collection.find_one({"username": user})
        metric_file_path = user_doc['metric_file_path']
        df = goal_evaluation.read_input_data_secondary(metric_file_path)
        ts = goal_evaluation.create_time_series(df)
        ts_featured = goal_evaluation.feature_engineer(ts, df)
        user_score = ts_featured['3_day_avg'][-1:].values
        if np.isnan(user_score[0]):
            user_score = 0
        else:
            user_score = user_score[0]
        user_score_dict[user.encode('ascii')] = user_score
    sorted_x = sorted(user_score_dict.items(), key=operator.itemgetter(1))
    return sorted_x[:2]


def get_self_performance_index(user):
    user_doc = collection.find_one({"username": user})
    print user_doc, user
    metric_file_path = user_doc['metric_file_path']
    df = goal_evaluation.read_input_data_secondary(metric_file_path)
    ts = goal_evaluation.create_time_series(df)
    ts_featured = goal_evaluation.feature_engineer(ts, df)
    user_score = ts_featured['3_day_avg'][-1:].values
    if np.isnan(user_score[0]):
        return 0
    else:
        return user_score[0]


def compare_friends(user, friends):
    top_n_performers_list = get_top_n_performers(friends + [user], 29)
    bottom_2_performers = get_bottom_performers(friends + [user])
    final_top_3 = []
    for use in top_n_performers_list:
        if use[0] not in dict(bottom_2_performers):
            final_top_3.append(use)
    return {'top': dict(final_top_3),
            'bottom': dict(bottom_2_performers),
            'self_last_day': get_self_performance_index(user)}


def main():
    users = ['utkarsh', 'vivek', 'siddhant', 'kunal', 'himanshu', 'abhishek']
    compare_friends('utkarsh', ['vivek', 'siddhant', 'kunal', 'himanshu', 'abhishek'])
    print get_top_n_performers(users, 30)


if __name__ == '__main__':
    main()
