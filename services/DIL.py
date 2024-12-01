import pandas as pd

# Constants for normalization
STEP_GOAL = 10000
HEART_RATE_MIN = 60
HEART_RATE_MAX = 200
SLEEP_MIN = 7
SLEEP_MAX = 9
HRV_MIN = 20
HRV_MAX = 100


def process_health_metrics(data: pd.DataFrame):
    """
    Accept health metrics as a DataFrame, normalize the data, and return it rounded to 1 decimal place.
    """
    # Normalize each column
    data["steps_normalized"] = data["steps"] / STEP_GOAL
    data["heart_rate_normalized"] = (data["heart_rate"] - HEART_RATE_MIN) / (
        HEART_RATE_MAX - HEART_RATE_MIN
    )
    data["sleep_normalized"] = (data["sleep_hours"] - SLEEP_MIN) / (
        SLEEP_MAX - SLEEP_MIN
    )
    data["hrv_normalized"] = (data["hrv"] - HRV_MIN) / (HRV_MAX - HRV_MIN)

    # Handle edge cases
    # Clip only numeric columns
    numeric_columns = [
        "steps_normalized",
        "heart_rate_normalized",
        "sleep_normalized",
        "hrv_normalized",
    ]
    data[numeric_columns] = data[numeric_columns].clip(0, 1)

    # Return normalized data
    return data.to_dict(orient="records")
