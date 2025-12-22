# slis/matching/__init__.py
from .names import normalize_name, calculate_advanced_name_score
from .dob import parse_dob, calculate_dob_score_flexible
from .geo import generate_geographic_insights, HIGH_RISK_JURISDICTIONS, REGIONAL_BLOCS
from .utils import normalize_and_compare
from .engine import run_screening_engine

__all__ = [
    "normalize_name",
    "calculate_advanced_name_score",
    "parse_dob",
    "calculate_dob_score_flexible",
    "generate_geographic_insights",
    "HIGH_RISK_JURISDICTIONS",
    "REGIONAL_BLOCS",
    "normalize_and_compare",
    "run_screening_engine",
]
