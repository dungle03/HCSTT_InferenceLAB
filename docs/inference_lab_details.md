# Báo cáo Chi tiết Mô-đun `inference_lab`

## 1. Vai trò tổng quan

`inference_lab` là mô-đun lõi cài đặt **engine suy diễn dựa trên luật** của project. Nó chịu trách nhiệm:

- Biểu diễn tập luật (rules), fact, và mục tiêu (goals) dưới dạng cấu trúc dữ liệu rõ ràng.
- Thực hiện **suy diễn tiến (Forward Chaining)** và **suy diễn lùi (Backward Chaining)** độc lập với miền tri thức cụ thể.
- Cung cấp **kết quả suy luận + vết suy luận (trace)** để các lớp bên trên (web UI, hệ chẩn đoán xoang, medical KB) có thể hiển thị và giải thích.
- Tùy chọn sinh **đồ thị suy diễn (FPG, RPG)** bằng Graphviz để trực quan hóa.

Các hệ thống như chẩn đoán xoang, medical diagnosis, v.v. chỉ cần xây dựng Knowledge Base riêng (JSON) và gọi chung engine trong `inference_lab`.

---

## 2. Cấu trúc thư mục `inference_lab`

```text
inference_lab/
  __init__.py
  forward.py         # Suy diễn tiến
  backward.py        # Suy diễn lùi
  graphs.py          # Vẽ và sinh đồ thị suy diễn
  knowledge_base.py  # Lớp quản lý KB (rules, facts, goals)
  models.py          # Định nghĩa Rule, Atom, v.v.
  results.py         # Định nghĩa kết quả Forward/Backward
  sample_data.py     # Bộ luật mẫu (tam giác)
  utils.py           # Hàm parse và tiện ích chung
  web/               # Phần web cho Inference Lab (nếu dùng giao diện Lab)
```

Dưới đây là mô tả chi tiết từng phần.

---

## 3. `models.py` – Các cấu trúc dữ liệu lõi

File này định nghĩa các kiểu dữ liệu trung tâm cho engine:

- **`Rule`**:
  - `id`: định danh rule (sử dụng khi trace).
  - `premises`: danh sách mã fact đầu vào (ví dụ: `['a', 'b']` hoặc `['nghet_mui', 'dau_nang_mat']`).
  - `conclusion`: fact kết luận (ví dụ: `"viem_xoang_cap"`).
  - `module`: nhóm logic (ví dụ: `ACUTE_DIAGNOSIS`, `CHRONIC_DIAGNOSIS`), dùng để lọc giải thích.
  - `confidence` / `notes` (nếu có): phục vụ hiển thị.

Ngoài ra có thể có:

- Kiểu cho "atom" hoặc fact đơn lẻ.
- Kiểu enum/constant cho chiến lược (`stack/queue`, `min/max`).

Mục đích của `models.py` là gom chung các định nghĩa, giúp toàn bộ engine dùng chung một “ngôn ngữ” để thao tác rules/facts.

---

## 4. `knowledge_base.py` – Lớp quản lý Tri thức

`knowledge_base.py` chịu trách nhiệm:

- Nạp danh sách rules và (tuỳ trường hợp) các facts/metadata từ nguồn dữ liệu (JSON, sample).
- Cung cấp API cho engine, ví dụ:
  - `get_rules()`: trả về toàn bộ rules.
  - `get_goals()` / `get_diseases()`: trả danh sách fact kết luận quan trọng.
  - `index_rules_by_premise()`: lập chỉ mục rule theo premise để tăng tốc Forward Chaining.

Ý tưởng chính:

- Thay vì mỗi vòng lặp phải duyệt toàn bộ rules, `KnowledgeBase` xây dựng một map:

  ```text
  premise_atom  ->  [rule_1, rule_5, ...]
  ```

- Khi một fact mới được suy ra, engine chỉ xét những rule có liên quan đến fact đó.

Nhờ đó, hiệu năng Forward Chaining được cải thiện đáng kể khi số lượng rule tăng.

---

## 5. `forward.py` – Thuật toán Suy diễn tiến

### 5.1. Hàm chính: `run_forward_inference`

Hàm này nhận vào:

- `kb`: đối tượng KnowledgeBase, đã chứa danh sách Rule.
- `initial_facts`: tập fact ban đầu.
- `goals`: danh sách fact mục tiêu (các chẩn đoán hoặc kết luận cần tìm).
- `strategy`: `'stack'` hoặc `'queue'` – chọn THOA (LIFO/FIFO).
- `index_mode`: `'min'` hoặc `'max'` – ưu tiên rule có ID nhỏ/lớn.
- `make_graphs`: có sinh đồ thị suy diễn hay không.

### 5.2. Quy trình core

1. **Khởi tạo**:
   - `facts = set(initial_facts)`; `agenda` chứa tất cả fact ban đầu.
   - `fired_rules = []` để lưu id rule đã bắn.
   - Dùng `kb` để tạo cấu trúc chỉ mục `premise_index`.

2. **Vòng lặp suy diễn**:
   - Lấy một fact từ `agenda` theo chiến lược:
     - `stack`: dùng ngăn xếp (LIFO).
     - `queue`: dùng hàng đợi (FIFO).
   - Từ fact đó, tìm tất cả rule có chứa premise tương ứng.
   - Với mỗi rule:
     - Nếu **chưa bắn** và **tất cả premises** nằm trong `facts`:
       - Thêm `conclusion` vào `facts`.
       - Thêm `conclusion` vào `agenda`.
       - Ghi lại rule vào `fired_rules` và `history`.

3. **Điều kiện dừng**:
   - Khi `agenda` rỗng (không suy ra được fact mới).
   - Hoặc khi đã thu được một trong các `goals` ưu tiên (có thể cấu hình tuỳ domain).

4. **Kết quả (`ForwardResult`)**:
   - `final_facts`: tất cả facts đã suy ra.
   - `fired_rules`: danh sách ID rule theo thứ tự kích hoạt.
   - `history`: log chi tiết các bước suy luận.
   - `success`: `True` nếu ít nhất một goal được đáp ứng.

### 5.3. Chiến lược THOA & ưu tiên

- **Stack vs Queue**:
  - *Stack*: ưu tiên rule “mới nhất” → giống DFS, đi sâu theo một nhánh suy luận.
  - *Queue*: ưu tiên rule được xếp từ sớm → giống BFS, trải đều hơn.

- **Min vs Max index**:
  - Min: phù hợp khi các rule ID nhỏ mang tính “gốc” hoặc “quan trọng” hơn.
  - Max: hữu ích khi muốn ưu tiên những rule mới được thêm sau cùng.

Việc cho phép thay đổi các tham số này là điểm mạnh giáo dục của Inference Lab: sinh viên có thể quan sát cùng một KB nhưng trace suy luận khác nhau.

---

## 6. `backward.py` – Thuật toán Suy diễn lùi

Backward Chaining là **goal-driven**: xuất phát từ kết luận muốn chứng minh, đi ngược lại tìm xem cần những fact nào.

### 6.1. Ý tưởng

Giả sử goal là `G`:

1. Nếu `G` đã nằm trong tập fact đã biết → chứng minh xong.
2. Nếu không, tìm các rule có `conclusion == G`.
3. Với mỗi rule đó:
   - Xem các `premises` là các **sub-goal** cần chứng minh.
   - Gọi đệ quy để tìm xem từng premise có thể suy ra từ facts ban đầu hay không.
4. Nếu có một rule mà tất cả premises chứng minh được, coi goal `G` là chứng minh được.

### 6.2. Triển khai

Trong `backward.py`:

- Dùng DFS với tập `visited` để tránh lặp vô hạn (vòng lặp trên graph rule).
- Xây dựng một cấu trúc kết quả (`BackwardResult`) bao gồm:
  - Cây chứng minh: goal → rule → premises → ... → facts đầu vào.
  - Thông tin rule đã sử dụng.

Backward đặc biệt hữu ích khi cần **giải thích vì sao** một kết luận đúng

---

## 7. `graphs.py` – Đồ thị FPG & RPG

`graphs.py` dùng thư viện `graphviz` để trực quan hóa quá trình suy luận.

### 7.1. FPG – Forward Proof Graph

- Node: các fact.
- Edge: biểu diễn một rule đi từ tập premises đến conclusion.
- Thường hiển thị theo chiều từ trái sang phải hoặc trên xuống dưới, để người xem thấy rõ đường suy luận.

### 7.2. RPG – Rule/Reasoning Graph

- Node: các rule.
- Edge: rule A → rule B nếu conclusion của A là premise của B.
- Dùng để xem **mối quan hệ phụ thuộc giữa rule với rule**.

Các hàm trong `graphs.py` thường nhận:

- `ForwardResult` hoặc `BackwardResult`.
- Đường dẫn output.

Sau đó sinh ra file `.svg`/`.png` đặt trong thư mục static (`web/static/generated/`) để UI có thể hiển thị.

---

## 8. `sample_data.py` – Bộ ví dụ luật Tam giác

Bộ ví dụ tam giác minh họa một domain toán học đơn giản:

- Facts:
  - `a`, `b`, `c`: độ dài cạnh.
  - `goc_A`, `goc_B`, `goc_C`: góc.
  - `tam_giac_vuong`, `tam_giac_deu`, `tam_giac_can`.
  - `dien_tich`.

- Rules tiêu biểu:
  - Nếu `a`, `b` đã biết và tam giác vuông tại A → suy ra `c` theo Pythagore.
  - Nếu `a = b = c` → `tam_giac_deu`.
  - Nếu `a = b` nhưng `c` khác → `tam_giac_can`.

Mục đích:

- Cho phép chạy thử engine với input rất dễ hiểu.
- Dùng trong giao diện Inference Lab để demo: nhập `a=3, b=4` và yêu cầu goal `c`, sinh viên quan sát các bước suy luận.

---

## 9. `utils.py` – Các hàm tiện ích

`utils.py` thường chứa:

- Hàm parse chuỗi input (ví dụ: `"a=3, b=4"`) thành tập fact chuẩn.
- Hàm chuẩn hóa tên biến: cắt khoảng trắng, chuyển lower-case, v.v.
- Các helper cho logging, merge kết quả, xử lý ngoại lệ.

Nhờ đó, code trong `forward.py` và `backward.py` gọn sạch hơn, tập trung vào logic chính.

---

## 10. Thư mục `inference_lab/web/`

Thư mục con `web/` trong `inference_lab` (nếu còn dùng) liên quan đến **giao diện Lab**:

- Blueprint Flask cho `/lab`.
- Template HTML + JavaScript để người dùng:
  - Chọn mode Forward/Backward.
  - Chọn Stack/Queue, Min/Max.
  - Nhập tập facts và goals.
  - Xem bảng THOA, trace suy luận, và đồ thị FPG/RPG.

Ở bản hiện tại, phần chẩn đoán xoang dùng một web module riêng trong thư mục `web/` gốc, nhưng tư tưởng là giống nhau: cả hai đều gọi chung tới engine trong `inference_lab`.

---

## 11. Quan hệ với các phần khác của project

- **Medical KB / Sinusitis**:
  - Các module như `medical_kb` và KB xoang dựng tri thức riêng (triệu chứng, bệnh, rule y khoa).
  - Sau đó gọi trực tiếp hàm `run_forward_inference` từ `inference_lab.forward` để suy luận.

- **Tests**:
  - `tests/test_medical_diagnosis.py` và `tests/test_sinusitis_inference.py` đều dựa vào engine này để kiểm tra logic.

Điều này chứng minh `inference_lab` là **một engine tổng quát**, không bị buộc vào bất kỳ domain cụ thể nào.

---

## 12. Gợi ý trình bày khi báo cáo với giảng viên

Khi trình bày về `inference_lab`, bạn có thể đi theo flow:

1. **Giới thiệu tổng quan**:
   - Đây là mô-đun engine suy luận, độc lập với miền tri thức.
   - Cài đặt đầy đủ Forward & Backward Chaining, có thể minh họa trong môn học.

2. **Đi qua cấu trúc file**:
   - Lần lượt nói ngắn gọn: `models.py` (cấu trúc dữ liệu), `knowledge_base.py` (nạp và index tri thức), `forward.py` & `backward.py` (thuật toán), `graphs.py` (đồ thị), `sample_data.py` (bộ ví dụ), `utils.py` (tiện ích).

3. **Minh họa thuật toán**:
   - Vẽ sơ đồ nhỏ cho Forward Chaining: facts ban đầu → rule → fact mới → ...
   - Giải thích ý nghĩa Stack/Queue, Min/Max, và cho ví dụ đơn giản.

4. **Kết nối với ứng dụng thực tế**:
   - Nhấn mạnh: hệ chẩn đoán xoang chỉ là một instance của engine này với một Knowledge Base y khoa cụ thể.

5. **Kiểm thử & Đảm bảo chất lượng**:
   - Nêu rằng engine được kiểm tra gián tiếp thông qua các bộ test domain (đặc biệt bộ test viêm xoang chuyên sâu).

Với file này, bạn có thể dùng như “script” khi báo cáo, hoặc trích ra thành slide/handout cho thầy đều được.
