import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def read_input_data():
    """Converts input csv file to pandas dataframe."""
    df = pd.read_csv("../data/training_load_data.csv", skiprows=1,
                     names=["date", "status", "session_time", "type",
                            "duration", "rpe", "session_load"],
                     parse_dates=["date"])
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
    # offset date
    ts["date"] = pd.DatetimeIndex(ts["date"]) + pd.DateOffset(days=446)
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


def main(date, weekly_goal):
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


if __name__ == "__main__":
    # test main function
    date = datetime.now() - timedelta(days=1)
    date = date.date()
    weekly_goal = 16500
    print main(date, weekly_goal)
