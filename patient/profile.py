from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class PatientProfile:
    name: str = ""
    age: int = 0
    gender: str = ""
    height_cm: float = 0.0
    weight_kg: float = 0.0
    diet_preference: str = ""
    activity_level: str = ""
    sleep_time: str = ""
    known_condition: str = ""
    medications: str = ""
    allergies: str = ""


def create_profile(
    name: str = "",
    age: int = 0,
    gender: str = "",
    height_cm: float = 0.0,
    weight_kg: float = 0.0,
    diet_preference: str = "",
    activity_level: str = "",
    sleep_time: str = "",
    known_condition: str = "",
    medications: str = "",
    allergies: str = "",
) -> PatientProfile:
    """Create a structured patient profile object."""
    return PatientProfile(
        name=name,
        age=age,
        gender=gender,
        height_cm=height_cm,
        weight_kg=weight_kg,
        diet_preference=diet_preference,
        activity_level=activity_level,
        sleep_time=sleep_time,
        known_condition=known_condition,
        medications=medications,
        allergies=allergies,
    )


def profile_to_dict(profile: PatientProfile) -> dict:
    """Convert a PatientProfile object to a dictionary."""
    return asdict(profile)


def calculate_bmi(weight_kg: float, height_cm: float) -> Optional[float]:
    """Calculate BMI from weight and height. Return None if height is invalid."""
    if height_cm <= 0:
        return None

    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 2)


def bmi_category(bmi: Optional[float]) -> str:
    """Return a simple BMI category."""
    if bmi is None:
        return "Unknown"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"
