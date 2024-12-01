from dotenv import load_dotenv
from groq import Groq
from utils import FitnessCoach

load_dotenv()

fitness_coach = FitnessCoach(model="llama3-8b-8192", client=Groq())


def aggregated_insights(information):
    """
    Analyze multiple data insights and generate holistic fitness recommendations.

    This function leverages a professional fitness coach AI model to provide actionable advice
    for users based on data insights such as sleep quality, stress levels, and fitness activity.

    Parameters:
    ----------
    information : dict
        A dictionary containing the user's health and fitness data, including
        metrics like sleep quality, stress levels, and physical activity.

    Returns:
    -------
    str
        A string containing the AI-generated recommendation or an error message
        in case of a failure.

    Process:
    -------
    1. Creates a system prompt that sets the context for the AI as a fitness coach.
    2. Creates a user prompt containing the user's health and fitness data.
    3. Calls the `fitness_coach.generate_completion` method to generate insights.
    4. Handles any exceptions that may arise during the process and returns
       an appropriate error message.

    Example:
    -------
    Input:
        information = {
            "sleep_quality": "good",
            "stress_levels": "moderate",
            "fitness_activity": "high"
        }

    Output:
        "Based on your good sleep quality, moderate stress levels, and high fitness activity,
        I recommend maintaining your current activity levels while integrating relaxation exercises
        to further reduce stress."
    """
    system_prompt = (
        "You are a professional fitness coach. Your role is to analyze multiple data insights "
        "such as sleep quality, stress levels, and fitness activity, and provide a holistic "
        "recommendation. Format your response with actionable advice for the user."
    )
    user_prompt = (
        f"Provide a holistic recommendation based on the following data:\n{information}"
    )

    try:
        response = fitness_coach.generate_completion(system_prompt, user_prompt)
        return response
    except Exception as e:
        return f"Error generating insights: {e}"
