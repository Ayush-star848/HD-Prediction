"""tests/test_validators.py — Run: python -m pytest tests/ -v"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from backend.utils.validators import validate_inputs

BASE = dict(age=55,sex=1,cp=3,trestbps=140,chol=250,fbs=0,
            restecg=1,thalach=140,exang=1,oldpeak=2.3,slope=1,ca=1,thal=3)

def test_valid():           assert validate_inputs(BASE).is_valid
def test_missing_age():     assert not validate_inputs({k:v for k,v in BASE.items() if k!="age"}).is_valid
def test_age_out_of_range():assert not validate_inputs({**BASE,"age":200}).is_valid
def test_bad_sex():         assert not validate_inputs({**BASE,"sex":9}).is_valid
def test_string_coercion(): assert validate_inputs({**BASE,"age":"55","chol":"240"}).is_valid
def test_model_selection():
    r = validate_inputs({**BASE,"selected_models":["xgboost","random_forest"]})
    assert r.is_valid and r.cleaned["selected_models"] == ["xgboost","random_forest"]
def test_bad_model():
    assert not validate_inputs({**BASE,"selected_models":["fake_model"]}).is_valid
