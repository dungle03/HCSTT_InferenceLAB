"""Medical Routes - User-facing medical diagnosis interface.

This blueprint provides a user-friendly medical diagnosis system where users can:
- Input symptoms through an intuitive wizard form
- Get AI-powered diagnosis based on 100 medical rules
- Receive treatment recommendations
- View visualization of inference process
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set
from uuid import uuid4

from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    url_for,
)

from inference_lab.forward import run_forward_inference

# Import Smart Diagnosis Scorer
# from web.diagnosis_scorer import SmartDiagnosisScorer - BỎ TÍNH NĂNG TÍNH ĐIỂM

# Import Medical KB
try:
    from medical_kb import MedicalKnowledgeBase, extract_facts_from_form
except ImportError:
    MedicalKnowledgeBase = None
    extract_facts_from_form = None


# Create blueprint
medical_bp = Blueprint(
    "medical",
    __name__,
    url_prefix="/sinusitis",  # THAY ĐỔI URL PREFIX
    template_folder="../templates/sinusitis",  # THAY ĐỔI TEMPLATE FOLDER
    static_folder="../static/sinusitis",  # THAY ĐỔI STATIC FOLDER
    static_url_path="/static",
)


# Global KB instance (loaded once)
_sinusitis_kb = None


def get_sinusitis_kb() -> Any:
    """Get or create Sinusitis KB instance."""
    global _sinusitis_kb
    if _sinusitis_kb is None:
        if MedicalKnowledgeBase is None:
            raise RuntimeError(
                "Medical KB not available. Please ensure medical_kb module is installed."
            )
        # TẢI KB MỚI (chấp nhận kb_path hoặc json_path)
        _sinusitis_kb = MedicalKnowledgeBase(kb_path="data/sinusitis_kb.json")
    return _sinusitis_kb


# ---------------------------------------------------------------------------
# Conversational Interview Flow (Doctor-style Q&A)
# ---------------------------------------------------------------------------

# Ordered question bank (prioritize red flags and major symptoms)
INTERVIEW_QUESTIONS: List[Dict[str, Any]] = [
    # 1) Red flags trước - hỏi rất rõ ràng, giống bác sĩ sàng lọc nguy hiểm
    {
        "id": "sung_quanh_mat",
        "variable": "sung_quanh_mat",
        "type": "boolean",
        "label": "Mình hỏi trước một dấu hiệu quan trọng nhé: Gần đây bạn có sưng, đỏ hoặc đau quanh mắt không?",
    },
    {
        "id": "nhin_mo",
        "variable": "nhin_mo",
        "type": "boolean",
        "label": "Mắt bạn có bị nhìn mờ, nhìn đôi hoặc thay đổi thị lực bất thường không?",
    },
    {
        "id": "dau_dau_du_doi",
        "variable": "dau_dau_du_doi",
        "type": "boolean",
        "label": "Bạn có gặp cơn đau đầu rất dữ dội, không đáp ứng với thuốc giảm đau thông thường không?",
    },
    {
        "id": "cung_gay",
        "variable": "cung_gay",
        "type": "boolean",
        "label": "Bạn có cảm giác cứng gáy, khó cúi gập cổ không?",
    },
    # 2) Thời gian triệu chứng - nền tảng để phân biệt virus/vi khuẩn/mạn tính
    {
        "id": "thoi_gian_trieu_chung",
        "variable": "thoi_gian_trieu_chung",
        "type": "number",
        "label": "Triệu chứng khó chịu (nghẹt mũi, đau mặt, chảy mũi...) đã kéo dài khoảng bao nhiêu ngày?",
        "min": 0,
        "max": 365,
        "step": 1,
    },
    # 3) Triệu chứng chính của viêm xoang
    {
        "id": "nghet_mui",
        "variable": "nghet_mui",
        "type": "boolean",
        "label": "Hiện tại bạn có bị nghẹt mũi hoặc khó thở bằng mũi rõ rệt không?",
    },
    {
        "id": "dau_vung_xoang_ham",
        "variable": "dau_vung_xoang_ham",
        "type": "boolean",
        "label": "Bạn có đau hoặc căng tức vùng má (xoang hàm) không?",
    },
    {
        "id": "dau_vung_xoang_tran",
        "variable": "dau_vung_xoang_tran",
        "type": "boolean",
        "label": "Bạn có đau hoặc căng tức vùng trán (xoang trán) không?",
    },
    {
        "id": "loai_dich_mui",
        "variable": "loai_dich_mui",
        "type": "radio",
        "label": "Dịch mũi của bạn hiện tại như thế nào?",
        "options": ["Không có", "Trong, loãng", "Đặc, vàng/xanh"],
    },
    {
        "id": "giam_khuu_giac",
        "variable": "giam_khuu_giac",
        "type": "boolean",
        "label": "Bạn có cảm giác ngửi kém hoặc mất mùi so với bình thường không?",
    },
    # 4) Diễn tiến bệnh - giúp tách virus/vi khuẩn
    {
        "id": "trieu_chung_nang_len_sau_5_ngay",
        "variable": "trieu_chung_nang_len_sau_5_ngay",
        "type": "boolean",
        "label": "Sau vài ngày đầu có vẻ đỡ, triệu chứng của bạn có nặng lên lại sau khoảng 5–7 ngày không?",
    },
    # 5) Nhiệt độ và triệu chứng hỗ trợ
    {
        "id": "nhiet_do",
        "variable": "nhiet_do",
        "type": "number",
        "label": "Nhiệt độ cơ thể gần nhất bạn đo được là bao nhiêu °C?",
        "min": 35,
        "max": 43,
        "step": 0.1,
    },
    {
        "id": "ho",
        "variable": "ho",
        "type": "boolean",
        "label": "Bạn có ho (đặc biệt ho nhiều về đêm) không?",
    },
    {
        "id": "hoi_mieng",
        "variable": "hoi_mieng",
        "type": "boolean",
        "label": "Bạn hoặc người xung quanh có cảm nhận hơi thở của bạn có mùi hôi khó chịu không?",
    },
    # 6) Yếu tố nguy cơ và nền bệnh - chỉ hỏi những yếu tố có ý nghĩa trong luật
    {
        "id": "co_di_ung",
        "variable": "co_di_ung",
        "type": "boolean",
        "label": "Bạn có tiền sử viêm mũi dị ứng hoặc dễ dị ứng với bụi/phấn hoa/khói... không?",
    },
    {
        "id": "co_hen_suyen",
        "variable": "co_hen_suyen",
        "type": "boolean",
        "label": "Bạn có được chẩn đoán hen suyễn trước đây không?",
    },
    {
        "id": "co_polyp_mui",
        "variable": "co_polyp_mui",
        "type": "boolean",
        "label": "Bạn đã từng được bác sĩ báo là có polyp mũi hoặc đã phẫu thuật polyp mũi chưa?",
    },
    {
        "id": "suy_giam_mien_dich",
        "variable": "suy_giam_mien_dich",
        "type": "boolean",
        "label": "Hiện tại bạn có đang trong tình trạng suy giảm miễn dịch (tiểu đường khó kiểm soát, HIV, dùng corticoid kéo dài, hóa trị, v.v.) không?",
    },
    {
        "id": "tai_phat_nhieu_lan",
        "variable": "tai_phat_nhieu_lan",
        "type": "boolean",
        "label": "Trong 12 tháng qua bạn có ít nhất 4 đợt viêm xoang cấp cần điều trị y tế không?",
    },
]


def _choose_next_question(current_answers: Dict[str, Any]) -> Dict[str, Any] | None:
    """Pick the next unanswered question from the ordered bank."""
    answered_keys = set(current_answers.keys())
    for q in INTERVIEW_QUESTIONS:
        if q["variable"] not in answered_keys:
            return q
    return None


def _get_question_for_fact(fact: str) -> Dict[str, Any] | None:
    """Map an inferred/required fact to a concrete question definition."""
    # Direct one-to-one mapping when variable == fact
    for q in INTERVIEW_QUESTIONS:
        if q["variable"] == fact:
            return q

    # Derived fact → source question mapping
    derived_map = {
        # Time-derived facts
        "trieu_chung_duoi_10_ngay": "thoi_gian_trieu_chung",
        "trieu_chung_tren_10_ngay": "thoi_gian_trieu_chung",
        "trieu_chung_keo_dai_12_tuan": "thoi_gian_trieu_chung",
        # Nasal discharge to radio
        "chay_mui_trong": "loai_dich_mui",
        "chay_mui_dac": "loai_dich_mui",
        # Face pain aggregates → ask a concrete site first
        "dau_nang_mat": "dau_vung_xoang_ham",
        "co_bang_chung_thoi_gian_cap": "thoi_gian_trieu_chung",
        "co_bang_chung_dich_cap": "loai_dich_mui",
        "dieu_kien_cap_day_du": "loai_dich_mui",
    }
    var = derived_map.get(fact)
    if var:
        for q in INTERVIEW_QUESTIONS:
            if q["variable"] == var:
                return q
    return None


def _choose_next_question_dynamic(
    kb: Any, answers: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Chọn câu hỏi tiếp theo theo kiểu 'ít nhưng trúng'.

    Chiến lược:
    - Luôn ưu tiên phát hiện sớm red flags và các chẩn đoán nguy hiểm.
    - Chỉ hỏi những fact còn thiếu của các luật đang 'gần được kích hoạt' (partially satisfied).
    - Bỏ qua các câu hỏi không còn ảnh hưởng đến chẩn đoán ưu tiên.
    - Nếu KB không gợi ý được gì thêm, fallback sang danh sách tĩnh tối giản.
    """
    # Bước 1: nếu chưa có câu nào -> hỏi thời gian (trục phân loại chính)
    if not answers:
        for q in INTERVIEW_QUESTIONS:
            if q.get("variable") == "thoi_gian_trieu_chung":
                return q

    if extract_facts_from_form is None:
        return _choose_next_question(current_answers=answers)

    # Bước 2: tính các facts đã biết từ câu trả lời hiện tại
    try:
        known_facts = set(extract_facts_from_form(answers, kb))
    except Exception:
        known_facts = set()

    # Mục tiêu chẩn đoán cần quan tâm
    target_conclusions = {
        "nguy_co_bien_chung",
        "viem_xoang_do_nam",
        "viem_xoang_cap_do_vi_khuan",
        "viem_xoang_tai_phat",
        "viem_xoang_man_tinh",
        "viem_xoang_cap_do_virus",
        "viem_xoang_cap",
    }

    # Bước 3: duyệt rules để tìm những premises còn thiếu nhưng quan trọng
    missing_facts: Dict[str, int] = {}
    for rule in kb.data.get("rules", []):
        conclusion = rule.get("conclusion")
        if conclusion not in target_conclusions:
            # Không dùng các rule ngoài mục tiêu chính để quyết định câu hỏi
            continue

        premises = set(rule.get("premises", []))
        if not premises:
            continue

        missing = premises - known_facts

        # Chỉ quan tâm:
        # - ĐÃ có ít nhất 1 tiền đề đúng (rule đang "gần bắn")
        # - CÒN thiếu nhưng không phải thiếu toàn bộ
        if 0 < len(missing) < len(premises):
            for fact in missing:
                missing_facts[fact] = missing_facts.get(fact, 0) + 1

    # Bước 4: nếu có các fact thiếu quan trọng -> chọn fact xuất hiện nhiều nhất
    if missing_facts:
        # Lấy fact có tần suất cao nhất (ảnh hưởng nhiều rule nhất)
        fact = max(missing_facts.items(), key=lambda kv: kv[1])[0]
        q = _get_question_for_fact(fact)
        if q:
            # Chỉ hỏi nếu user chưa trả lời biến này
            if q["variable"] not in answers or answers.get(q["variable"]) in (None, ""):
                # Đảm bảo có options cho radio nếu cần
                if q.get("type") == "radio" and "options" not in q:
                    q = {**q, "options": ["Không có", "Trong, loãng", "Đặc, vàng/xanh"]}
                return q

    # Bước 5: nếu không còn fact quan trọng cần hỏi:
    # dùng fallback tối giản (theo thứ tự đã được rút gọn trong INTERVIEW_QUESTIONS)
    return _choose_next_question(current_answers=answers)


def _try_early_stop(kb: Any, answers: Dict[str, Any]) -> Dict[str, Any] | None:
    """Run inference with current answers; if a prioritized diagnosis is determined, return result payload.

    Returns None if more information should be asked.
    """
    if extract_facts_from_form is None:
        return None

    try:
        facts = extract_facts_from_form(answers, kb)
        goals = [d["variable"] for d in kb.get_diseases()]
        result = run_forward_inference(
            kb.kb,
            initial_facts=facts,
            goals=goals,
            strategy="stack",
            index_mode="min",
            make_graphs=False,
        )

        # Determine diagnosis only if any disease fact was actually inferred
        priority_order = [
            "nguy_co_bien_chung",
            "viem_xoang_do_nam",
            "viem_xoang_cap_do_vi_khuan",
            "viem_xoang_tai_phat",
            "viem_xoang_man_tinh",
            "viem_xoang_cap_do_virus",
            "viem_xoang_cap",
            "khong_phai_viem_xoang",
        ]
        diagnosed: str | None = None
        for disease in priority_order:
            if disease in result.final_facts:
                diagnosed = disease
                break

        # If nothing inferred yet, or only negative conclusion, keep asking
        if diagnosed is None or diagnosed == "khong_phai_viem_xoang":
            return None

        # If we only have viem_xoang_cap, try to refine etiology by asking targeted questions
        if diagnosed == "viem_xoang_cap":
            if "thoi_gian_trieu_chung" not in answers or "loai_dich_mui" not in answers:
                return None

        # Build and persist a full result to reuse existing results page
        disease_info = kb.get_disease_info(diagnosed)
        recommendation = kb.get_recommendation(diagnosed)
        severity_map = {
            "Mild": "low",
            "Moderate": "medium",
            "Severe": "high",
            "Critical": "critical",
            "Info": "info",
        }
        disease_label = (
            disease_info.get("label", "Không xác định") if disease_info else diagnosed
        )
        severity_raw = (
            disease_info.get("severity", "Unknown") if disease_info else "Unknown"
        )
        severity = severity_map.get(severity_raw, "low")

        session_id = uuid4().hex
        output_root = Path(
            current_app.config.get("GRAPH_OUTPUT_ROOT", "web/static/generated")
        )
        output_dir = output_root / session_id
        output_dir.mkdir(parents=True, exist_ok=True)

        response = {
            "ok": True,
            "session_id": session_id,
            "diagnosis": {
                "disease": diagnosed,
                "disease_label": disease_label,
                "severity": severity,
                "severity_raw": severity_raw,
                "confidence": 100 if result.success else 0,
                "success": result.success,
            },
            "symptoms": {"input": answers, "extracted_facts": list(facts)},
            "recommendation": recommendation,
            "inference": {
                "fired_rules": result.fired_rules,
                "final_facts": result.final_facts,
                "steps": len(result.history),
            },
            "graphs": {"fpg": None, "rpg": None},
        }
        _save_result(session_id, response)
        return {
            "done": True,
            "result_url": url_for("medical.results", session_id=session_id),
            "summary": {
                "label": disease_label,
                "severity": severity,
            },
        }

    except Exception:
        return None


def _generate_symptom_based_recommendation(
    input_facts: Set[str], final_facts: List[str], analysis: Dict[str, Any]
) -> str:
    """Tạo khuyến nghị dựa trên triệu chứng khi không chẩn đoán được bệnh cụ thể.

    Args:
        input_facts: Triệu chứng ban đầu
        final_facts: Facts sau inference
        analysis: Kết quả phân tích từ _analyze_symptoms_without_diagnosis

    Returns:
        Chuỗi khuyến nghị
    """
    recommendations = []

    # Khuyến nghị chung
    recommendations.append("🏥 **Khám bác sĩ để được chẩn đoán chính xác**")
    recommendations.append("   - Triệu chứng hiện tại chưa đủ để xác định bệnh cụ thể")
    recommendations.append("   - Cần thêm thông tin và xét nghiệm y tế")

    # Khuyến nghị theo category
    if "Hô hấp" in analysis["categories"]:
        recommendations.append("🫁 **Chăm sóc hệ hô hấp:**")
        recommendations.append("   - Nghỉ ngơi đầy đủ, tránh khói bụi")
        recommendations.append("   - Uống đủ nước, giữ ấm cơ thể")

    if "Tiêu hóa" in analysis["categories"]:
        recommendations.append("🍵 **Chăm sóc tiêu hóa:**")
        recommendations.append("   - Uống nhiều nước để tránh mất nước")
        recommendations.append("   - Ăn nhẹ, dễ tiêu, tránh thức ăn cay nóng")

    if "Thần kinh" in analysis["categories"]:
        recommendations.append("🧠 **Chú ý triệu chứng thần kinh:**")
        recommendations.append("   - Nghỉ ngơi trong môi trường yên tĩnh")
        recommendations.append("   - Theo dõi sát, nếu nặng hơn hãy đến bác sĩ ngay")

    if "Tim mạch" in analysis["categories"]:
        recommendations.append("❤️ **Cảnh báo triệu chứng tim mạch:**")
        recommendations.append("   - Cần được khám ngay nếu có đau ngực, khó thở")
        recommendations.append("   - Không tự ý vận động mạnh")

    # Khuyến nghị về severity
    if analysis["severity_indicators"]:
        recommendations.append("⚠️ **Lưu ý quan trọng:**")
        recommendations.append("   - Có dấu hiệu cần theo dõi sát")
        recommendations.append("   - Đến cơ sở y tế nếu triệu chứng nặng hơn")
        recommendations.append("   - Gọi 115 trong trường hợp khẩn cấp")

    # Khuyến nghị chung cuối
    recommendations.append("📝 **Ghi chú thêm:**")
    recommendations.append("   - Theo dõi nhiệt độ, diễn biến triệu chứng")
    recommendations.append("   - Chuẩn bị thông tin chi tiết khi gặp bác sĩ")
    recommendations.append("   - Không tự ý dùng thuốc kháng sinh")

    return "\n".join(recommendations)


@medical_bp.get("/")
def landing():
    """Sinusitis landing page."""
    try:
        kb = get_sinusitis_kb()
        metadata = kb.get_metadata()
    except Exception:
        metadata = {"total_rules": 45, "modules": []}

    return render_template(
        "landing.html",
        metadata=metadata,
        graphviz_available=False,
        current_year=datetime.now().year,
    )


# Wizard route removed: interview-only mode


@medical_bp.get("/interview")
def interview():
    """Doctor-style interview page."""
    try:
        kb = get_sinusitis_kb()
        # Optionally pass some metadata if needed later
        metadata = kb.get_metadata()
    except Exception:
        metadata = {"total_rules": 45}

    return render_template(
        "interview.html",
        metadata=metadata,
        current_year=datetime.now().year,
    )


@medical_bp.post("/api/next_question")
def api_next_question():
    """Return the next interview question or conclude with a result when ready."""
    payload = request.get_json(silent=True) or {}
    answers: Dict[str, Any] = payload.get("answers") or {}

    try:
        kb = get_sinusitis_kb()
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

    # Try early conclusion only when a concrete disease is inferred
    early = _try_early_stop(kb, answers)
    if early:
        return jsonify({"ok": True, "done": True, **early})

    # Otherwise, serve the next question (dynamic by KB, with fallback)
    q = _choose_next_question_dynamic(kb, answers)
    if q:
        question_payload = {
            k: v
            for k, v in q.items()
            if k in {"id", "variable", "type", "label", "options", "min", "max", "step"}
        }
        return jsonify({"ok": True, "done": False, "question": question_payload})

    # No more questions; finalize regardless of outcome
    try:
        if extract_facts_from_form is None:
            return jsonify({"ok": False, "error": "Fact extraction not available"}), 500

        facts = extract_facts_from_form(answers, kb)
        goals = [d["variable"] for d in kb.get_diseases()]
        result = run_forward_inference(
            kb.kb,
            initial_facts=facts,
            goals=goals,
            strategy="stack",
            index_mode="min",
            make_graphs=False,
        )

        priority_order = [
            "nguy_co_bien_chung",
            "viem_xoang_do_nam",
            "viem_xoang_cap_do_vi_khuan",
            "viem_xoang_tai_phat",
            "viem_xoang_man_tinh",
            "viem_xoang_cap_do_virus",
            "viem_xoang_cap",
            "khong_phai_viem_xoang",
        ]
        diagnosed = next(
            (d for d in priority_order if d in result.final_facts),
            "khong_phai_viem_xoang",
        )

        disease_info = kb.get_disease_info(diagnosed)
        recommendation = kb.get_recommendation(diagnosed)
        severity_map = {
            "Mild": "low",
            "Moderate": "medium",
            "Severe": "high",
            "Critical": "critical",
            "Info": "info",
        }
        disease_label = (
            disease_info.get("label", "Không xác định") if disease_info else diagnosed
        )
        severity_raw = (
            disease_info.get("severity", "Unknown") if disease_info else "Unknown"
        )
        severity = severity_map.get(severity_raw, "low")

        session_id = uuid4().hex
        output_root = Path(
            current_app.config.get("GRAPH_OUTPUT_ROOT", "web/static/generated")
        )
        output_dir = output_root / session_id
        output_dir.mkdir(parents=True, exist_ok=True)

        response = {
            "ok": True,
            "session_id": session_id,
            "diagnosis": {
                "disease": diagnosed,
                "disease_label": disease_label,
                "severity": severity,
                "severity_raw": severity_raw,
                "confidence": 100 if result.success else 0,
                "success": result.success,
            },
            "symptoms": {"input": answers, "extracted_facts": list(facts)},
            "recommendation": recommendation,
            "inference": {
                "fired_rules": result.fired_rules,
                "final_facts": result.final_facts,
                "steps": len(result.history),
            },
            "graphs": {"fpg": None, "rpg": None},
        }
        _save_result(session_id, response)
        return jsonify(
            {
                "ok": True,
                "done": True,
                "result_url": url_for("medical.results", session_id=session_id),
                "summary": {"label": disease_label, "severity": severity},
            }
        )
    except Exception as e:
        return jsonify({"ok": False, "error": f"Finalize error: {e}"}), 500


@medical_bp.get("/results/<session_id>")
def results(session_id: str):
    """Display diagnosis results."""
    result_data = _load_result(session_id)
    if not result_data:
        return render_template("error.html", error="Result not found or expired"), 404

    try:
        kb = get_sinusitis_kb()
    except Exception:
        kb = None

    diagnosis = result_data.get("diagnosis", {})
    symptoms = result_data.get("symptoms", {})

    # Lấy fact đầu vào và chuyển thành label để hiển thị
    input_facts_raw = symptoms.get("extracted_facts", [])
    input_symptoms_display = []
    if kb:
        for fact in input_facts_raw:
            label = kb.get_symptom_label(fact)
            if label:
                input_symptoms_display.append(label)
    else:
        input_symptoms_display = input_facts_raw

    recommendation = result_data.get("recommendation", "")
    recommendations = [
        line.strip() for line in recommendation.split("\n") if line.strip()
    ]

    fired_rules = result_data.get("inference", {}).get("fired_rules", [])
    final_facts = set(result_data.get("inference", {}).get("final_facts", []))
    patient_facts = set(input_facts_raw)

    # Lấy giải thích cho các luật đã được kích hoạt
    rule_explanations = []

    def _allowed_modules_for(disease_code: str | None) -> set:
        mapping = {
            "nguy_co_bien_chung": {"COMPLICATIONS", "ACUTE_DIAGNOSIS", "ACUTE_CONTEXT"},
            "viem_xoang_do_nam": {"FUNGAL_DIAGNOSIS", "CHRONIC_DIAGNOSIS"},
            "viem_xoang_cap_do_vi_khuan": {
                "ACUTE_DIAGNOSIS",
                "ACUTE_ETIOLOGY",
                "ACUTE_CONTEXT",
            },
            "viem_xoang_man_tinh": {"CHRONIC_DIAGNOSIS"},
            "viem_xoang_cap_do_virus": {
                "ACUTE_DIAGNOSIS",
                "ACUTE_ETIOLOGY",
                "ACUTE_CONTEXT",
            },
            "viem_xoang_cap": {"ACUTE_DIAGNOSIS", "ACUTE_CONTEXT"},
            "viem_xoang_tai_phat": {
                "ACUTE_DIAGNOSIS",
                "ACUTE_CONTEXT",
                "RECURRENT_ACUTE",
            },
            "khong_phai_viem_xoang": {"DIFFERENTIAL"},
        }
        return mapping.get(disease_code or "", set())

    if kb:
        allowed_modules = _allowed_modules_for(diagnosis.get("disease"))
        module_labels = {
            "ACUTE_DIAGNOSIS": "Chẩn đoán viêm xoang cấp",
            "ACUTE_ETIOLOGY": "Phân loại nguyên nhân cấp",
            "CHRONIC_DIAGNOSIS": "Chẩn đoán viêm xoang mạn",
            "FUNGAL_DIAGNOSIS": "Tầm soát nấm",
            "COMPLICATIONS": "Cảnh báo biến chứng",
            "DIFFERENTIAL": "Chẩn đoán phân biệt",
            "ACUTE_CONTEXT": "Điều kiện bổ trợ viêm xoang cấp",
            "RECURRENT_ACUTE": "Đánh giá viêm xoang tái phát",
        }
        disease_goal_set = {item.get("variable") for item in kb.get_diseases()}
        for rule_id in fired_rules:
            rule_info = kb.get_rule_info(rule_id)
            if not rule_info:
                continue
            if allowed_modules and rule_info.get("module") not in allowed_modules:
                continue
            premises = []
            for atom in rule_info.get("premises", []):
                premises.append(
                    {
                        "code": atom,
                        "label": kb.get_symptom_label(atom),
                        "satisfied": atom in final_facts,
                        "source": "patient" if atom in patient_facts else "inferred",
                    }
                )

            conclusion_code = rule_info.get("conclusion")
            conclusion_label = kb.get_symptom_label(conclusion_code)
            disease_info = kb.get_disease_info(conclusion_code)
            if disease_info and disease_info.get("label"):
                conclusion_label = disease_info["label"]

            rule_explanations.append(
                {
                    "rule_id": rule_info.get("json_id") or f"Rule {rule_id}",
                    "engine_id": rule_id,
                    "module": rule_info.get("module"),
                    "module_label": module_labels.get(
                        rule_info.get("module"), rule_info.get("module")
                    ),
                    "notes": rule_info.get("notes"),
                    "premises": premises,
                    "conclusion": {
                        "code": conclusion_code,
                        "label": conclusion_label,
                        "is_goal": conclusion_code in disease_goal_set,
                    },
                    "confidence": rule_info.get("confidence"),
                }
            )

    return render_template(
        "results.html",
        diagnosis=diagnosis,
        input_symptoms=input_symptoms_display,
        recommendations=recommendations,
        inference_steps=result_data.get("inference", {}).get("steps"),
        fired_rules_count=len(result_data.get("inference", {}).get("fired_rules", [])),
        fpg_image=None,
        rpg_image=None,
        session_id=session_id,
        rule_explanations=rule_explanations,
        current_year=datetime.now().year,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _simple_extract_facts(form_data: Dict[str, Any]) -> Set[str]:
    """Simple fact extraction fallback."""
    facts = set()

    def is_true(value):
        """Helper to check if a value should be treated as True."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() not in ("false", "no", "0", "", "none")
        return bool(value)

    # Temperature
    nhiet_do = form_data.get("nhiet_do")
    if nhiet_do:
        try:
            nhiet_do = float(nhiet_do)
            if nhiet_do > 38:
                facts.add("sot")
            if nhiet_do > 38.5:
                facts.add("sot_cao")
        except (ValueError, TypeError):
            pass

    # Boolean symptoms
    if is_true(form_data.get("ho")):
        facts.add("ho")
        loai_ho = form_data.get("loai_ho")
        if loai_ho == "khan":
            facts.add("ho_khan")
        elif loai_ho == "co_dam":
            facts.add("ho_co_dam")

    if is_true(form_data.get("dau_dau")):
        facts.add("dau_dau")
    if is_true(form_data.get("met_moi")):
        facts.add("met_moi")
    if is_true(form_data.get("dau_hong")):
        facts.add("dau_hong")
    if is_true(form_data.get("chay_mui")):
        facts.add("chay_mui")
    if is_true(form_data.get("mat_vi_giac")):
        facts.add("mat_vi_giac")
    if is_true(form_data.get("mat_khu_giac")):
        facts.add("mat_khu_giac")
    if is_true(form_data.get("dau_nguc")):
        facts.add("dau_nguc")
    if is_true(form_data.get("kho_tho")):
        facts.add("kho_tho")
    if is_true(form_data.get("dau_bung")):
        facts.add("dau_bung")
    if is_true(form_data.get("buon_non")):
        facts.add("buon_non")
    if is_true(form_data.get("tieu_chay")):
        facts.add("tieu_chay")

    # SpO2
    spo2 = form_data.get("spo2")
    if spo2:
        try:
            spo2 = float(spo2)
            if spo2 < 95:
                facts.add("spo2_thap")
            else:
                facts.add("spo2_binh_thuong")
        except (ValueError, TypeError):
            pass

    # Age groups
    tuoi = form_data.get("tuoi")
    if tuoi:
        try:
            tuoi = int(tuoi)
            if tuoi < 15:
                facts.add("tre_em")
            elif tuoi >= 60:
                facts.add("nguoi_gia")
        except (ValueError, TypeError):
            pass

    return facts


def _get_possible_diseases(kb: Any) -> List[str]:
    """Get list of possible diseases as inference goals."""
    diseases = [
        "cam_thuong",
        "nghi_covid",
        "covid_19",
        "covid_nhe",
        "covid_nang",
        "viem_phoi",
        "hen_suyen",
        "viem_hong",
        "viem_da_day",
        "ngo_doc_thuc_pham",
    ]
    return diseases


def _save_result(session_id: str, result_data: Dict[str, Any]) -> None:
    """Save result to file for later retrieval."""
    output_root = Path(
        current_app.config.get("GRAPH_OUTPUT_ROOT", "web/static/generated")
    )
    result_file = output_root / session_id / "result.json"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)


def _load_result(session_id: str) -> Dict[str, Any] | None:
    """Load saved result from file."""
    output_root = Path(
        current_app.config.get("GRAPH_OUTPUT_ROOT", "web/static/generated")
    )
    result_file = output_root / session_id / "result.json"

    if not result_file.exists():
        return None

    with open(result_file, "r", encoding="utf-8") as f:
        return json.load(f)
