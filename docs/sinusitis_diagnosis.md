# Hướng dẫn ngắn: Chẩn đoán Viêm Xoang (Sinusitis)

Tài liệu này giải thích ngắn gọn và dễ hiểu cách mô‑đun viêm xoang hoạt động: từ cơ sở luật, cơ chế suy diễn, đến cách tự bổ sung luật/câu hỏi/khuyến nghị.

---

## 1) Mô hình tổng quát (3 bước)
1) Người dùng trả lời phỏng vấn bác sĩ (giao diện web).
2) Hệ thống chuyển câu trả lời thô thành các “facts” chuẩn hóa (ví dụ: `trieu_chung_tren_10_ngay`, `chay_mui_dac`).
3) Engine suy diễn tiến (forward chaining) áp dụng các luật IF–THEN để suy ra chẩn đoán và khuyến nghị.

Kết quả được lưu tại `web/static/generated/<session_id>/result.json` và hiển thị ở trang `/sinusitis/results/<session_id>`.

---

## 2) Các tệp quan trọng
- Cơ sở tri thức: `data/sinusitis_kb.json`
- API/luồng phỏng vấn: `web/routes/medical_routes.py`
- Chuyển câu trả lời → facts: `medical_kb/form_generator.py`
- Engine suy diễn: `inference_lab/forward.py`
- Giao diện: `web/templates/sinusitis/*.html`, `web/static/sinusitis/*`

---

## 3) Cấu trúc cơ sở tri thức (KB)
Trong `data/sinusitis_kb.json` có bốn phần chính:

- symptoms: danh sách biến triệu chứng với `variable` và `label` (nhóm: major, minor, duration, pattern, risk_factor, red_flag…).
- diseases: các kết luận có thể suy ra (ví dụ: `viem_xoang_cap_do_vi_khuan`) kèm `label` và `severity`.
- rules: luật IF–THEN. Mỗi luật có `premises` (tiền đề) và `conclusion` (kết luận), gắn `module` (ACUTE_DIAGNOSIS, ACUTE_ETIOLOGY, CHRONIC_DIAGNOSIS, FUNGAL_DIAGNOSIS, COMPLICATIONS, DIFFERENTIAL) và `notes` (giải thích).
- fact_rules: luật suy diễn fact từ dữ liệu số/chọn lựa. Ví dụ:
  ```json
  { "condition": "thoi_gian_trieu_chung >= 10", "fact": "trieu_chung_tren_10_ngay" }
  { "condition": "nhiet_do > 38", "fact": "sot" }
  { "condition": "dau_vung_xoang_ham === true || dau_vung_xoang_tran === true", "fact": "dau_nang_mat" }
  ```

Ngoài ra có `recommendations`: khuyến nghị theo từng chẩn đoán (UI dùng dòng đầu tiên làm tóm tắt nổi bật).

---

## 4) Cơ chế suy diễn (Forward chaining)
- Input: tập facts đã chuẩn hóa từ câu trả lời.
- Lặp:
  - Tìm luật có mọi tiền đề nằm trong facts hiện có và kết luận chưa có.
  - “Bắn luật” → thêm kết luận mới vào facts; ghi nhận `fired_rules`.
  - Tiếp tục cho đến khi không bắn thêm được.
- Nếu suy ra nhiều chẩn đoán, lấy theo ưu tiên (từ nặng đến nhẹ):
  `nguy_co_bien_chung` > `viem_xoang_do_nam` > `viem_xoang_cap_do_vi_khuan` > `viem_xoang_man_tinh` > `viem_xoang_cap_do_virus` > `viem_xoang_cap`.

### Kết thúc sớm (early‑stop)
Sau mỗi câu trả lời, hệ thống chạy nhanh một vòng suy diễn. Nếu đã có chẩn đoán thật (theo thứ tự ưu tiên trên) thì dừng phỏng vấn và trả kết quả ngay. Riêng `viem_xoang_cap` cần hỏi thêm để tách nguyên nhân (thời gian bệnh, loại dịch mũi, “nặng lên sau 5–7 ngày”).

### Hỏi câu tiếp theo (dynamic)
Hệ thống tìm các luật “gần kích hoạt”, đếm những tiền đề còn thiếu và hỏi fact thiếu quan trọng nhất. Nếu không xác định được, quay về danh sách câu hỏi cố định đã sắp sẵn (red flag → thời gian → triệu chứng chính → hỗ trợ → nguy cơ).

---

## 5) Cách bổ sung/mở rộng

### 5.1 Thêm triệu chứng mới
1) Thêm vào `symptoms` (đủ `variable`, `label`, `category`).
2) Thêm câu hỏi tương ứng trong `INTERVIEW_QUESTIONS` (ở `medical_routes.py`, cùng `variable`).
3) Nếu cần biến đổi dữ liệu (số/radio → fact), thêm rule vào `fact_rules`.

### 5.2 Thêm hoặc chỉnh luật suy diễn
Thêm một entry vào `rules`, ví dụ:
```json
{
  "id": "VXC_26",
  "module": "ACUTE_ETIOLOGY",
  "premises": ["viem_xoang_cap", "sot_rat_cao"],
  "conclusion": "viem_xoang_cap_do_vi_khuan",
  "notes": "Sốt >39°C gợi ý nguy cơ bội nhiễm vi khuẩn."
}
```
Lưu ý:
- Ghi đúng `module` để phần “Luận giải của AI” lọc theo nhóm phù hợp.
- Nếu có kết luận mới, thêm nó vào `diseases` (kèm `severity`) và bổ sung `recommendations` tương ứng.

### 5.3 Cập nhật khuyến nghị
- Sửa phần `recommendations` cho chẩn đoán tương ứng. Giữ câu đầu làm tóm tắt ngắn; các dòng sau là gạch đầu dòng.

### 5.4 Tinh chỉnh luồng phỏng vấn
- Bổ sung ánh xạ trong `_get_question_for_fact` nếu xuất hiện fact mới cần hỏi.
- Tùy biến `_choose_next_question_dynamic` nếu muốn ưu tiên hỏi red flag mạnh hơn hoặc thay đổi thứ tự câu hỏi khởi đầu.

---

## 6) Ví dụ kiểm thử nhanh (Python)
```python
from medical_kb import MedicalKnowledgeBase
from inference_lab.forward import run_forward_inference

kb = MedicalKnowledgeBase(kb_path="data/sinusitis_kb.json")
result = run_forward_inference(
    kb.kb,
    goals=["viem_xoang_cap_do_vi_khuan"],
    initial_facts={"viem_xoang_cap", "sot_rat_cao"},
    strategy="stack",
    index_mode="min",
)
assert "viem_xoang_cap_do_vi_khuan" in result.final_facts
```

---

## 7) Bảng nhóm luật (tóm tắt)
| Module              | Vai trò chính |
|---------------------|----------------|
| ACUTE_DIAGNOSIS     | Nhận biết viêm xoang cấp từ triệu chứng chính |
| ACUTE_ETIOLOGY      | Phân loại nguyên nhân cấp: virus hay vi khuẩn |
| CHRONIC_DIAGNOSIS   | Phát hiện viêm xoang mạn (≥12 tuần, yếu tố nguy cơ) |
| FUNGAL_DIAGNOSIS    | Cảnh báo viêm xoang do nấm (thường ở người suy giảm miễn dịch) |
| COMPLICATIONS       | Bắt các dấu hiệu biến chứng nặng (mắt, TK) |
| DIFFERENTIAL        | Kết luận “không phải viêm xoang” khi thiếu bằng chứng |

Giữ tên module ổn định giúp bộ lọc giải thích trên trang kết quả hoạt động chính xác và đảm bảo thứ tự ưu tiên nhất quán.

---

## 8) Đầu vào và Đầu ra (chuẩn hoá và ví dụ)

### 8.1 Đầu vào từ phỏng vấn (UI fields)
- Số/ngày: `thoi_gian_trieu_chung`, `nhiet_do`
- Radio: `loai_dich_mui` ∈ {"Không có", "Trong, loãng", "Đặc, vàng/xanh"}
- Boolean triệu chứng chính: `nghet_mui`, `giam_khuu_giac`, `dau_vung_xoang_ham`, `dau_vung_xoang_tran`, `dau_vung_xoang_sang`
- Boolean mẫu diễn tiến: `trieu_chung_nang_len_sau_5_ngay` (double‑worsening)
- Boolean phụ/yếu tố nguy cơ: `ho`, `dau_dau`, `hoi_mieng`, `co_di_ung`, `co_hen_suyen`, `co_polyp_mui`, `suy_giam_mien_dich`
- Boolean red flags: `sung_quanh_mat`, `nhin_mo`, `dau_dau_du_doi`, `cung_gay`

### 8.2 Facts nội bộ sau chuẩn hoá
- Từ số:
  - `thoi_gian_trieu_chung` → `trieu_chung_duoi_10_ngay` | `trieu_chung_tren_10_ngay` | `trieu_chung_keo_dai_12_tuan`
  - `nhiet_do` → `sot` | `sot_rat_cao`
- Từ radio:
  - `loai_dich_mui` → `chay_mui_trong` | `chay_mui_dac`
- Tổng hợp:
  - `dau_nang_mat` = bất kỳ của `dau_vung_xoang_ham`/`tran`/`sang` là true

### 8.3 API phỏng vấn (vòng hỏi–đáp)
Yêu cầu (đã có các câu trả lời tạm thời):

```json
{
  "answers": {
    "thoi_gian_trieu_chung": 6,
    "nghet_mui": true,
    "loai_dich_mui": "Trong, loãng",
    "giam_khuu_giac": true
  }
}
```

Phản hồi khi CHƯA đủ kết luận:

```json
{
  "ok": true,
  "done": false,
  "question": {
    "id": "dau_vung_xoang_ham",
    "variable": "dau_vung_xoang_ham",
    "type": "boolean",
    "label": "Bạn có đau/căng tức vùng má không?"
  }
}
```

Phản hồi khi ĐÃ đủ kết luận:

```json
{
  "ok": true,
  "done": true,
  "result_url": "/sinusitis/results/abcdef123456"
}
```

### 8.4 Kết quả chẩn đoán (result.json – rút gọn)

```json
{
  "session_id": "abcdef123456",
  "diagnosis": {
    "disease": "viem_xoang_cap_do_virus",
    "disease_label": "Viêm xoang cấp do Virus",
    "severity": "low",
    "severity_raw": "Mild",
    "confidence": 100,
    "success": true
  },
  "symptoms": {
    "input": {
      "thoi_gian_trieu_chung": 6,
      "nghet_mui": true,
      "loai_dich_mui": "Trong, loãng",
      "giam_khuu_giac": true
    },
    "extracted_facts": [
      "trieu_chung_duoi_10_ngay",
      "nghet_mui",
      "giam_khuu_giac",
      "chay_mui_trong",
      "viem_xoang_cap",
      "viem_xoang_cap_do_virus"
    ]
  },
  "recommendation": "Đây có thể là viêm xoang cấp do virus, thường tự khỏi sau 7–10 ngày...\n- Nghỉ ngơi...\n- Rửa mũi...",
  "inference": {
    "fired_rules": ["VXC_04", "VXC_VIRUS_01"],
    "final_facts": ["viem_xoang_cap_do_virus", "viem_xoang_cap"],
    "steps": 2
  },
  "graphs": { "fpg": null, "rpg": null }
}
```

Ghi chú: đồ thị suy diễn (FPG/RPG) bị tắt để tối ưu tốc độ và giảm phụ thuộc.
