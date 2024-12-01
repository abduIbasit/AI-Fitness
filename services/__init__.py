from typing import Dict, List

import pandas as pd


# Load and preprocess data as pandas dataframe
def preprocess_data(activity_data: List[Dict]):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame([dict(entry) for entry in activity_data])

    df["date"] = pd.to_datetime(df["date"])  # Convert dates to datetime
    df = df.sort_values(by="date")  # Sort by date

    # Assign each entry to a week starting from the earliest date
    df["week"] = (df["date"] - df["date"].min()).dt.days // 7 + 1

    return df
