"""Util and helper functions for analyzing data."""

import pymongo as pm

def get_calories_estimate(activity, weight):
    """Calculates the calories expenditure for an activity, which depends on
    the weight of a person.

    Args:
        activity: activity available in the database, examples are running,
        cycling, swimming, etc.
        weight: weight of the person in lbs
    """
    doc = get_calorie_details(activity)
    if weight < 155:
        slope = (doc["lb155"] - doc["lb130"])/(155-130)
        x0 = 130
        y0 = doc["lb130"]
    elif 155 < weight < 180:
        slope = (doc["lb180"] - doc["lb155"])/(180-155)
        x0 = 155
        y0 = doc["lb155"]
    elif 180 < weight:
        slope = (doc["lb205"] - doc["lb180"])/(205-180)
        x0 = 180
        y0 = doc["lb180"]
    calorie = slope*(weight-x0) + y0
    return calorie


def get_calorie_details(activity):
    """Get calorie values for standard weights for a given activity from the
    db.

    Args:
        activity: activity available in the database, examples are running,
        cycling, swimming, etc.
    Returns:
        dict containing standard calorie values
    """
    client = pm.MongoClient("localhost", 27017)
    col = client["sports_hack"]["exercise_list"]
    doc = col.find_one({"exercise": activity})
    return doc

def test_get_calorie_details(activity):
    print get_calorie_details(activity)

def test_get_calories_estimate(activity, weight):
    print get_calories_estimate(activity, weight)

if __name__ == "__main__":
    test_get_calorie_details("Aerobics, low impact")
    test_get_calories_estimate("Aerobics, low impact", 215)
