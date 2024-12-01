from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException

from models.models import *
from services import preprocess_data
from services.DIL import process_health_metrics
from services.fitness_tracking import *
from services.IAL import aggregated_insights
from services.journaling_sentiment import *
from services.sleep_analysis import *

# Initialize FastAPI app
app = FastAPI()

# In-memory database for user data
user_data_store: Dict[str, Dict[str, Any]] = {}


@app.get("/")
@app.post("/")
def ping():
    """
    Ping endpoint to check if the API is running.
    """
    return {"message": "Welcome to the AI Fitness API"}


@app.post("/api/health-metrics")
def health_metrics(data: HealthData):
    """
    Process and normalize health metrics data for a user.
    """
    user_id = data.user_id
    health_data = preprocess_data(data.metrics)
    normalized_health_data = process_health_metrics(health_data)

    # Update in-memory data store
    user_data_store.setdefault(user_id, {})["health_data"] = {
        "health_data": health_data,
    }

    return {"Health Data": normalized_health_data}


@app.post("/api/fitness-tracking")
def fitness_tracking(data: FitnessData):
    """
    Analyze weekly fitness trends and provide recommendations.
    """
    user_id = data.user_id
    activity_data = preprocess_data(data.activity)
    weekly_trends = analyze_trends(activity_data)
    recommendations = generate_recommendations(weekly_trends)

    # Update in-memory data store
    user_data_store.setdefault(user_id, {})["fitness_data"] = {
        "weekly_trends": weekly_trends,
        "recommendations": recommendations,
    }

    return {"Weekly Trends": weekly_trends, "Recommendations": recommendations}


@app.post("/api/fitness-tracking/predict")
def fitness_predict(data: FitnessData, prediction_data: PredictionData):
    """
    Predict user next day volume of burned calories from past fitness history
    """
    activity_data = preprocess_data(data.activity)
    prediction = predict_calories(data=activity_data, prediction_data=prediction_data)

    return {"Predicted Calories": prediction}


@app.post("/api/sleep-analysis")
def sleep_analysis(data: SleepData):
    """
    Analyze sleep patterns and generate personalized recommendations.
    """
    user_id = data.user_id
    sleep_data = preprocess_data(data.activity)
    sleep_patterns = analyze_sleep_patterns(sleep_data)
    recommendations = generate_sleep_recommendations(sleep_patterns)

    # Update in-memory data store
    user_data_store.setdefault(user_id, {})["sleep_data"] = {
        "sleep_patterns": sleep_patterns,
        "recommendations": recommendations,
    }

    return {"Sleep Patterns": sleep_patterns, "Recommendations": recommendations}


@app.post("/api/journal-sentiment")
def journal_sentiment(data: JournalData):
    """
    Analyze journal entries for sentiment and provide feedback.
    """
    user_id = data.user_id
    journal_entries = preprocess_data(data.journal_entries)
    summary = sentiment_summary(journal_entries)
    feedback = generate_feedback(summary)

    # Update in-memory data store
    user_data_store.setdefault(user_id, {})["journal_sentiment"] = {
        "summary": summary,
        "feedback": feedback,
    }

    return {"Sentiment Summary": summary, "Feedback": feedback}


@app.get("/api/aggregated-insights/{user_id}")
def get_aggregated_insights(user_id: str):
    """
    Retrieve aggregated insights for a specific user.
    """
    if user_id not in user_data_store:
        raise HTTPException(status_code=404, detail="User data not found.")

    # Gather all user data
    user_data = user_data_store[user_id]
    aggregated_data = aggregated_insights(user_data)

    return {"Aggregated Insights": aggregated_data}


if __name__ == "__main__":
    uvicorn.run(app=app, port=8080, host="127.0.0.1")
