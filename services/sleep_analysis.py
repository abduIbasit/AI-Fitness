from typing import Dict, List

import pandas as pd
from prophet import Prophet


def analyze_sleep_patterns(data: pd.DataFrame) -> List[Dict[str, float]]:
    # Group by week
    data["week"] = (
        data["date"].dt.to_period("W").apply(lambda r: r.start_time)
    )  # Get week start date
    weekly_data = (
        data.groupby("week")
        .agg(
            start_date=("week", "first"),
            avg_duration=("duration", "mean"),
            avg_disturbances=("disturbances", "mean"),
            below_min_duration=(
                "duration",
                lambda x: (x < 6).sum(),
            ),  # Count days < 6 hours
        )
        .reset_index(drop=True)
    )

    weekly_data["start_date"] = weekly_data["start_date"].dt.strftime("%Y-%m-%d")
    return weekly_data.to_dict("records")


def generate_sleep_recommendations(trends: List[Dict[str, float]]) -> List[str]:
    recommendations = []

    # Analyze the most recent week
    last_week = trends[-1]  # Get data for the most recent week
    avg_duration = last_week["avg_duration"]
    avg_disturbances = last_week["avg_disturbances"]
    below_min_duration = last_week["below_min_duration"]

    # Sleep duration recommendations
    if avg_duration < 6:
        recommendations.append(
            "Your average sleep time has dropped below 6 hours. Consider a consistent bedtime routine."
        )
    elif avg_duration < 7:
        recommendations.append(
            "You're close to the recommended 7–8 hours of sleep. Try to sleep a little earlier."
        )
    else:
        recommendations.append("Great job maintaining good sleep duration!")

    # Sleep disturbances recommendations
    if avg_disturbances > 2:
        recommendations.append(
            "You have frequent sleep disturbances. Consider reducing screen time before bed or trying relaxation techniques."
        )

    # Below minimum permissible duration report
    if below_min_duration > 1:
        recommendations.append(
            f"Sleep duration was less than 6 hours {below_min_duration} times in the last week. "
            "Consider improving your sleep quality by reducing caffeine intake or establishing a relaxing bedtime ritual."
        )

    # Multi-week trend analysis
    if len(trends) > 1:
        prev_week = trends[-2]  # Get data for the previous week
        prev_below_min = prev_week["below_min_duration"]
        recommendations.append(
            f"In the past two weeks, sleep duration was less than 6 hours "
            f"{below_min_duration + prev_below_min} times in total. Focus on consistent sleep habits."
        )

    return recommendations


def predict_sleep_duration(data: pd.DataFrame) -> float:
    # Prepare data for Prophet
    df_prophet = data[["date", "duration"]].rename(
        columns={"date": "ds", "duration": "y"}
    )

    # Initialize and fit model
    model = Prophet()
    model.fit(df_prophet)

    # Forecast next day
    future = model.make_future_dataframe(periods=1)
    forecast = model.predict(future)
    predicted_duration = forecast.iloc[-1]["yhat"]
    return round(predicted_duration, 0)
