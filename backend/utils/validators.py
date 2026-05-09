"""
backend/utils/validators.py
============================
Input validation & sanitisation for prediction requests.
"""
from dataclasses import dataclass, field

RULES: dict = {
    "age":      {"type": "int",   "min": 18,  "max": 100},
    "sex":      {"type": "int",   "choices": [0, 1]},
    "cp":       {"type": "int",   "choices": [0, 1, 2, 3]},
    "trestbps": {"type": "int",   "min": 80,  "max": 220},
    "chol":     {"type": "int",   "min": 100, "max": 600},
    "fbs":      {"type": "int",   "choices": [0, 1]},
    "restecg":  {"type": "int",   "choices": [0, 1, 2]},
    "thalach":  {"type": "int",   "min": 60,  "max": 220},
    "exang":    {"type": "int",   "choices": [0, 1]},
    "oldpeak":  {"type": "float", "min": 0.0, "max": 6.2},
    "slope":    {"type": "int",   "choices": [0, 1, 2]},
    "ca":       {"type": "int",   "choices": [0, 1, 2, 3]},
    "thal":     {"type": "int",   "choices": [1, 2, 3]},
}

REQUIRED = list(RULES.keys())

VALID_MODELS = {
    "logistic_regression", "random_forest", "svm", "xgboost",
    "gradient_boosting", "knn", "naive_bayes", "decision_tree", "voting_ensemble",
}


@dataclass
class ValidationResult:
    is_valid: bool
    errors:   list = field(default_factory=list)
    cleaned:  dict = field(default_factory=dict)


def validate_inputs(payload: dict) -> ValidationResult:
    errors, cleaned = [], {}
    for feat in REQUIRED:
        if feat not in payload:
            errors.append(f"Missing required field: '{feat}'")
            continue
        rule = RULES[feat]
        try:
            val = int(payload[feat]) if rule["type"] == "int" else float(payload[feat])
        except (ValueError, TypeError):
            errors.append(f"'{feat}' must be {rule['type']} (got {repr(payload[feat])})")
            continue
        if "choices" in rule and val not in rule["choices"]:
            errors.append(f"'{feat}' must be one of {rule['choices']}")
            continue
        if "min" in rule and val < rule["min"]:
            errors.append(f"'{feat}' must be ≥ {rule['min']}")
            continue
        if "max" in rule and val > rule["max"]:
            errors.append(f"'{feat}' must be ≤ {rule['max']}")
            continue
        cleaned[feat] = val

    sel = payload.get("selected_models")
    if sel is not None:
        if not isinstance(sel, list):
            errors.append("'selected_models' must be a list")
        else:
            bad = [m for m in sel if m not in VALID_MODELS]
            if bad:
                errors.append(f"Unknown model(s): {bad}")
            else:
                cleaned["selected_models"] = sel

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, cleaned=cleaned)
