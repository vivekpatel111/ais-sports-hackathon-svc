from pymongo import MongoClient
import pandas as pd

DATABASE = 'sports_hack'
COLLECTION = 'user_activities'
client = MongoClient('localhost', 27017)
db = client[DATABASE]
collection = db[COLLECTION]


def read_input_data():
    """Converts input csv file to pandas dataframe."""
    df = pd.read_csv("../data/training_load_data.csv", skiprows=1,
                     names=["date", "status", "session_time", "type",
                            "duration", "rpe", "session_load"],
                     parse_dates=["date"])
    return df

if __name__ == '__main__':
    main()
