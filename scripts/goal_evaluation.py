import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json


def read_input_data():
    """Converts input csv file to pandas dataframe."""
    df = pd.read_csv("../data/training_load_data.csv", skiprows=1,
                     names=["date", "status", "session_time", "type",
                            "duration", "rpe", "session_load"],
                     parse_dates=["date"])
    return df


def read_input_data_secondary(file):
    """Converts input csv file to pandas dataframe."""
    df = pd.read_csv(file, skiprows=1,
                     names=["date", "status", "session_time", "type",
                            "duration", "rpe", "session_load", "month"],
                     parse_dates=["date"])
    max_date = max(df.date)
    days_diff = (datetime(2016, 2, 27) - max_date).days
    df.date = pd.DatetimeIndex(df.date) + pd.DateOffset(days=days_diff)
    return df


def create_time_series(df):
    """Groups by date and computes overall training load by date. Offset the
    date to make the last entry in the dataset 27th February, 2016. Actual date
    value doesn't matter.

    Args:
        df: raw dataframe in csv file

    Returns:
        ts: time-series dataframe
    """
    grouped_df = df.groupby("date")
    ts = grouped_df["session_load"].agg(np.sum)
    ts = pd.DataFrame(data={"date": ts.index, "session_load": ts.values})
    return ts


def is_sick(df, date):
    """Checks if the user was sick on the given date
    Args:
        df: dataframe to search in (ideally the raw dataframe)
        date: python date object

    Returns:
        True or False
    """
    temp = df[df["date"] == date]
    if "Sick" in set(temp["status"].values):
        return True
    else:
        return False


def is_injured(df, date):
    """Checks if the user was injured on the given date
    Args:
        df: dataframe to search in
        date: python date object

    Returns:
        True or False
    """
    temp = df[df["date"] == date]
    if "Injured" in set(temp["status"].values):
        return True
    else:
        return False


def is_rest_for_4_days(df, date):
    """Checks if the user didn't train for at least the previous 4 days.
    Args:
        df: dataframe to search in
        date: python date object

    Returns:
        True or False
    """
    # TODO
    pass


def feature_engineer(ts, df):
    """Use rolling averages over 1-4 weeks, sick/injured information and acute:
    chronic training load ratio as features to decide the aggressiveness of the
    training load.

    Args:
        ts: time series dataframe
        df: raw input dataframe to get sickness and injury information

    Returns:
        the same dataframe with engineered features added
    """
    # compute rolling averages
    ts.loc[:, "last_day_avg"] = pd.rolling_mean(ts["session_load"], 1)
    ts.loc[:, "3_day_avg"] = pd.rolling_mean(ts["session_load"], 3)
    ts.loc[:, "weekly_avg"] = pd.rolling_mean(ts["session_load"], 7)
    ts.loc[:, "2_week_avg"] = pd.rolling_mean(ts["session_load"], 14)
    ts.loc[:, "3_week_avg"] = pd.rolling_mean(ts["session_load"], 21)
    ts.loc[:, "4_week_avg"] = pd.rolling_mean(ts["session_load"], 28)
    # injured or sick information
    ts["sick"] = ts["date"].apply(lambda x: int(is_sick(df, x)))
    ts["injured"] = ts["date"].apply(lambda x: int(is_injured(df, x)))
    # acute:chronic load ratio
    ts.loc[:, "w14"] = ts["weekly_avg"]/ts["4_week_avg"]
    return ts


def check_goal(ts, date, weekly_goal):
    """Evaluates the user entered target.

    Args:
        ts: time series dataframe
        date: date on which user entered the goal
        weekly_goal: weekly_goal in terms of training load (intensity*duration)

    Returns:
        Moderate, moderately aggressive or aggressive.
    """
    # assess risk of injury for goal set, i.e. find optimal range for training
    four_week_avg = ts[ts["date"] == date]["4_week_avg"].values[0]
    daily_goal = weekly_goal/7.0
    min_load = four_week_avg * 0.8
    moderate_load_threshold = four_week_avg*1.25
    aggressive_threshold = four_week_avg*1.5
    max_load = four_week_avg * 1.5
    # TODO: if sick the previous day, change the recommendation. Recommend no
    # more than 10% of the average training load.
    # TODO: if sick for at least the last 4 days, plan a proper training plan
    # for recovery
    if min_load <= daily_goal < moderate_load_threshold:
        return "Moderate"
    elif moderate_load_threshold <= daily_goal < aggressive_threshold:
        return "Moderately aggressive"
    elif daily_goal > max_load:
        return "Aggressive"
    else:
        return "Too easy"


def get_intensity(goal):
    """Fetches the intensity associated with a goal, like cycling or running.

    Args:
        goal: goal provided by the user

    Returns:
        intensity: RPE, integer 1-10 scale
    """
    with open("../data/goal_intensity_mapping.json", "r") as f:
        data = json.load(f)

    return data[goal]


def get_weekly_avg_load(ts, date):
    """Get the average daily load for the last week.

    Args:
        ts: time series dataframe
        date: date on which user entered the goal, usually the previous day
        data

    Returns:
        daily avg load for the past week
    """
    ts = ts.fillna(0)
    avg_load = ts[ts["date"] == date]["4_week_avg"].values[0]
    if avg_load == 0:
        avg_load = ts[ts["date"] == date]["3_week_avg"].values[0]
    if avg_load == 0:
        avg_load = ts[ts["date"] == date]["2_week_avg"].values[0]
    if avg_load == 0:
        avg_load = ts[ts["date"] == date]["weekly_avg"].values[0]

    return avg_load


def suggest_exercises(ts, date, weekly_goal, fav_activity):
    """Suggests a 7-day exercise plan for the user.

    Args:
        weekly_goal: number of training load equivalent
        fav_activity: cycling, swimming or running

    Returns:
        list of dicts containing the activity, day and duration
    """
    # strategy: suggest one (or two) days for running or swimming
    avg_load = get_weekly_avg_load(ts, date)
    with open("../data/goal_intensity_mapping.json", "r") as f:
        intensity = json.load(f)
    activities = intensity.keys()
    # select a side activity randomly
    side_activity = random.choice(list(set(activities) - set(fav_activity)))
    # aim for 10% increase on avg load
    side_activity_duration = avg_load*1.1/intensity[side_activity] + \
        random.uniform(-20, 20)
    # one day is rest day, ideally the third day
    regular_activity_load = (weekly_goal - avg_load*1.1)/5
    # below becomes a suggestion
    regular_activity_duration = regular_activity_load/intensity[fav_activity]
    # send the recommendation
    reco = {
        "day 1": {"activity": fav_activity, "duration": regular_activity_duration + random.uniform(-20, 20)},
        "day 2": {"activity": side_activity, "duration": side_activity_duration},
        "day 3": {"activity": fav_activity, "duration": regular_activity_duration + random.uniform(-20, 20)},
        "day 4": {"activity": "rest", "duration": 0},
        "day 5": {"activity": fav_activity, "duration": regular_activity_duration + random.uniform(-20, 20)},
        "day 6": {"activity": fav_activity, "duration": regular_activity_duration + random.uniform(-20, 20)},
        "day 7": {"activity": fav_activity, "duration": regular_activity_duration + random.uniform(-20, 20)},
    }
    return reco


def test_check_goal(date, weekly_goal):
    """Data ingestion, cleaning, feature engineering and evaluation of weekly
    goal.

    Args:
        date: date on which user entered the goal, usually the previous day
        data
        weekly_goal: weekly_goal in terms of training load (intensity*duration)

    Returns:
        Moderate, moderately aggressive or aggressive.
    """
    df = read_input_data()
    ts = create_time_series(df)
    # feature engineer
    ts = feature_engineer(ts, df)
    return check_goal(ts, date, weekly_goal)


def test_suggest_exercises(date, weekly_goal, fav_activity):
    """Test for exercise suggestions."""
    df = read_input_data()
    ts = create_time_series(df)
    ts = feature_engineer(ts, df)
    return suggest_exercises(ts, date, weekly_goal, fav_activity)

def test_create_time_series_secondary(file):
    df = read_input_data_secondary(file)
    ts = create_time_series(df)
    ts = feature_engineer(ts, df)
    print ts


if __name__ == "__main__":
    # test main function
    date = datetime.now() - timedelta(days=1)
    date = date.date()
    weekly_goal = 16500
    fav_activity = "cycling"
    print test_check_goal(date, weekly_goal)
    print json.dumps(test_suggest_exercises(date, weekly_goal, fav_activity), indent=4, sort_keys=True)
    #print test_create_time_series_secondary("/home/utkarsh.jain/Code/Hackathon/Sports/sportsHack/data/data_files/vivek.csv")
