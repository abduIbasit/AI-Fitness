from typing import List

from pydantic import BaseModel


class HealthMetric(BaseModel):
    date: str
    steps: int
    heart_rate: int
    sleep_hours: float
    hrv: int


class HealthData(BaseModel):
    user_id: str
    metrics: List[HealthMetric]


class FitnessActivity(BaseModel):
    date: str
    steps: int
    calories: int
    active_minutes: int


class FitnessData(BaseModel):
    user_id: str
    activity: List[FitnessActivity]


class PredictionData(BaseModel):
    day_of_week: int
    active_minutes: int
    steps: int


class SleepMetrics(BaseModel):
    date: str
    duration: float
    disturbances: int


class SleepData(BaseModel):
    user_id: str
    activity: List[SleepMetrics]


class JournalEntries(BaseModel):
    date: str
    entry: str


class JournalData(BaseModel):
    user_id: str
    journal_entries: List[JournalEntries]
