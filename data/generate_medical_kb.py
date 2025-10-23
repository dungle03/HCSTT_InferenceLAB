"""Generate Medical Knowledge Base JSON file.

This script generates a comprehensive medical KB with 100 rules covering:
- Symptoms (15 rules)
- Respiratory diseases (25 rules)
- Digestive diseases (20 rules)
- Cardiovascular diseases (15 rules)
- Endocrine diseases (10 rules)
- Emergency conditions (10 rules)
- Treatment recommendations (5 rules)
"""

import json
from datetime import datetime
from pathlib import Path


def generate_medical_kb():
    """Generate complete medical knowledge base."""

    kb = {
        "version": "1.0.0",
        "last_updated": datetime.now().isoformat(),
        "description": "Medical Knowledge Base with 100 rules for common diagnoses",
        "metadata": {
            "total_rules": 100,
            "total_symptoms": 30,
            "total_diseases": 20,
            "modules": [
                {"code": "SYMP", "name": "Triệu chứng cơ bản", "rules": 15},
                {"code": "RESP", "name": "Hô hấp", "rules": 25},
                {"code": "DIGE", "name": "Tiêu hóa", "rules": 20},
                {"code": "CARD", "name": "Tim mạch", "rules": 15},
                {"code": "ENDO", "name": "Nội tiết", "rules": 10},
                {"code": "EMER", "name": "Cấp cứu", "rules": 10},
                {"code": "RECO", "name": "Khuyến nghị", "rules": 5},
            ],
        },
        # Triệu chứng
        "symptoms": [
            {
                "id": "S001",
                "variable": "nhiet_do_cao",
                "label": "Nhiệt độ cao",
                "category": "vital",
            },
            {"id": "S002", "variable": "sot", "label": "Sốt", "category": "vital"},
            {
                "id": "S003",
                "variable": "sot_cao",
                "label": "Sốt cao >38.5°C",
                "category": "vital",
            },
            {"id": "S004", "variable": "ho", "label": "Ho", "category": "resp"},
            {
                "id": "S005",
                "variable": "ho_khan",
                "label": "Ho khan",
                "category": "resp",
            },
            {
                "id": "S006",
                "variable": "ho_co_dam",
                "label": "Ho có đờm",
                "category": "resp",
            },
            {
                "id": "S007",
                "variable": "dam_mau",
                "label": "Đờm có máu",
                "category": "resp",
            },
            {
                "id": "S008",
                "variable": "kho_tho",
                "label": "Khó thở",
                "category": "resp",
            },
            {
                "id": "S009",
                "variable": "chay_mui",
                "label": "Chảy nước mũi",
                "category": "resp",
            },
            {
                "id": "S010",
                "variable": "dau_hong",
                "label": "Đau họng",
                "category": "resp",
            },
            {
                "id": "S011",
                "variable": "dau_dau",
                "label": "Đau đầu",
                "category": "neuro",
            },
            {
                "id": "S012",
                "variable": "met_moi",
                "label": "Mệt mỏi",
                "category": "general",
            },
            {
                "id": "S013",
                "variable": "mat_vi_giac",
                "label": "Mất vị giác",
                "category": "neuro",
            },
            {
                "id": "S014",
                "variable": "mat_khu_giac",
                "label": "Mất khứu giác",
                "category": "neuro",
            },
            {
                "id": "S015",
                "variable": "dau_nguc",
                "label": "Đau ngực",
                "category": "card",
            },
            {
                "id": "S016",
                "variable": "dau_bung",
                "label": "Đau bụng",
                "category": "dige",
            },
            {
                "id": "S017",
                "variable": "buon_non",
                "label": "Buồn nôn",
                "category": "dige",
            },
            {
                "id": "S018",
                "variable": "tieu_chay",
                "label": "Tiêu chảy",
                "category": "dige",
            },
            {
                "id": "S019",
                "variable": "spo2_thap",
                "label": "SpO2 < 95%",
                "category": "vital",
            },
            {
                "id": "S020",
                "variable": "spo2_binh_thuong",
                "label": "SpO2 >= 95%",
                "category": "vital",
            },
        ],
        # Bệnh
        "diseases": [
            {
                "id": "D001",
                "variable": "cam_thuong",
                "label": "Cảm cúm thông thường",
                "severity": "Mild",
                "icd10": "J00",
            },
            {
                "id": "D002",
                "variable": "nghi_covid",
                "label": "Nghi ngờ COVID-19",
                "severity": "Moderate",
                "icd10": "U07.1",
            },
            {
                "id": "D003",
                "variable": "covid_19",
                "label": "COVID-19",
                "severity": "Moderate",
                "icd10": "U07.1",
            },
            {
                "id": "D004",
                "variable": "covid_nhe",
                "label": "COVID-19 nhẹ",
                "severity": "Mild",
                "icd10": "U07.1",
            },
            {
                "id": "D005",
                "variable": "covid_nang",
                "label": "COVID-19 nặng",
                "severity": "Severe",
                "icd10": "U07.1",
            },
            {
                "id": "D006",
                "variable": "viem_phoi",
                "label": "Viêm phổi",
                "severity": "Severe",
                "icd10": "J18",
            },
            {
                "id": "D007",
                "variable": "hen_suyen",
                "label": "Hen suyễn",
                "severity": "Moderate",
                "icd10": "J45",
            },
            {
                "id": "D008",
                "variable": "viem_hong",
                "label": "Viêm họng",
                "severity": "Mild",
                "icd10": "J02",
            },
            {
                "id": "D009",
                "variable": "viem_da_day",
                "label": "Viêm dạ dày",
                "severity": "Moderate",
                "icd10": "K29",
            },
            {
                "id": "D010",
                "variable": "ngo_doc_thuc_pham",
                "label": "Ngộ độc thực phẩm",
                "severity": "Moderate",
                "icd10": "A05",
            },
        ],
        # 100 LUẬT
        "rules": [],
    }

    # ==================== SYMPTOMS (15 rules) ====================
    kb["rules"].extend(
        [
            {
                "id": "R001",
                "module": "SYMP",
                "premises": ["nhiet_do_cao"],
                "conclusion": "sot",
                "confidence": 1.0,
                "notes": "Định nghĩa sốt",
            },
            {
                "id": "R002",
                "module": "SYMP",
                "premises": ["sot", "nhiet_do_cao"],
                "conclusion": "sot_cao",
                "confidence": 1.0,
                "notes": "Sốt cao",
            },
            {
                "id": "R003",
                "module": "SYMP",
                "premises": ["ho", "dam_mau"],
                "conclusion": "ho_co_dam",
                "confidence": 0.9,
                "notes": "Ho có đờm máu",
            },
            {
                "id": "R004",
                "module": "SYMP",
                "premises": ["kho_tho", "spo2_thap"],
                "conclusion": "kho_tho_nang",
                "confidence": 0.95,
                "notes": "Khó thở nặng",
            },
            {
                "id": "R005",
                "module": "SYMP",
                "premises": ["dau_dau", "sot"],
                "conclusion": "dau_dau_do_sot",
                "confidence": 0.8,
                "notes": "Đau đầu do sốt",
            },
            {
                "id": "R006",
                "module": "SYMP",
                "premises": ["dau_bung", "buon_non"],
                "conclusion": "trieu_chung_tieu_hoa",
                "confidence": 0.85,
                "notes": "Triệu chứng tiêu hóa",
            },
            {
                "id": "R007",
                "module": "SYMP",
                "premises": ["dau_bung", "tieu_chay"],
                "conclusion": "trieu_chung_tieu_hoa",
                "confidence": 0.9,
                "notes": "Triệu chứng tiêu hóa",
            },
            {
                "id": "R008",
                "module": "SYMP",
                "premises": ["dau_nguc", "kho_tho"],
                "conclusion": "trieu_chung_tim_mach",
                "confidence": 0.85,
                "notes": "Triệu chứng tim mạch",
            },
            {
                "id": "R009",
                "module": "SYMP",
                "premises": ["ho", "kho_tho"],
                "conclusion": "trieu_chung_ho_hap",
                "confidence": 0.9,
                "notes": "Triệu chứng hô hấp",
            },
            {
                "id": "R010",
                "module": "SYMP",
                "premises": ["sot", "ho"],
                "conclusion": "trieu_chung_ho_hap",
                "confidence": 0.85,
                "notes": "Triệu chứng hô hấp",
            },
            {
                "id": "R011",
                "module": "SYMP",
                "premises": ["mat_vi_giac"],
                "conclusion": "trieu_chung_than_kinh",
                "confidence": 0.8,
                "notes": "Triệu chứng thần kinh",
            },
            {
                "id": "R012",
                "module": "SYMP",
                "premises": ["mat_khu_giac"],
                "conclusion": "trieu_chung_than_kinh",
                "confidence": 0.8,
                "notes": "Triệu chứng thần kinh",
            },
            {
                "id": "R013",
                "module": "SYMP",
                "premises": ["sot", "met_moi"],
                "conclusion": "trieu_chung_chung",
                "confidence": 0.7,
                "notes": "Triệu chứng chung",
            },
            {
                "id": "R014",
                "module": "SYMP",
                "premises": ["dau_dau", "met_moi"],
                "conclusion": "trieu_chung_chung",
                "confidence": 0.7,
                "notes": "Triệu chứng chung",
            },
            {
                "id": "R015",
                "module": "SYMP",
                "premises": ["sot_cao", "kho_tho"],
                "conclusion": "trieu_chung_nang",
                "confidence": 0.9,
                "notes": "Triệu chứng nặng",
            },
        ]
    )

    # ==================== RESPIRATORY (25 rules) ====================
    kb["rules"].extend(
        [
            # Cảm cúm (5 rules)
            {
                "id": "R016",
                "module": "RESP",
                "premises": ["sot", "ho", "chay_mui"],
                "conclusion": "cam_thuong",
                "confidence": 0.85,
                "notes": "Cảm cúm thông thường",
            },
            {
                "id": "R017",
                "module": "RESP",
                "premises": ["sot", "ho_khan", "dau_dau"],
                "conclusion": "cam_thuong",
                "confidence": 0.8,
                "notes": "Cảm cúm",
            },
            {
                "id": "R018",
                "module": "RESP",
                "premises": ["cam_thuong", "kho_tho"],
                "conclusion": "can_kham_bac_si",
                "confidence": 0.9,
                "notes": "Cảm + khó thở",
            },
            {
                "id": "R019",
                "module": "RESP",
                "premises": ["cam_thuong", "sot_cao"],
                "conclusion": "can_kham_bac_si",
                "confidence": 0.85,
                "notes": "Cảm + sốt cao",
            },
            {
                "id": "R020",
                "module": "RESP",
                "premises": ["cam_thuong", "spo2_binh_thuong"],
                "conclusion": "tu_dieu_tri",
                "confidence": 0.9,
                "notes": "Có thể tự điều trị",
            },
            # COVID-19 (8 rules)
            {
                "id": "R021",
                "module": "RESP",
                "premises": ["sot", "ho_khan", "met_moi"],
                "conclusion": "nghi_covid",
                "confidence": 0.8,
                "notes": "Nghi COVID",
            },
            {
                "id": "R022",
                "module": "RESP",
                "premises": ["nghi_covid", "mat_vi_giac"],
                "conclusion": "nghi_covid_manh",
                "confidence": 0.9,
                "notes": "Nghi COVID mạnh",
            },
            {
                "id": "R023",
                "module": "RESP",
                "premises": ["nghi_covid", "mat_khu_giac"],
                "conclusion": "nghi_covid_manh",
                "confidence": 0.9,
                "notes": "Nghi COVID mạnh",
            },
            {
                "id": "R024",
                "module": "RESP",
                "premises": ["nghi_covid_manh", "test_duong"],
                "conclusion": "covid_19",
                "confidence": 0.95,
                "notes": "Xác nhận COVID",
            },
            {
                "id": "R025",
                "module": "RESP",
                "premises": ["covid_19", "spo2_binh_thuong", "kho_tho"],
                "conclusion": "covid_nhe",
                "confidence": 0.85,
                "notes": "COVID nhẹ",
            },
            {
                "id": "R026",
                "module": "RESP",
                "premises": ["covid_nhe"],
                "conclusion": "cach_ly_tai_nha",
                "confidence": 0.9,
                "notes": "Cách ly tại nhà",
            },
            {
                "id": "R027",
                "module": "RESP",
                "premises": ["covid_19", "spo2_thap"],
                "conclusion": "covid_nang",
                "confidence": 0.95,
                "notes": "COVID nặng",
            },
            {
                "id": "R028",
                "module": "RESP",
                "premises": ["covid_nang"],
                "conclusion": "nhap_vien_gap",
                "confidence": 1.0,
                "notes": "Cần nhập viện",
            },
            # Viêm phổi (7 rules)
            {
                "id": "R029",
                "module": "RESP",
                "premises": ["sot_cao", "ho_co_dam", "kho_tho"],
                "conclusion": "viem_phoi",
                "confidence": 0.8,
                "notes": "Viêm phổi",
            },
            {
                "id": "R030",
                "module": "RESP",
                "premises": ["viem_phoi", "dam_mau"],
                "conclusion": "viem_phoi_nang",
                "confidence": 0.9,
                "notes": "Viêm phổi nặng",
            },
            {
                "id": "R031",
                "module": "RESP",
                "premises": ["viem_phoi"],
                "conclusion": "can_xquang",
                "confidence": 0.95,
                "notes": "Cần X-quang",
            },
            {
                "id": "R032",
                "module": "RESP",
                "premises": ["viem_phoi"],
                "conclusion": "can_khang_sinh",
                "confidence": 0.9,
                "notes": "Cần kháng sinh",
            },
            {
                "id": "R033",
                "module": "RESP",
                "premises": ["viem_phoi", "tre_em"],
                "conclusion": "nhap_vien",
                "confidence": 0.95,
                "notes": "Trẻ em cần nhập viện",
            },
            {
                "id": "R034",
                "module": "RESP",
                "premises": ["viem_phoi", "nguoi_gia"],
                "conclusion": "nhap_vien",
                "confidence": 0.95,
                "notes": "Người già cần nhập viện",
            },
            {
                "id": "R035",
                "module": "RESP",
                "premises": ["viem_phoi_nang"],
                "conclusion": "nhap_vien_gap",
                "confidence": 1.0,
                "notes": "Cần cấp cứu",
            },
            # Hen suyễn (3 rules)
            {
                "id": "R036",
                "module": "RESP",
                "premises": ["kho_tho", "tho_khoe_khe"],
                "conclusion": "hen_suyen",
                "confidence": 0.85,
                "notes": "Hen suyễn",
            },
            {
                "id": "R037",
                "module": "RESP",
                "premises": ["hen_suyen", "co_kich_thich"],
                "conclusion": "con_hen",
                "confidence": 0.9,
                "notes": "Cơn hen",
            },
            {
                "id": "R038",
                "module": "RESP",
                "premises": ["con_hen"],
                "conclusion": "dung_thuoc_xit",
                "confidence": 0.95,
                "notes": "Dùng thuốc xịt",
            },
            # Viêm họng (2 rules)
            {
                "id": "R039",
                "module": "RESP",
                "premises": ["dau_hong", "kho_nuot"],
                "conclusion": "viem_hong",
                "confidence": 0.85,
                "notes": "Viêm họng",
            },
            {
                "id": "R040",
                "module": "RESP",
                "premises": ["viem_hong", "sot"],
                "conclusion": "viem_amidan",
                "confidence": 0.8,
                "notes": "Viêm amidan",
            },
        ]
    )

    # ==================== DIGESTIVE (20 rules) ====================
    kb["rules"].extend(
        [
            # Viêm dạ dày (8 rules)
            {
                "id": "R041",
                "module": "DIGE",
                "premises": ["dau_bung", "buon_non"],
                "conclusion": "viem_da_day",
                "confidence": 0.75,
                "notes": "Viêm dạ dày",
            },
            {
                "id": "R042",
                "module": "DIGE",
                "premises": ["viem_da_day", "an_cay"],
                "conclusion": "viem_da_day_cap",
                "confidence": 0.85,
                "notes": "Viêm cấp",
            },
            {
                "id": "R043",
                "module": "DIGE",
                "premises": ["viem_da_day", "dau_lau_ngay"],
                "conclusion": "viem_da_day_man",
                "confidence": 0.8,
                "notes": "Viêm mạn",
            },
            {
                "id": "R044",
                "module": "DIGE",
                "premises": ["viem_da_day_cap"],
                "conclusion": "uong_thuoc_da_day",
                "confidence": 0.9,
                "notes": "Uống thuốc",
            },
            {
                "id": "R045",
                "module": "DIGE",
                "premises": ["viem_da_day_man"],
                "conclusion": "can_noi_soi",
                "confidence": 0.85,
                "notes": "Cần nội soi",
            },
            {
                "id": "R046",
                "module": "DIGE",
                "premises": ["dau_bung", "non_ra_mau"],
                "conclusion": "loet_da_day",
                "confidence": 0.9,
                "notes": "Loét dạ dày",
            },
            {
                "id": "R047",
                "module": "DIGE",
                "premises": ["loet_da_day"],
                "conclusion": "nhap_vien",
                "confidence": 0.95,
                "notes": "Cần nhập viện",
            },
            {
                "id": "R048",
                "module": "DIGE",
                "premises": ["viem_da_day", "stress"],
                "conclusion": "can_giam_stress",
                "confidence": 0.8,
                "notes": "Giảm stress",
            },
            # Tiêu chảy (6 rules)
            {
                "id": "R049",
                "module": "DIGE",
                "premises": ["tieu_chay", "buon_non"],
                "conclusion": "ngo_doc_thuc_pham",
                "confidence": 0.8,
                "notes": "Ngộ độc",
            },
            {
                "id": "R050",
                "module": "DIGE",
                "premises": ["ngo_doc_thuc_pham", "sot"],
                "conclusion": "ngo_doc_nang",
                "confidence": 0.85,
                "notes": "Ngộ độc nặng",
            },
            {
                "id": "R051",
                "module": "DIGE",
                "premises": ["tieu_chay", "dau_bung"],
                "conclusion": "viem_ruot",
                "confidence": 0.75,
                "notes": "Viêm ruột",
            },
            {
                "id": "R052",
                "module": "DIGE",
                "premises": ["tieu_chay", "phan_co_mau"],
                "conclusion": "viem_ruot_nang",
                "confidence": 0.9,
                "notes": "Viêm ruột nặng",
            },
            {
                "id": "R053",
                "module": "DIGE",
                "premises": ["viem_ruot_nang"],
                "conclusion": "nhap_vien",
                "confidence": 0.95,
                "notes": "Cần nhập viện",
            },
            {
                "id": "R054",
                "module": "DIGE",
                "premises": ["tieu_chay"],
                "conclusion": "uong_nhieu_nuoc",
                "confidence": 0.95,
                "notes": "Uống nhiều nước",
            },
            # Viêm gan (4 rules)
            {
                "id": "R055",
                "module": "DIGE",
                "premises": ["met_moi", "da_vang"],
                "conclusion": "viem_gan",
                "confidence": 0.85,
                "notes": "Viêm gan",
            },
            {
                "id": "R056",
                "module": "DIGE",
                "premises": ["viem_gan", "nieu_sẫm"],
                "conclusion": "viem_gan_cap",
                "confidence": 0.9,
                "notes": "Viêm gan cấp",
            },
            {
                "id": "R057",
                "module": "DIGE",
                "premises": ["viem_gan_cap"],
                "conclusion": "nhap_vien",
                "confidence": 0.95,
                "notes": "Cần nhập viện",
            },
            {
                "id": "R058",
                "module": "DIGE",
                "premises": ["viem_gan"],
                "conclusion": "xet_nghiem_men_gan",
                "confidence": 0.95,
                "notes": "Xét nghiệm",
            },
            # Khác (2 rules)
            {
                "id": "R059",
                "module": "DIGE",
                "premises": ["dau_bung", "tao_bon"],
                "conclusion": "tac_ruot",
                "confidence": 0.7,
                "notes": "Tắc ruột",
            },
            {
                "id": "R060",
                "module": "DIGE",
                "premises": ["tac_ruot"],
                "conclusion": "can_kham_gap",
                "confidence": 0.9,
                "notes": "Cần khám gấp",
            },
        ]
    )

    # ==================== CARDIOVASCULAR (15 rules) ====================
    kb["rules"].extend(
        [
            # Tăng huyết áp (5 rules)
            {
                "id": "R061",
                "module": "CARD",
                "premises": ["huyet_ap_cao"],
                "conclusion": "tang_huyet_ap",
                "confidence": 0.9,
                "notes": "Tăng huyết áp",
            },
            {
                "id": "R062",
                "module": "CARD",
                "premises": ["tang_huyet_ap", "dau_dau"],
                "conclusion": "tang_huyet_ap_nang",
                "confidence": 0.85,
                "notes": "THA nặng",
            },
            {
                "id": "R063",
                "module": "CARD",
                "premises": ["tang_huyet_ap_nang"],
                "conclusion": "uong_thuoc_ha_ap",
                "confidence": 0.95,
                "notes": "Uống thuốc",
            },
            {
                "id": "R064",
                "module": "CARD",
                "premises": ["tang_huyet_ap", "dau_nguc"],
                "conclusion": "can_kham_gap",
                "confidence": 0.95,
                "notes": "Cần khám gấp",
            },
            {
                "id": "R065",
                "module": "CARD",
                "premises": ["tang_huyet_ap"],
                "conclusion": "giam_muoi",
                "confidence": 0.9,
                "notes": "Giảm muối",
            },
            # Đau thắt ngực (6 rules)
            {
                "id": "R066",
                "module": "CARD",
                "premises": ["dau_nguc", "kho_tho"],
                "conclusion": "dau_that_nguc",
                "confidence": 0.8,
                "notes": "Đau thắt ngực",
            },
            {
                "id": "R067",
                "module": "CARD",
                "premises": ["dau_that_nguc", "ra_mo_hoi"],
                "conclusion": "nhoi_mau_co_tim",
                "confidence": 0.85,
                "notes": "Nghi nhồi máu",
            },
            {
                "id": "R068",
                "module": "CARD",
                "premises": ["nhoi_mau_co_tim"],
                "conclusion": "goi_cap_cuu_115",
                "confidence": 1.0,
                "notes": "Gọi cấp cứu",
            },
            {
                "id": "R069",
                "module": "CARD",
                "premises": ["dau_that_nguc"],
                "conclusion": "ngung_hoat_dong",
                "confidence": 0.95,
                "notes": "Nghỉ ngơi",
            },
            {
                "id": "R070",
                "module": "CARD",
                "premises": ["dau_nguc", "trai_tim"],
                "conclusion": "can_dien_tam_do",
                "confidence": 0.9,
                "notes": "Cần điện tâm đồ",
            },
            {
                "id": "R071",
                "module": "CARD",
                "premises": ["dau_nguc", "nguoi_gia"],
                "conclusion": "can_kham_gap",
                "confidence": 0.95,
                "notes": "Người già cần khám",
            },
            # Rối loạn nhịp tim (4 rules)
            {
                "id": "R072",
                "module": "CARD",
                "premises": ["tim_dap_nhanh"],
                "conclusion": "roi_loan_nhip",
                "confidence": 0.85,
                "notes": "Rối loạn nhịp",
            },
            {
                "id": "R073",
                "module": "CARD",
                "premises": ["tim_dap_cham"],
                "conclusion": "roi_loan_nhip",
                "confidence": 0.85,
                "notes": "Rối loạn nhịp",
            },
            {
                "id": "R074",
                "module": "CARD",
                "premises": ["roi_loan_nhip", "choang_vang"],
                "conclusion": "can_kham_gap",
                "confidence": 0.95,
                "notes": "Cần khám gấp",
            },
            {
                "id": "R075",
                "module": "CARD",
                "premises": ["roi_loan_nhip"],
                "conclusion": "can_dien_tam_do",
                "confidence": 0.9,
                "notes": "Cần điện tâm đồ",
            },
        ]
    )

    # ==================== ENDOCRINE (10 rules) ====================
    kb["rules"].extend(
        [
            # Đái tháo đường (6 rules)
            {
                "id": "R076",
                "module": "ENDO",
                "premises": ["duong_huyet_cao"],
                "conclusion": "dai_thao_duong",
                "confidence": 0.9,
                "notes": "Đái tháo đường",
            },
            {
                "id": "R077",
                "module": "ENDO",
                "premises": ["dai_thao_duong", "khat_nuoc"],
                "conclusion": "dai_thao_duong_type2",
                "confidence": 0.85,
                "notes": "ĐTĐ type 2",
            },
            {
                "id": "R078",
                "module": "ENDO",
                "premises": ["dai_thao_duong"],
                "conclusion": "can_kiem_soat_an_uong",
                "confidence": 0.95,
                "notes": "Kiểm soát ăn",
            },
            {
                "id": "R079",
                "module": "ENDO",
                "premises": ["dai_thao_duong"],
                "conclusion": "theo_doi_duong_huyet",
                "confidence": 0.95,
                "notes": "Theo dõi",
            },
            {
                "id": "R080",
                "module": "ENDO",
                "premises": ["dai_thao_duong", "duong_huyet_qua_cao"],
                "conclusion": "uong_thuoc",
                "confidence": 0.95,
                "notes": "Uống thuốc",
            },
            {
                "id": "R081",
                "module": "ENDO",
                "premises": ["dai_thao_duong", "tre_em"],
                "conclusion": "dai_thao_duong_type1",
                "confidence": 0.9,
                "notes": "ĐTĐ type 1",
            },
            # Tuyến giáp (4 rules)
            {
                "id": "R082",
                "module": "ENDO",
                "premises": ["co_sung", "can_giam"],
                "conclusion": "cuong_giap",
                "confidence": 0.8,
                "notes": "Cường giáp",
            },
            {
                "id": "R083",
                "module": "ENDO",
                "premises": ["met_moi", "can_tang"],
                "conclusion": "suy_giap",
                "confidence": 0.75,
                "notes": "Suy giáp",
            },
            {
                "id": "R084",
                "module": "ENDO",
                "premises": ["cuong_giap"],
                "conclusion": "xet_nghiem_hormone",
                "confidence": 0.95,
                "notes": "Xét nghiệm",
            },
            {
                "id": "R085",
                "module": "ENDO",
                "premises": ["suy_giap"],
                "conclusion": "xet_nghiem_hormone",
                "confidence": 0.95,
                "notes": "Xét nghiệm",
            },
        ]
    )

    # ==================== EMERGENCY (10 rules) ====================
    kb["rules"].extend(
        [
            # Ngất/Choáng (3 rules)
            {
                "id": "R086",
                "module": "EMER",
                "premises": ["choang_vang", "hoa_mat"],
                "conclusion": "sap_ngat",
                "confidence": 0.85,
                "notes": "Sắp ngất",
            },
            {
                "id": "R087",
                "module": "EMER",
                "premises": ["sap_ngat"],
                "conclusion": "nam_xuong",
                "confidence": 0.95,
                "notes": "Nằm xuống",
            },
            {
                "id": "R088",
                "module": "EMER",
                "premises": ["ngat"],
                "conclusion": "goi_cap_cuu_115",
                "confidence": 1.0,
                "notes": "Gọi cấp cứu",
            },
            # Chấn thương (3 rules)
            {
                "id": "R089",
                "module": "EMER",
                "premises": ["gay_xuong"],
                "conclusion": "can_nep_xuong",
                "confidence": 0.95,
                "notes": "Nẹp xương",
            },
            {
                "id": "R090",
                "module": "EMER",
                "premises": ["chay_mau_nhieu"],
                "conclusion": "can_ep_止血",
                "confidence": 1.0,
                "notes": "Cầm máu",
            },
            {
                "id": "R091",
                "module": "EMER",
                "premises": ["chan_thuong_nang"],
                "conclusion": "goi_cap_cuu_115",
                "confidence": 1.0,
                "notes": "Gọi cấp cứu",
            },
            # Sốc (2 rules)
            {
                "id": "R092",
                "module": "EMER",
                "premises": ["khó_tho", "phat_ban", "sung_mui"],
                "conclusion": "soc_phan_ve",
                "confidence": 0.9,
                "notes": "Sốc phản vệ",
            },
            {
                "id": "R093",
                "module": "EMER",
                "premises": ["soc_phan_ve"],
                "conclusion": "tiem_adrenaline",
                "confidence": 1.0,
                "notes": "Tiêm adrenaline",
            },
            # Ngừng thở/tim (2 rules)
            {
                "id": "R094",
                "module": "EMER",
                "premises": ["khong_tho"],
                "conclusion": "cap_cuu_ho_hap",
                "confidence": 1.0,
                "notes": "CPR",
            },
            {
                "id": "R095",
                "module": "EMER",
                "premises": ["tim_ngung"],
                "conclusion": "bop_tim_ngoai_long",
                "confidence": 1.0,
                "notes": "Bóp tim",
            },
        ]
    )

    # ==================== RECOMMENDATIONS (5 rules) ====================
    kb["rules"].extend(
        [
            {
                "id": "R096",
                "module": "RECO",
                "premises": ["tu_dieu_tri"],
                "conclusion": "nghi_ngoi",
                "confidence": 0.95,
                "notes": "Nghỉ ngơi",
            },
            {
                "id": "R097",
                "module": "RECO",
                "premises": ["can_kham_bac_si"],
                "conclusion": "dat_lich_kham",
                "confidence": 0.9,
                "notes": "Đặt lịch",
            },
            {
                "id": "R098",
                "module": "RECO",
                "premises": ["nhap_vien"],
                "conclusion": "chuan_bi_do_dung",
                "confidence": 0.9,
                "notes": "Chuẩn bị",
            },
            {
                "id": "R099",
                "module": "RECO",
                "premises": ["goi_cap_cuu_115"],
                "conclusion": "giu_binh_tinh",
                "confidence": 1.0,
                "notes": "Giữ bình tĩnh",
            },
            {
                "id": "R100",
                "module": "RECO",
                "premises": ["can_tai_kham"],
                "conclusion": "theo_doi_trieu_chung",
                "confidence": 0.9,
                "notes": "Theo dõi",
            },
        ]
    )

    # Form configuration
    kb["form_config"] = {
        "fields": [
            {
                "id": "F001",
                "variable": "nhiet_do",
                "label": "Nhiệt độ cơ thể (°C)",
                "type": "number",
                "options": {"min": 35, "max": 42, "step": 0.1},
                "required": True,
                "hint": "Nhiệt độ bình thường: 36-37°C",
            },
            {
                "id": "F002",
                "variable": "ho",
                "label": "Có ho không?",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F003",
                "variable": "loai_ho",
                "label": "Loại ho",
                "type": "radio",
                "options": {"options": "khan,co_dam,ra_mau"},
                "required": False,
            },
            {
                "id": "F004",
                "variable": "kho_tho",
                "label": "Mức độ khó thở (0-10)",
                "type": "range",
                "options": {"min": 0, "max": 10, "default": 0},
                "required": False,
            },
            {
                "id": "F005",
                "variable": "spo2",
                "label": "SpO2 - Nồng độ oxy trong máu (%)",
                "type": "number",
                "options": {"min": 70, "max": 100},
                "required": False,
                "hint": "Bình thường: >= 95%",
            },
            {
                "id": "F006",
                "variable": "dau_dau",
                "label": "Đau đầu",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F007",
                "variable": "met_moi",
                "label": "Mệt mỏi",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F008",
                "variable": "dau_hong",
                "label": "Đau họng",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F009",
                "variable": "chay_mui",
                "label": "Chảy nước mũi",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F010",
                "variable": "mat_vi_giac",
                "label": "Mất vị giác",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F011",
                "variable": "mat_khu_giac",
                "label": "Mất khứu giác",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F012",
                "variable": "dau_nguc",
                "label": "Đau ngực",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F013",
                "variable": "dau_bung",
                "label": "Đau bụng",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F014",
                "variable": "buon_non",
                "label": "Buồn nôn",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F015",
                "variable": "tieu_chay",
                "label": "Tiêu chảy",
                "type": "boolean",
                "required": False,
            },
            {
                "id": "F016",
                "variable": "tuoi",
                "label": "Tuổi",
                "type": "number",
                "options": {"min": 0, "max": 120},
                "required": True,
            },
        ]
    }

    # Fact extraction rules
    kb["fact_rules"] = [
        {"fact": "nhiet_do_cao", "condition": "nhiet_do > 37.5"},
        {"fact": "sot", "condition": "nhiet_do > 38"},
        {"fact": "sot_cao", "condition": "nhiet_do > 38.5"},
        {"fact": "ho_khan", "condition": "ho === true ^ loai_ho === 'khan'"},
        {"fact": "ho_co_dam", "condition": "ho === true ^ loai_ho === 'co_dam'"},
        {"fact": "dam_mau", "condition": "loai_ho === 'ra_mau'"},
        {"fact": "spo2_thap", "condition": "spo2 < 95"},
        {"fact": "spo2_binh_thuong", "condition": "spo2 >= 95"},
        {"fact": "tre_em", "condition": "tuoi < 15"},
        {"fact": "nguoi_gia", "condition": "tuoi >= 60"},
    ]

    # Recommendations
    kb["recommendations"] = [
        {
            "condition": "cam_thuong",
            "recommendation": "Nghỉ ngơi đầy đủ, uống nhiều nước (2-3 lít/ngày), dùng paracetamol nếu sốt. Nếu không đỡ sau 3 ngày hoặc triệu chứng nặng hơn, cần khám bác sĩ.",
            "priority": "Low",
        },
        {
            "condition": "covid_19",
            "recommendation": "Cách ly tại nhà, theo dõi SpO2 hàng ngày. Nếu SpO2 < 95% hoặc khó thở, đi bệnh viện ngay. Uống nhiều nước, nghỉ ngơi.",
            "priority": "High",
        },
        {
            "condition": "viem_phoi",
            "recommendation": "Cần nhập viện để điều trị kháng sinh và theo dõi. Không tự ý điều trị tại nhà.",
            "priority": "Critical",
        },
        {
            "condition": "nhoi_mau_co_tim",
            "recommendation": "GỌI CẤP CỨU 115 NGAY! Nằm yên, không vận động. Nhai thuốc aspirin nếu có.",
            "priority": "Critical",
        },
        {
            "condition": "tu_dieu_tri",
            "recommendation": "Có thể tự chăm sóc tại nhà với các triệu chứng nhẹ. Theo dõi và tái khám nếu không đỡ.",
            "priority": "Low",
        },
    ]

    return kb


if __name__ == "__main__":
    # Generate KB
    kb = generate_medical_kb()

    # Save to file
    output_path = Path(__file__).parent / "medical_kb.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

    print(f"✅ Generated Medical KB with {len(kb['rules'])} rules")
    print(f"📁 Saved to: {output_path}")
    print(f"\n📊 Summary:")
    for module in kb["metadata"]["modules"]:
        print(f"   • {module['name']}: {module['rules']} rules")
