import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(entry):
    scores = analyzer.polarity_scores(entry)
    compound = scores["compound"]
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"


def sentiment_summary(data: pd.DataFrame):
    # Keep only the last 10 journal entries if there are more than 10
    if len(data) > 10:
        data = data.iloc[-10:]

    data["sentiment"] = data["entry"].apply(analyze_sentiment)

    # Step 3: Summarize emotional trends
    sentiment_summary = data["sentiment"].value_counts(normalize=True) * 100
    sentiment_summary = sentiment_summary.to_dict()

    return sentiment_summary


def generate_feedback(summary):
    feedback = []
    if summary.get("negative", 0) > 50:
        feedback.append(
            "Your recent journal entries reflect sadness or negativity. Would you like some tips for managing negative emotions?"
        )
    elif summary.get("positive", 0) > 70:
        feedback.append(
            "Your journal entries are mostly positive. Keep up the great mindset!"
        )
    else:
        feedback.append(
            "Your journal entries are balanced between positive and negative tones. Continue journaling to track your emotional well-being."
        )
    return feedback
