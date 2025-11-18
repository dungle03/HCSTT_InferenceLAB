# Hệ thống chẩn đoán viêm xoang

Tài liệu này ghi lại toàn bộ thiết kế và cách vận hành của phân hệ chẩn đoán viêm xoang trên nền tảng `inference_lab`, bao gồm: cấu trúc kiến trúc, tập tri thức, cơ chế suy luận, luồng phỏng vấn động, giao diện hiển thị kết quả, bộ kiểm thử và định hướng mở rộng.

---

## 1. Kiến trúc tổng thể

Phân hệ viêm xoang được xây dựng bằng cách tái sử dụng engine suy diễn tiến của `inference_lab` và bổ sung các lớp miền chuyên biệt:

- **Tri thức chuyên dụng**: `data/sinusitis_kb.json` chứa toàn bộ triệu chứng, luật và khuyến nghị cho xoang.
- **Adapter miền y khoa**: thư mục `medical_kb/` (đặc biệt `form_generator.py`) chuyển đổi câu trả lời thành fact.
- **Lớp web backend**: blueprint trong `web/routes/medical_routes.py` điều phối phỏng vấn và trả kết quả.
- **Giao diện chuyên biệt**: template/JS/CSS tại `web/templates/sinusitis/` và `web/static/sinusitis/`.
- **Bộ kiểm thử miền**: `tests/test_sinusitis_inference.py` đảm bảo tri thức và engine thống nhất.

### Luồng xử lý tổng quát

1. Người dùng điền câu trả lời trên giao diện phỏng vấn xoang.
2. Frontend gửi trạng thái hiện tại đến `/sinusitis/api/next_question`.
3. Backend dùng adapter để chuyển câu trả lời thành tập fact logic.
4. `run_forward_inference` chạy trên `sinusitis_kb.json` với tập fact đó.
5. Engine:
   - Hoặc kết luận sớm nếu có chẩn đoán vững chắc và điều kiện bắt buộc đã thỏa.
   - Hoặc xác định câu hỏi tiếp theo cần hỏi, dựa trên rule nào sắp được kích hoạt.
6. Khi đã kết thúc phỏng vấn, hệ thống render trang kết quả với chẩn đoán, mức độ nặng, khuyến nghị phân mảnh và giải thích từng luật.

---

## 2. Tập tri thức viêm xoang (`data/sinusitis_kb.json`)

### 2.1. Thành phần chính

File JSON này có năm phần cốt lõi:

- **metadata**: số lượng luật, triệu chứng, bệnh để dễ theo dõi quy mô.
- **symptoms**: danh sách triệu chứng quan sát được và triệu chứng dẫn xuất (derived facts).
- **diseases**: các chẩn đoán đích kèm nhãn, mô tả, mức độ nặng.
- **rules**: tập luật suy diễn tiến, phân nhóm theo module.
- **recommendations**: văn bản khuyến nghị có đánh dấu (marker) cho từng chẩn đoán.

### 2.2. Phân loại triệu chứng

Triệu chứng (atom) được chia thành nhiều cụm:

- **Triệu chứng chính**: `nghet_mui`, `dau_vung_xoang_ham`, `dau_vung_xoang_tran`, `dau_vung_xoang_mat`, `dau_nang_mat`, `giam_khuu_giac`.
- **Triệu chứng phụ**: `ho_khan`, `ho_co_dom`, `hoi_mieng`, `tiet_dich_hau_hong`, `met_moi`, `dau_dau_nhe`.
- **Thời gian & pattern**: `trieu_chung_duoi_10_ngay`, `trieu_chung_tren_10_ngay`, `trieu_chung_keo_dai_12_tuan`, `trieu_chung_nang_len_sau_5_ngay`.
- **Dịch mũi**: `co_dich_mui`, `khong_co_dich_mui`, `chay_mui_trong`, `chay_mui_dac`.
- **Tiền sử & yếu tố nguy cơ**: `tai_phat_nhieu_lan`, `co_polyp_mui`, `co_di_ung`, `co_hen_suyen`, `suy_giam_mien_dich`.
- **Dấu hiệu red flag**: `sot_rat_cao`, `sung_quanh_mat`, `nhin_mo`, `dau_dau_du_doi`, `cung_gay`.
- **Fact dẫn xuất**: `co_bang_chung_thoi_gian_cap`, `co_bang_chung_dich_cap`, `dieu_kien_cap_day_du` giúp khống chế chẩn đoán thể cấp.

### 2.3. Các atom bệnh

Danh sách chẩn đoán bao gồm cả bệnh chính và biến thể:

- Viêm xoang cấp nói chung `viem_xoang_cap`.
- Viêm xoang cấp do virus `viem_xoang_cap_do_virus`.
- Viêm xoang cấp do vi khuẩn `viem_xoang_cap_do_vi_khuan`.
- Viêm xoang cấp tái phát `viem_xoang_tai_phat`.
- Viêm xoang mạn `viem_xoang_man_tinh` và `viem_xoang_man_tinh_co_polyp`.
- Viêm xoang do nấm `viem_xoang_do_nam`.
- Nguy cơ biến chứng `nguy_co_bien_chung`.
- Trường hợp không phải xoang `khong_phai_viem_xoang`.

Mỗi bệnh có trường `label`, `severity`, `description` để template và báo cáo sử dụng.

### 2.4. Module luật

Luật được nhóm để dễ kiểm soát logic:

- **ACUTE_CONTEXT**: dựng fact về thời gian/dịch mũi, sau cùng tạo `dieu_kien_cap_day_du`.
- **ACUTE_DIAGNOSIS**: quyết định có `viem_xoang_cap` dựa trên triệu chứng chính + điều kiện cấp đầy đủ.
- **ACUTE_ETIOLOGY**: tách virus/vi khuẩn/tái phát bằng thời gian, kiểu dịch, pattern nặng lên, sốt.
- **CHRONIC_DIAGNOSIS**: nhận diện viêm xoang mạn, có thể cộng thêm polyp.
- **FUNGAL_DIAGNOSIS**: kịch bản thời gian dài, đau nhiều, suy giảm miễn dịch → `viem_xoang_do_nam`.
- **RECURRENT_ACUTE**: luật dành riêng cho `tai_phat_nhieu_lan`.
- **COMPLICATIONS**: kích hoạt `nguy_co_bien_chung` khi có red flag.
- **DIFFERENTIAL**: giúp đưa ra `khong_phai_viem_xoang` nếu thiếu tiêu chuẩn của xoang.

### 2.5. Điều kiện “gating” cho thể cấp

Mentor yêu cầu: chỉ được chẩn đoán viêm xoang cấp khi đã hỏi rõ **thời gian** và **dịch mũi**. Vì vậy:

- `dieu_kien_cap_day_du` = `co_bang_chung_thoi_gian_cap` ∧ `co_bang_chung_dich_cap`.
- Mọi luật cho `viem_xoang_cap`, `viem_xoang_cap_do_virus`, `viem_xoang_cap_do_vi_khuan`, `viem_xoang_tai_phat` đều phụ thuộc fact này.
- Nếu thông tin chưa đủ, engine buộc UI tiếp tục hỏi thay vì kết luận sớm.

### 2.6. Khuyến nghị có marker

Mỗi chẩn đoán có một chuỗi khuyến nghị chứa các marker cố định để frontend cắt ra từng thẻ:

- `@summary:` – mô tả ngắn gọn.
- `@drivers:` – lý do và triệu chứng chính.
- `@home_care:` – chăm sóc tại nhà.
- `@medical_visit:` – khi nào cần đi khám bác sĩ.
- `@follow_up:` – kế hoạch tái khám/theo dõi.
- `@emergency:` – dấu hiệu nguy cấp.
- `@notes:` – ghi chú thêm.

---

## 3. Ánh xạ câu trả lời thành fact (`medical_kb/form_generator.py`)

Hàm `extract_facts_from_form` xử lý JSON câu trả lời:

- Trường boolean (ví dụ `nghet_mui`, `dau_vung_xoang_ham`) → nếu `True` thì thêm fact cùng tên.
- Trường số `thoi_gian_trieu_chung` → engine dùng để suy ra các fact thời gian qua luật của KB.
- Trường chuỗi `loai_dich_mui` → chuẩn hóa chữ thường, kiểm tra từ khóa để thêm `khong_co_dich_mui`, `co_dich_mui`, `chay_mui_trong`, `chay_mui_dac`.

Lớp adapter này đảm bảo dù người dùng nhập hơi khác nhau thì engine vẫn nhận được các atom chuẩn xác.

---

## 4. Luồng phỏng vấn động (`web/routes/medical_routes.py`)

### 4.1. Blueprint & endpoint

- Blueprint đăng ký với `url_prefix="/sinusitis"` và sử dụng template trong `web/templates/sinusitis/`.
- Các route chính:
  - `GET /sinusitis/interview`: hiển thị giao diện phỏng vấn.
  - `POST /sinusitis/api/next_question`: nhận câu trả lời hiện tại, chạy suy luận, quyết định dừng hay hỏi tiếp.
  - `GET /sinusitis/results/<session_id>`: render trang kết quả.

### 4.2. Ngân hàng câu hỏi

`INTERVIEW_QUESTIONS` liệt kê khoảng 20 câu hỏi, mỗi câu có `key`, `text`, `type`. Phạm vi bao gồm:

- Câu hỏi red flag (sốt rất cao, sưng quanh mắt, nhìn mờ...).
- Triệu chứng chính/phụ.
- Thời gian, pattern double-worsening.
- Dịch mũi.
- Yếu tố nguy cơ và tiền sử tái phát.

### 4.3. Mapping fact → câu hỏi

Hàm `_get_question_for_fact` dùng để ánh xạ fact dẫn xuất về câu hỏi gốc (ví dụ `co_bang_chung_thoi_gian_cap` → `thoi_gian_trieu_chung`). Điều này cho phép engine “yêu cầu” thêm dữ kiện nâng cao mà UI vẫn biết phải hỏi người dùng điều gì.

### 4.4. Thuật toán chọn câu hỏi mới

1. Chuyển câu trả lời hiện tại thành `known_facts`.
2. Duyệt các luật, xác định tiên đề đã thỏa và tiên đề còn thiếu.
3. Với mỗi tiên đề thiếu, map về câu hỏi tương ứng và cộng điểm.
4. Ưu tiên các luật dẫn đến chẩn đoán nguy hiểm (biến chứng, nấm, vi khuẩn...).
5. Chọn câu hỏi có điểm cao nhất mà chưa được trả lời. Nếu hết câu phù hợp, dùng fallback thứ tự cố định.

### 4.5. Cơ chế dừng sớm

Sau mỗi câu trả lời, hệ thống thử chạy `run_forward_inference`:

- Nếu nhận được chẩn đoán cụ thể, đáp ứng điều kiện gating và không bị chẩn đoán nặng hơn phủ nhận → kết thúc phỏng vấn, lưu session và trả về URL kết quả.
- Nếu chỉ có kết luận chung chung (vd mới có `viem_xoang_cap` nhưng thiếu dữ kiện), hệ thống tiếp tục hỏi.

---

## 5. Trang kết quả (`web/templates/sinusitis/`)

### 5.1. Nội dung hiển thị

Trang kết quả cho mỗi session hiển thị:

- Tên chẩn đoán + mức độ nặng (lấy từ metadata).
- Danh sách triệu chứng quan trọng (facts chính).
- Khuyến nghị phân chia theo các marker (`@summary`, `@home_care`, ...).
- Bảng giải thích luật: module, mô tả, tiên đề đã thỏa, kết luận.

### 5.2. Ưu tiên tính minh bạch

Nhờ bảng luật, mentor/bác sĩ có thể rà soát vì sao engine đưa ra kết luận, từ đó góp ý điều chỉnh ngưỡng hoặc bổ sung luật mới.

---

## 6. Kiểm thử (`tests/test_sinusitis_inference.py`)

### 6.1. Bộ kịch bản chuẩn

`SCENARIOS` định nghĩa nhiều hồ sơ bệnh nhân bao phủ các thể bệnh: cấp do virus, cấp do vi khuẩn, cấp tái phát, mạn có polyp, nấm, nguy cơ biến chứng.

### 6.2. Test suy diễn

`test_forward_inference_matches_medical_expectation`:

- Chạy `_infer_diagnosis` cho từng scenario.
- Đảm bảo tất cả `expected_facts` xuất hiện trong `final_facts`.
- Kiểm tra `severity` của chẩn đoán khớp với metadata.

### 6.3. Test khuyến nghị

`test_recommendations_remain_structured` đảm bảo mỗi khuyến nghị bắt đầu bằng `@summary:` và chứa đủ các marker quan trọng (`@home_care`, `@medical_visit`, `@follow_up`, `@emergency`).

---

## 7. Các cải tiến chính theo góp ý

1. **Điều kiện cấp chặt chẽ**: thêm `co_bang_chung_thoi_gian_cap`, `co_bang_chung_dich_cap`, `dieu_kien_cap_day_du` để không chẩn đoán cấp thiếu dữ kiện.
2. **Phân biệt virus/vi khuẩn rõ ràng**: dùng thời gian, kiểu dịch, sốt, double-worsening trong module `ACUTE_ETIOLOGY`.
3. **Bổ sung chẩn đoán tái phát**: fact `tai_phat_nhieu_lan` và module `RECURRENT_ACUTE`.
4. **Theo dõi/tái khám**: mọi khuyến nghị đều có `@follow_up` giải thích khi nào cần quay lại bác sĩ.
5. **Tính giải thích cao**: trang kết quả hiển thị nguồn gốc từng chẩn đoán để phục vụ báo cáo và thảo luận.

---

## 8. Định hướng mở rộng

Để phát triển thêm phân hệ này, có thể:

1. **Bổ sung triệu chứng/derived fact** trong `data/sinusitis_kb.json` khi có guideline mới.
2. **Điều chỉnh ngưỡng** (số ngày, mức sốt, tần suất tái phát) cho phù hợp dữ liệu thực tế.
3. **Thêm chẩn đoán mới** (ví dụ phân biệt thêm phenotype viêm xoang mạn) cùng rules và recommendation tương ứng.
4. **Mở rộng ngân hàng câu hỏi** và điều chỉnh thuật toán chọn câu hỏi.
5. **Thêm scenario test** để bao phủ ca biên hoặc ca hiếm.

Sau mỗi thay đổi, chạy lại:

```pwsh
python -m pytest tests/test_sinusitis_inference.py
```

nhằm đảm bảo engine, tập tri thức và giao diện luôn đồng bộ, ổn định.
