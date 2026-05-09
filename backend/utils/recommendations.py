"""
backend/utils/recommendations.py
==================================
Clinical recommendations + full detail summary for the /summary page.

B.Tech Final Year Project (BTP) — CardioSense AI
Heart Disease Prediction Using Ensemble Machine Learning - 2026

CRITICAL NOTE FOR MAINTAINERS
-------------------------------
Never use 'items', 'values', 'keys', 'update', 'get', 'pop' as dict keys
in data passed to Jinja2 templates. These are Python built-in dict method
names. Jinja2's attribute lookup finds the method before the key, causing:
  TypeError: 'builtin_function_or_method' object is not iterable
Use 'points', 'entries', 'rows', 'steps', 'data_list' instead.
"""
from dataclasses import dataclass


@dataclass
class Recommendation:
    icon: str
    title: str
    body: str
    priority: str   # "urgent" | "moderate" | "healthy"

    def to_dict(self) -> dict:
        return {
            "icon":     self.icon,
            "title":    self.title,
            "body":     self.body,
            "priority": self.priority,
        }


# ── Quick recommendations (shown on results page) ─────────────────────────────

def build_recommendations(inputs: dict, risk_tier: str) -> list[dict]:
    recs: list[Recommendation] = []
    high = risk_tier == "high"
    mid  = risk_tier in ("medium", "high")

    recs.append(Recommendation("🥗", "Heart-Healthy Diet",
        "Adopt the Mediterranean or DASH diet. Prioritise whole grains, legumes, oily fish, "
        "olive oil, nuts, and colourful vegetables. Limit saturated fat, sodium, and added sugars.",
        "urgent" if high else "healthy"))

    recs.append(Recommendation("🏃", "Physical Activity",
        "Consult a cardiologist before starting exercise - supervised cardiac rehabilitation "
        "is strongly recommended." if high else
        "Target 150 min/week moderate aerobic exercise plus 2 days/week resistance training.",
        "urgent" if high else "healthy"))

    if inputs.get("trestbps", 0) >= 130 or mid:
        recs.append(Recommendation("💊", "Blood Pressure Control",
            f"Resting BP of {inputs.get('trestbps')} mmHg requires management. "
            "Monitor BP twice daily and reduce sodium intake.",
            "urgent" if inputs.get("trestbps", 0) >= 150 else "moderate"))

    if inputs.get("chol", 0) >= 200 or mid:
        recs.append(Recommendation("🔬", "Cholesterol Management",
            f"Cholesterol of {inputs.get('chol')} mg/dL. Request a full lipid panel. "
            "Discuss statin therapy if LDL >= 130 mg/dL.",
            "urgent" if inputs.get("chol", 0) >= 280 else "moderate"))

    if inputs.get("fbs") == 1:
        recs.append(Recommendation("🍬", "Blood Sugar Control",
            "Fasting blood sugar > 120 mg/dL. Screen for diabetes with HbA1c. "
            "Eliminate sugar-sweetened beverages and refined carbohydrates.",
            "urgent"))

    if inputs.get("exang") == 1 or inputs.get("cp") == 3 or high:
        recs.append(Recommendation("🏥", "Urgent Cardiology Referral",
            "Immediate specialist evaluation: resting + stress ECG, echocardiogram, coronary CT.",
            "urgent"))

    if inputs.get("oldpeak", 0) >= 2:
        recs.append(Recommendation("📉", "ST Depression Follow-up",
            f"ST depression of {inputs.get('oldpeak')} mm suggests ischaemia. "
            "Nuclear perfusion imaging (MPI) is recommended.",
            "urgent"))

    if inputs.get("thal") == 3:
        recs.append(Recommendation("🫀", "Perfusion Defect Follow-up",
            "Reversible thalassemia defect. Coronary angiography is warranted.",
            "urgent"))

    if inputs.get("ca", 0) >= 2:
        recs.append(Recommendation("🩺", "Multi-vessel Disease",
            f"{inputs.get('ca')} vessels flagged. Interventional cardiology review needed.",
            "urgent"))

    bmi = inputs.get("bmi")
    if bmi and bmi >= 30:
        recs.append(Recommendation("⚖️", "Weight Management",
            f"BMI {bmi:.1f} kg/m2. Target 5-10% reduction through caloric deficit and exercise.",
            "moderate" if bmi < 35 else "urgent"))

    recs.append(Recommendation("🚭", "Smoking and Alcohol",
        "Quitting smoking halves cardiac risk within 1 year. Limit alcohol to 14 units/week.",
        "urgent" if high else "moderate"))

    recs.append(Recommendation("😴", "Sleep and Stress",
        "Achieve 7-9 hours of quality sleep. Screen for sleep apnoea. "
        "Practice mindfulness or CBT for chronic stress.",
        "moderate" if mid else "healthy"))

    if mid:
        recs.append(Recommendation("📅", "Monitoring Schedule",
            "Annual: lipid panel, HbA1c, ECG. Every 6 months: BP, BMI, meds review.",
            "moderate"))

    priority_order = {"urgent": 0, "moderate": 1, "healthy": 2}
    recs.sort(key=lambda r: priority_order[r.priority])
    return [r.to_dict() for r in recs]


# ── Full detail summary (for /summary page) ────────────────────────────────────

def build_detail_summary(inputs: dict, prediction_result: dict) -> dict:
    """
    Returns the complete action-plan dict rendered by summary.html.

    KEY NAMING RULES — avoids Python dict built-in method names in Jinja2:
      USE 'points'  NOT 'items'   (dict.items is a built-in method)
      USE 'text'    NOT 'values'  (dict.values is a built-in method)
      'sign', 'timeframe', 'action', 'factor', 'level', 'icon' are all safe.
    """
    tier     = prediction_result["risk_tier"]
    prob     = prediction_result["ensemble_prob"]
    pred     = prediction_result["ensemble_pred"]
    best_mdl = prediction_result.get("best_model", {})
    high     = tier == "high"
    mid      = tier in ("medium", "high")

    # ── Immediate actions ──────────────────────────────────────────────────────
    if high:
        immediate_actions = [
            {"icon": "🚨", "text": "Call your doctor or visit a cardiology clinic within 24-48 hours."},
            {"icon": "💊", "text": "Do not start or stop cardiac medications without medical guidance."},
            {"icon": "🚫", "text": "Avoid strenuous physical exertion until cleared by a cardiologist."},
            {"icon": "📋", "text": "Prepare a medication list and symptom diary for your consultation."},
        ]
    elif mid:
        immediate_actions = [
            {"icon": "📞", "text": "Book a GP appointment within 1-2 weeks to review these results."},
            {"icon": "📏", "text": "Start measuring and recording your blood pressure daily at home."},
            {"icon": "🥗", "text": "Begin the Mediterranean or DASH diet this week."},
        ]
    else:
        immediate_actions = [
            {"icon": "✅", "text": "Schedule your annual cardiac health check-up."},
            {"icon": "🏃", "text": "Commit to the recommended 150 min/week exercise target."},
            {"icon": "📊", "text": "Maintain a health journal tracking BP, weight, and diet."},
        ]

    # ── Actions to take
    # SAFE KEY: 'points'  (NOT 'items' — that is a Python dict built-in method
    # and causes TypeError in Jinja2 when accessed as cat.items)
    actions_to_take = [
        {
            "category": "Diet",
            "icon":     "🥗",
            "points": [
                "Eat oily fish (salmon, mackerel, sardines) 2-3 times per week for omega-3 fatty acids.",
                "Increase dietary fibre to 25-35 g/day via whole grains, legumes, and vegetables.",
                "Use olive oil as primary cooking fat; avoid butter and tropical oils.",
                "Eat a handful (30 g) of unsalted nuts daily - walnuts, almonds, or pistachios.",
                "Consume 5 or more portions of fruits and vegetables daily; vary the colours.",
                "Limit red meat to 2 portions/week; avoid processed meats entirely.",
            ],
        },
        {
            "category": "Exercise",
            "icon":     "🏃",
            "points": (
                [
                    "Do NOT exercise independently until cleared by a cardiologist.",
                    "Ask your doctor about supervised cardiac rehabilitation programmes.",
                    "Light walking (10-15 min, very low intensity) only if medically approved.",
                ] if high else [
                    "Walk briskly for 30 minutes on at least 5 days per week.",
                    "Add 2 sessions/week of resistance training (bodyweight, bands, or weights).",
                    "Include flexibility and balance exercises (yoga, tai chi) twice weekly.",
                    "Monitor heart rate - target 50-70% of max HR for moderate intensity.",
                    "Consider referral to a cardiac rehabilitation class if available.",
                ]
            ),
        },
        {
            "category": "Medical",
            "icon":     "🏥",
            "points": [
                "Schedule ECG, stress test, echocardiogram, and coronary screening as advised.",
                "Request full lipid panel: LDL-C, HDL-C, non-HDL-C, triglycerides, ApoB.",
                "Screen for diabetes with fasting glucose and HbA1c.",
                "Discuss statin therapy if LDL >= 130 mg/dL.",
                "Ask your doctor about aspirin prophylaxis suitability.",
                "Review all current medications for cardiac interactions.",
            ],
        },
        {
            "category": "Lifestyle",
            "icon":     "🌿",
            "points": [
                "Quit smoking - use NRT patches, varenicline, or a stop-smoking service.",
                "Limit alcohol to 14 units/week maximum, spread over 3 or more days.",
                "Achieve 7-9 hours of quality sleep; treat snoring or sleep apnoea if present.",
                "Practice 10-20 minutes of mindfulness or deep breathing daily.",
                "Avoid prolonged sitting - stand or walk briefly every 45-60 minutes.",
                "Monitor weight weekly; target BMI 18.5-24.9 kg/m2.",
            ],
        },
    ]

    # ── Things to avoid
    # SAFE KEY: 'text'  (NOT 'values' or 'item')
    things_to_avoid = [
        {"icon": "🚬", "text": "Smoking and all tobacco or nicotine products including vaping."},
        {"icon": "🥩", "text": "Processed and cured meats: bacon, ham, hot dogs, salami, pepperoni."},
        {"icon": "🧈", "text": "Saturated fats: butter, ghee, full-fat dairy, coconut oil, palm oil."},
        {"icon": "🍟", "text": "Deep-fried foods and commercial fast food high in trans fats."},
        {"icon": "🧂", "text": "High-sodium foods: pickles, canned soups, instant noodles, ready meals."},
        {"icon": "🥤", "text": "Sugar-sweetened beverages: sodas, energy drinks, packaged fruit juices."},
        {"icon": "🍰", "text": "Refined carbohydrates: white bread, pastries, cakes, excess white rice."},
        {"icon": "🍺", "text": "Excessive alcohol - never more than 2 units on any single occasion."},
        {"icon": "💤", "text": "Chronic sleep deprivation: fewer than 6 hours per night consistently."},
        {"icon": "😤", "text": "Unmanaged chronic stress without active coping or relaxation strategies."},
        {"icon": "🏋️", "text": "High-intensity exercise without medical clearance if you are high-risk."},
        {"icon": "💊", "text": "Self-medicating with herbal or non-prescribed supplements that interact with cardiac drugs."},
    ]

    # ── Follow-up timeline ─────────────────────────────────────────────────────
    if high:
        follow_up = [
            {"timeframe": "Within 24-48 hrs", "action": "Contact cardiologist or attend urgent cardiac clinic."},
            {"timeframe": "Within 1 week",    "action": "Resting ECG, fasting blood panel, home BP monitoring setup."},
            {"timeframe": "Within 2-4 weeks", "action": "Stress test or exercise ECG, echocardiogram."},
            {"timeframe": "1-3 months",       "action": "Coronary CT angiography or nuclear perfusion imaging."},
            {"timeframe": "Every 3 months",   "action": "Cardiology review, medication titration, lifestyle audit."},
            {"timeframe": "Annually",         "action": "Comprehensive cardiac risk reassessment."},
        ]
    elif mid:
        follow_up = [
            {"timeframe": "Within 2 weeks", "action": "GP appointment to review results and arrange referrals."},
            {"timeframe": "Within 1 month", "action": "Fasting lipid panel, glucose, ECG, BP review."},
            {"timeframe": "3 months",       "action": "Follow-up: lifestyle changes and medication response."},
            {"timeframe": "6 months",       "action": "Re-screen with cardiology if risk factors persist."},
            {"timeframe": "Annually",       "action": "Full cardiac health check-up including all blood panels."},
        ]
    else:
        follow_up = [
            {"timeframe": "Within 1 month", "action": "Routine GP appointment; share these results."},
            {"timeframe": "6 months",       "action": "Recheck BP, cholesterol, and weight."},
            {"timeframe": "Annually",       "action": "Full health check: lipids, glucose, ECG, BMI."},
        ]

    # ── Warning signs ──────────────────────────────────────────────────────────
    warning_signs = [
        {"icon": "⚡", "sign": "Chest pain, pressure, tightness, or squeezing at rest or during activity"},
        {"icon": "🫁", "sign": "Sudden shortness of breath without obvious cause"},
        {"icon": "💫", "sign": "Unexplained dizziness, lightheadedness, or fainting"},
        {"icon": "💪", "sign": "Pain radiating to the left arm, jaw, neck, or back"},
        {"icon": "❤️", "sign": "Irregular, racing, or pounding heartbeat (palpitations)"},
        {"icon": "🦵", "sign": "Sudden leg swelling, especially if asymmetric"},
        {"icon": "🤢", "sign": "Unexplained nausea, cold sweats, or fatigue during minimal activity"},
    ]

    # ── Risk factors detected ──────────────────────────────────────────────────
    risk_factors = []
    if inputs.get("trestbps", 0) >= 130:
        risk_factors.append({
            "factor": "Hypertension",
            "value":  f"{inputs['trestbps']} mmHg",
            "level":  "high" if inputs["trestbps"] >= 160 else "moderate",
        })
    if inputs.get("chol", 0) >= 200:
        risk_factors.append({
            "factor": "High Cholesterol",
            "value":  f"{inputs['chol']} mg/dL",
            "level":  "high" if inputs["chol"] >= 240 else "moderate",
        })
    if inputs.get("fbs") == 1:
        risk_factors.append({"factor": "Elevated Blood Sugar", "value": "> 120 mg/dL", "level": "high"})
    if inputs.get("exang") == 1:
        risk_factors.append({"factor": "Exercise Angina",      "value": "Present",      "level": "high"})
    if inputs.get("oldpeak", 0) >= 2:
        risk_factors.append({"factor": "ST Depression",        "value": f"{inputs['oldpeak']} mm", "level": "high"})
    if inputs.get("ca", 0) >= 1:
        risk_factors.append({
            "factor": "Vessel Disease",
            "value":  f"{inputs['ca']} vessel(s)",
            "level":  "high" if inputs["ca"] >= 2 else "moderate",
        })
    if inputs.get("thal") == 3:
        risk_factors.append({"factor": "Thalassemia Defect", "value": "Reversible", "level": "high"})
    bmi = inputs.get("bmi")
    if bmi and bmi >= 30:
        risk_factors.append({
            "factor": "Obesity",
            "value":  f"BMI {bmi:.1f}",
            "level":  "high" if bmi >= 35 else "moderate",
        })
    if inputs.get("age", 0) >= 55:
        risk_factors.append({"factor": "Age Risk", "value": f"{inputs['age']} years", "level": "moderate"})
    if inputs.get("sex") == 1:
        risk_factors.append({"factor": "Male Sex", "value": "Higher baseline risk",   "level": "low"})

    return {
        "risk_tier":         tier,
        "probability":       prob,
        "prediction":        pred,
        "best_model":        best_mdl,
        "immediate_actions": immediate_actions,
        "actions_to_take":   actions_to_take,
        "things_to_avoid":   things_to_avoid,
        "follow_up":         follow_up,
        "warning_signs":     warning_signs,
        "risk_factors":      risk_factors,
        "recommendations":   build_recommendations(inputs, tier),
    }
