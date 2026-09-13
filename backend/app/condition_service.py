from __future__ import annotations
import random

CONDITIONS = [
    {"name": "Mauvais état", "key": "bad", "multiplier": 0.45},
    {"name": "État moyen", "key": "worn", "multiplier": 0.65},
    {"name": "État correct", "key": "field", "multiplier": 0.85},
    {"name": "Bon état", "key": "minimal", "multiplier": 1.00},
    {"name": "Comme neuf", "key": "factory", "multiplier": 1.35},
]

def _quality_bias(case_price: float) -> float:
    # expensive cases can very slightly improve the condition profile
    return max(0.0, min(1.0, (float(case_price or 0)-100.0)/(5000.0-100.0)))

def condition_distribution(case_price: float = 100.0) -> list[dict]:
    bias = _quality_bias(case_price)
    weights = [
        44.0 - 18.0*bias,
        27.0 - 8.0*bias,
        18.0 + 1.0*bias,
        9.0 + 7.0*bias,
        2.0 + 18.0*bias,
    ]
    total = sum(weights) or 1.0
    return [{**row, 'probability': weight / total * 100.0} for row, weight in zip(CONDITIONS, weights)]

def roll_condition(case_price: float = 100.0) -> dict:
    distribution = condition_distribution(case_price)
    picked = random.choices(distribution, weights=[row['probability'] for row in distribution], k=1)[0]
    return picked.copy()

def condition_multiplier(condition: str | None) -> float:
    for row in CONDITIONS:
        if row["name"] == condition or row["key"] == condition:
            return float(row["multiplier"])
    return 0.65

def effective_value(base_value: float, condition: str | None) -> float:
    # Keep cheap junk around 1€ even in its worst state.
    value=max(1.0, float(base_value or 0.0) * condition_multiplier(condition))
    return round(value, 2)
