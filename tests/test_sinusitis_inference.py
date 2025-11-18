"""Domain-focused tests for the sinusitis knowledge base.

These checks assert that representative patient profiles trigger the
intended sinusitis diagnoses and that structured recommendations remain
available for downstream UI rendering.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Optional, Sequence, Tuple

import pytest

import sys


def _ensure_project_root_on_path() -> None:
    project_root = Path(__file__).resolve().parents[1]
    root_str = str(project_root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


_ensure_project_root_on_path()

from inference_lab.forward import run_forward_inference
from medical_kb import MedicalKnowledgeBase, extract_facts_from_form


@pytest.fixture(scope="module")
def sinusitis_kb() -> MedicalKnowledgeBase:
    """Load the dedicated sinusitis knowledge base once for all tests."""

    return MedicalKnowledgeBase(kb_path="data/sinusitis_kb.json")


def _infer_diagnosis(
    kb: MedicalKnowledgeBase,
    answers: Dict[str, object],
    goals: Optional[Sequence[str]] = None,
) -> Tuple[Iterable[str], Iterable[str], object]:
    """Utility that performs fact extraction and forward inference."""

    facts = extract_facts_from_form(answers, kb)
    goal_atoms = (
        list(goals) if goals else [item["variable"] for item in kb.get_diseases()]
    )

    result = run_forward_inference(
        kb.kb,
        initial_facts=facts,
        goals=goal_atoms,
        strategy="stack",
        index_mode="min",
        make_graphs=False,
    )

    if goals:
        assert result.success, (
            "Inference failed for targeted goals."
            f" goals={goal_atoms} answers={answers} extracted={facts} steps={len(result.history)}"
        )

    return result.final_facts, facts, result


SCENARIOS = [
    pytest.param(
        {
            "disease": "viem_xoang_cap_do_virus",
            "answers": {
                "thoi_gian_trieu_chung": 6,
                "nghet_mui": True,
                "loai_dich_mui": "Trong, loãng",
                "dau_vung_xoang_ham": True,
                "dau_nang_mat": True,
                "giam_khuu_giac": True,
                "nhiet_do": 37.8,
            },
            "expected_facts": {
                "viem_xoang_cap",
                "viem_xoang_cap_do_virus",
                "co_bang_chung_thoi_gian_cap",
                "co_bang_chung_dich_cap",
                "dieu_kien_cap_day_du",
            },
            "expected_severity": "Mild",
        },
    ),
    pytest.param(
        {
            "disease": "viem_xoang_cap_do_vi_khuan",
            "answers": {
                "thoi_gian_trieu_chung": 12,
                "nghet_mui": True,
                "loai_dich_mui": "Đặc, vàng/xanh",
                "dau_vung_xoang_ham": True,
                "dau_nang_mat": True,
                "giam_khuu_giac": True,
                "nhiet_do": 38.9,
                "trieu_chung_nang_len_sau_5_ngay": True,
            },
            "expected_facts": {
                "viem_xoang_cap",
                "viem_xoang_cap_do_vi_khuan",
                "co_bang_chung_thoi_gian_cap",
                "co_bang_chung_dich_cap",
                "dieu_kien_cap_day_du",
            },
            "expected_severity": "Moderate",
        },
    ),
    pytest.param(
        {
            "disease": "viem_xoang_tai_phat",
            "answers": {
                "thoi_gian_trieu_chung": 9,
                "nghet_mui": True,
                "loai_dich_mui": "Đặc, vàng/xanh",
                "dau_vung_xoang_ham": True,
                "dau_nang_mat": True,
                "giam_khuu_giac": True,
                "tai_phat_nhieu_lan": True,
            },
            "expected_facts": {
                "viem_xoang_cap",
                "viem_xoang_tai_phat",
                "co_bang_chung_thoi_gian_cap",
                "co_bang_chung_dich_cap",
                "dieu_kien_cap_day_du",
            },
            "expected_severity": "Moderate",
        },
    ),
    pytest.param(
        {
            "disease": "viem_xoang_man_tinh",
            "answers": {
                "thoi_gian_trieu_chung": 140,
                "nghet_mui": True,
                "dau_vung_xoang_tran": True,
                "giam_khuu_giac": True,
                "co_polyp_mui": True,
            },
            "expected_facts": {"viem_xoang_man_tinh", "viem_xoang_man_tinh_co_polyp"},
            "expected_severity": "Moderate",
        },
    ),
    pytest.param(
        {
            "disease": "viem_xoang_do_nam",
            "answers": {
                "thoi_gian_trieu_chung": 200,
                "nghet_mui": True,
                "dau_vung_xoang_ham": True,
                "dau_nang_mat": True,
                "suy_giam_mien_dich": True,
                "giam_khuu_giac": True,
            },
            "expected_facts": {"viem_xoang_man_tinh", "viem_xoang_do_nam"},
            "expected_severity": "Severe",
        },
    ),
    pytest.param(
        {
            "disease": "nguy_co_bien_chung",
            "answers": {
                "thoi_gian_trieu_chung": 11,
                "nghet_mui": True,
                "dau_vung_xoang_ham": True,
                "dau_nang_mat": True,
                "loai_dich_mui": "Đặc, vàng/xanh",
                "nhiet_do": 39.7,
                "dau_dau_du_doi": True,
                "sung_quanh_mat": True,
            },
            "expected_facts": {
                "viem_xoang_cap",
                "nguy_co_bien_chung",
                "co_bang_chung_thoi_gian_cap",
                "co_bang_chung_dich_cap",
                "dieu_kien_cap_day_du",
            },
            "expected_severity": "Critical",
        },
    ),
]


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_forward_inference_matches_medical_expectation(
    sinusitis_kb: MedicalKnowledgeBase,
    scenario: Dict[str, object],
) -> None:
    """Ensure canonical patient archetypes trigger the right diagnosis."""

    expected_facts = scenario["expected_facts"]
    final_facts, facts, result = _infer_diagnosis(
        sinusitis_kb,
        scenario["answers"],
        goals=list(expected_facts),
    )
    missing = set(expected_facts) - set(final_facts)
    assert not missing, (
        "Inference missed expected facts"
        f" missing={missing} facts={final_facts} initial={facts} steps={len(result.history)}"
    )

    disease = scenario["disease"]
    info = sinusitis_kb.get_disease_info(disease)
    assert info is not None, f"Metadata missing for disease {disease}"
    assert (
        info.get("severity") == scenario["expected_severity"]
    ), f"Unexpected severity for {disease}: {info}"


@pytest.mark.parametrize(
    "disease",
    [
        "viem_xoang_cap_do_virus",
        "viem_xoang_cap_do_vi_khuan",
        "viem_xoang_cap",
        "viem_xoang_tai_phat",
        "viem_xoang_man_tinh",
        "viem_xoang_do_nam",
        "nguy_co_bien_chung",
        "khong_phai_viem_xoang",
    ],
)
def test_recommendations_remain_structured(
    sinusitis_kb: MedicalKnowledgeBase, disease: str
) -> None:
    """Structured advice should keep the expected section markers for the UI parser."""

    recommendation = sinusitis_kb.get_recommendation(disease)
    assert recommendation, f"No recommendation text for {disease}"
    assert recommendation.startswith(
        "@summary:"
    ), f"Missing @summary header for {disease}"
    required_markers = [
        "@summary:",
        "@home_care:",
        "@medical_visit:",
        "@follow_up:",
        "@emergency:",
    ]
    for marker in required_markers:
        assert marker in recommendation, f"Marker {marker} absent for {disease}"
