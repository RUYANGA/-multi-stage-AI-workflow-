import json
from pathlib import Path
from validator import validate_email


def load_spec():
    spec_path = Path(__file__).parent / "spec.json"
    return json.loads(spec_path.read_text())


def test_cases_from_spec():
    spec = load_spec()
    for case in spec["test_cases"]:
        result = validate_email(case["input"])
        assert result["is_valid"] == case["is_valid"], (
            f"Mismatch for {case['input']}: expected {case['is_valid']}, "
            f"got {result}"
        )


def test_reason_present_when_invalid():
    result = validate_email("bad@@address.com")
    assert result["is_valid"] is False
    assert result["reason"] is not None


    
