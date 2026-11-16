import pytest

from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds,
)


def test_invalid_wards():
    with pytest.raises(ValueError):
        process_triage_wards("invalid", 10)


def test_non_accepting_ward():
    result = process_triage_wards(
        [{"is_accepting": False}],
        10
    )

    assert result == {
        "acuity_score": 0,
        "status": "NO_URGENT_CASES"
    }


def test_general_mixed_with_icu():
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": True,
            "patients": [
                {"spo2": 0, "hr": 70},
                {"spo2": 95, "hr": 75, "unconscious": True},
                {"spo2": 89, "hr": 80},
                {"spo2": 98, "hr": 72},
            ],
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result == {
        "acuity_score": 195,
        "status": "TRIAGE_STABLE"
    }


def test_outpatient_break_with_icu():
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "icu_standby": True,
            "patients": [
                {"spo2": 98, "hr": 72},
                {"spo2": 95, "hr": 75, "unconscious": True},
            ],
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result == {
        "acuity_score": 25,
        "status": "TRIAGE_STABLE"
    }


def test_ward_alert_with_icu():
    wards = [
        {
            "is_accepting": True,
            "icu_standby": True,
            "patients": [
                {"spo2": 0, "hr": 70},
                {"spo2": 0, "hr": 70},
                {"spo2": 0, "hr": 70},
                {"spo2": 0, "hr": 70},
                {"spo2": 0, "hr": 70},
            ],
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result == {
        "acuity_score": 25,
        "status": "WARD_ALERT"
    }


def test_empty_wards_no_urgent():
    result = process_triage_wards([], 10)

    assert result == {
        "acuity_score": 0,
        "status": "NO_URGENT_CASES"
    }


def test_oxygen_no_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_oxygen_failure():
    assert monitor_oxygen_manifolds(
        [[5.0, 3.8, 3.7]]
    ) == "PRESSURE_FAILURE"


def test_oxygen_normal():
    assert monitor_oxygen_manifolds(
        [[5.0]]
    ) == "PRESSURE_NORMAL"


def test_multiple_wards_continue_outer_loop():
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [
                {
                    "spo2": 98,
                    "hr": 72,
                    "unconscious": False
                }
            ],
        },
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [
                {
                    "spo2": 89,
                    "hr": 80,
                    "unconscious": False
                }
            ],
        },
    ]

    result = process_triage_wards(wards, 10)

    assert result == {
        "acuity_score": 70,
        "status": "TRIAGE_STABLE"
    }