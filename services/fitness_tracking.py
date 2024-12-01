from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def analyze_trends(data: pd.DataFrame) -> List[Dict[str, float | str]]:
    # Group by week and calculate weekly aggregates
    weekly_data = (
        data.groupby("week")
        .agg(
            start_date=("date", "min"),  # Get the earliest date of the week
            average_steps=("steps", "mean"),
            average_calories=("calories", "mean"),
            average_active_minutes=("active_minutes", "mean"),
        )
        .reset_index()
    )
    # Round the averages to 0 decimal places
    weekly_data["average_steps"] = weekly_data["average_steps"].round(0)
    weekly_data["average_calories"] = weekly_data["average_calories"].round(0)
    weekly_data["average_active_minutes"] = weekly_data["average_active_minutes"].round(
        0
    )

    # Calculate weekly percentage changes
    weekly_data["weekly_steps_change"] = (
        weekly_data["average_steps"].pct_change() * 100
    ).map(lambda x: f"{x:.0f}%")
    weekly_data["weekly_calories_change"] = (
        weekly_data["average_calories"].pct_change() * 100
    ).map(lambda x: f"{x:.0f}%")
    weekly_data["weekly_active_minutes_change"] = (
        weekly_data["average_active_minutes"].pct_change() * 100
    ).map(lambda x: f"{x:.0f}%")

    # Replace "week" with the start date as the key
    weekly_data["week"] = weekly_data["start_date"].dt.strftime("%Y-%m-%d")
    weekly_data.drop(
        columns=["start_date"], inplace=True
    )  # Drop the intermediate column

    weekly_data = weekly_data.to_dict("records")

    return weekly_data


def generate_recommendations(
    trends: List[Dict[str, float]], step_goal: int = 10000
) -> List[str]:
    recommendations = []

    # Get data for the last week
    last_week = trends[-1]
    previous_week = trends[-2] if len(trends) > 1 else None

    # Steps ratio
    steps_ratio = last_week["average_steps"] / step_goal

    # Recommendations based on steps ratio
    if steps_ratio < 0.8:
        recommendations.append(
            "You're reaching 80% of your weekly step goal. Try adding 2,000 more steps daily."
        )
    elif steps_ratio < 1.0:
        recommendations.append(
            "You're close to your step goal. Add 500 steps daily to exceed it!"
        )
    else:
        recommendations.append(
            "Great job on meeting your step goal! Consider adding strength or flexibility exercises."
        )

    # Weekly active minutes
    if last_week["average_active_minutes"] < 150:
        recommendations.append(
            "Increase your weekly active minutes by 10% to meet the recommended 150 minutes."
        )

    # Percentage changes in activity compared to the previous week
    if previous_week:
        step_change = last_week["weekly_steps_change"]
        calorie_change = last_week["weekly_calories_change"]
        active_minutes_change = last_week["weekly_active_minutes_change"]

        recommendations.append(
            f"In the last week, your steps changed by {step_change}, "
            f"calories burned changed by {calorie_change}, and active minutes changed by {active_minutes_change}."
        )

    return recommendations


def predict_calories(data: pd.DataFrame, prediction_data: Dict[str, int]) -> int:
    # Prepare features and target
    data["day_of_week"] = data["date"].dt.dayofweek
    X = data[["day_of_week", "active_minutes", "steps"]]
    y = data["calories"]

    # Train regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict steps for the next day (e.g., day_of_week=5, active_minutes=60, steps=8000)
    day_of_week, active_minutes, steps = (
        prediction_data.day_of_week,
        prediction_data.active_minutes,
        prediction_data.steps,
    )
    next_day_features = np.array([[day_of_week, active_minutes, steps]])
    predicted_calories = model.predict(next_day_features)[0]
    return int(predicted_calories)
