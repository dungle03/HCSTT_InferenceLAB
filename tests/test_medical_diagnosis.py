"""Integration tests for the medical diagnosis API.

These tests spin up the Flask application and exercise the
`/medical/api/diagnose` endpoint with representative symptom payloads.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pytest

import sys


def _ensure_project_root_on_path() -> None:
    project_root = Path(__file__).resolve().parents[1]
    root_str = str(project_root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


_ensure_project_root_on_path()

from web import create_app


@pytest.fixture()
def client(tmp_path: Path):
    """Provide a Flask test client with an isolated graph output directory."""

    app = create_app()
    app.config.update(
        TESTING=True,
        GRAPH_OUTPUT_ROOT=tmp_path,
    )

    with app.test_client() as test_client:
        yield test_client


def _post_diagnosis(client, payload: Dict[str, object]):
    response = client.post("/medical/api/diagnose", json=payload)
    assert response.status_code == 200, response.get_data(as_text=True)

    data = response.get_json()
    assert data, "Response JSON must not be empty"
    assert data.get("ok"), f"Diagnosis failed: {data}"
    return data


def test_severe_upper_respiratory_symptoms_surface_pharyngitis(client):
    """Respiratory symptoms with throat pain should surface viêm họng diagnosis."""

    payload = {
        "tuoi": 28,
        "gioi_tinh": "nam",
        "nhiet_do": 39.1,
        "ho": True,
        "loai_ho": "khan",
        "met_moi": True,
        "dau_hong": True,
        "mat_vi_giac": True,
        "mat_khu_giac": True,
        "spo2": 93,
    }

    data = _post_diagnosis(client, payload)

    diagnosis = data["diagnosis"]
    assert diagnosis["disease"] == "viem_hong"
    assert diagnosis["confidence"] >= 40.0

    top_codes = {item["disease"] for item in data.get("top_diagnoses", [])}
    assert "viem_hong" in top_codes


def test_digestive_symptoms_rank_food_poisoning_or_gastritis_highest(client):
    """Digestive-centric symptoms should favour GI-related diagnoses."""

    payload = {
        "tuoi": 32,
        "gioi_tinh": "nu",
        "nhiet_do": 37.8,
        "dau_bung": True,
        "buon_non": True,
        "tieu_chay": True,
        "met_moi": True,
    }

    data = _post_diagnosis(client, payload)

    top_diagnoses = data.get("top_diagnoses", [])
    assert top_diagnoses, "Expected at least one ranked diagnosis"

    primary = top_diagnoses[0]
    assert primary["disease"] in {"ngo_doc_thuc_pham", "viem_da_day"}
    assert primary["confidence"] >= 20.0

    digestives = {item["disease"] for item in top_diagnoses}
    assert {"ngo_doc_thuc_pham", "viem_da_day"} & digestives
