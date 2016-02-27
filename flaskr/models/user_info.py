value_object = {
    "unit": None,
    "value": None,
    "value_type": None
}

LOCATION_OBJECT = {
    "longitude": None,
    "latitude": None,
    "country": None,
    "city": None,
    "state": None
}

NAME = "name"
DOB = "date_of_birth"
WEIGHT = "weight"
HEIGHT = "height"
DISEASES = "diseases"
LOCATION = "location"
TERM_ACCEPTANCE = "term_accpeptance"
USER_INFO_VAL_OBJECT_KEYS = [WEIGHT,
                             HEIGHT]

user_info_structure = {
    "name": {
        "first_name": None,
        "last_name": None
    },
    "date_of_birth": {
        "year": None,
        "month": None,
        "day": None
    },
    "weight": value_object,
    "height": value_object,
    "diseases": None,
    "location": LOCATION_OBJECT,
    "goal": None,
    "term_accpeptance": None,  # Boolean,
    "metric_file_path": None
}

WEIGHT_UNITS = ["pound",
                "kgs"]

HEIGHT_UNITS = ["cms",
                "inch",
                "meter"]
