from pymongo import MongoClient
import goal_evaluation
from flaskr.static import send_notification
from datetime import datetime, timedelta

DATABASE = 'sports_hack'
COLLECTION = 'users'
client = MongoClient('localhost', 27017)
db = client[DATABASE]
collection = db[COLLECTION]


def get_suggestion():
    return goal_evaluation.suggest_exercises()


def main():
    users = collection.find({})
    gcm_client = send_notification.GCMessage()
    for user_doc in users:
        metric_path = user_doc["metric_file_path"]
        username = user_doc['username']
        df = goal_evaluation.read_input_data_secondary(metric_path)
        ts = goal_evaluation.create_time_series(df)
        ts = goal_evaluation.feature_engineer(ts, df)
        date = datetime.now() - timedelta(days=1)
        date = date.date()
        weekly_goal = 16500
        fav_activity = "cycling"
        suggestion = goal_evaluation.suggest_exercises(ts, date, weekly_goal, fav_activity)
        gmc_key = user_doc['credentials']['gmc']['auth_key']
        collection.update_one({'username': username}, {'$set': {'weekly_suggestion': suggestion}})
        data = {
            "to": gmc_key,
            "notification": {
                "title": "Exercise suggestions",
                "body": suggestion,
                "sound": "default"
            }
        }
        print gcm_client.post_request(data)


if __name__ == '__main__':
    main()
