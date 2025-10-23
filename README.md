# 🧠 Intelligent Diagnosis System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Hệ thống chẩn đoán thông minh kết hợp **Inference Engine** (suy diễn tiến/lùi) và **Medical Diagnosis** (chẩn đoán y tế AI) phục vụ nghiên cứu và học tập về Hệ chuyên gia.

---

## ✨ Tính năng chính

### 🔬 Inference Lab - Module Suy diễn Chuyên gia

Giao diện dành cho nhà phát triển/nhà nghiên cứu để thao tác trực tiếp với tri thức:

#### **Suy diễn tiến (Forward Chaining)**
- 🎯 **2 chiến lược THOA**: Stack (LIFO) hoặc Queue (FIFO)
- 📊 **Chỉ số ưu tiên**: Min (ưu tiên rule ID nhỏ) hoặc Max (ưu tiên rule ID lớn)
- 📈 **Đồ thị FPG/RPG**: Visualize quá trình suy diễn với Graphviz
- 🔍 **Bảng THOA**: Theo dõi chi tiết từng bước suy diễn

#### **Suy diễn lùi (Backward Chaining)**
- 🎯 **Goal-driven reasoning**: Từ mục tiêu ngược về sự kiện
- 🌳 **DFS với kiểm soát vòng lặp**: Tránh infinite recursion
- 📊 **Chỉ số mục tiêu**: Min/Max priority cho rule selection
- 📈 **FPG Graph**: Visualize cây chứng minh

#### **Dữ liệu mẫu**
- 📐 **16 luật tam giác**: Tính cạnh, góc, diện tích
- ✏️ **Custom rules**: Nhập luật tùy chỉnh để test

### 🏥 Medical Diagnosis - Hệ thống Chẩn đoán Y tế AI

Giao diện thân thiện cho người dùng cuối (bệnh nhân):

#### **Knowledge Base**
- 📚 **109 medical rules** từ `medical_kb.json`
- 🦠 **20 bệnh phổ biến**: Cảm cúm, COVID-19, viêm phổi, viêm họng, hen suyễn, viêm dạ dày, ngộ độc thực phẩm...
- 🩺 **30+ triệu chứng**: Sốt, ho, đau đầu, khó thở, đau bụng, buồn nôn...
- 🏷️ **7 modules**: SYMP, RESP, DIGE, CARD, ENDO, EMER, RECO

#### **Smart Diagnosis Scorer**
Hệ thống chấm điểm thông minh với thuật toán Weighted Evidence Accumulation:

- 🎯 **Trọng số triệu chứng**: Mỗi triệu chứng có trọng số khác nhau (0.0-1.0)
- ➕ **Positive Evidence**: Triệu chứng phù hợp tăng điểm (+)
- ➖ **Negative Evidence**: Triệu chứng trái ngược giảm điểm (-)
- 🎁 **Combo Bonuses**: Thưởng điểm khi có tổ hợp triệu chứng đặc trưng
- ⚠️ **Severity Penalties**: Phạt khi bệnh nhẹ nhưng có triệu chứng nặng
- 📊 **Prior Probability**: Xác suất tiền nghiệm từ thống kê y tế
- 🏆 **Top 2-3 Diagnoses**: Hiển thị các bệnh có khả năng cao nhất

#### **UI/UX**
- 🧙 **Wizard Form**: Form nhập triệu chứng từng bước
- 📊 **Confidence Score**: Hiển thị độ tin cậy (0-100%)
- 🎨 **Severity Color**: Low (xanh) / Medium (vàng) / High (đỏ)
- 💊 **Treatment Recommendations**: Khuyến nghị điều trị cụ thể
- 📈 **Inference Visualization**: Xem quá trình inference (optional)

## 📁 Kiến trúc Project

```
intelligent-diagnosis-system/
│
├── 📂 inference_lab/              # ⚙️ Core Inference Engine
│   ├── forward.py                 # Suy diễn tiến (Stack/Queue + Min/Max)
│   ├── backward.py                # Suy diễn lùi (DFS + Goal-driven)
│   ├── graphs.py                  # FPG/RPG Graphviz visualization
│   ├── knowledge_base.py          # Quản lý rules & facts
│   ├── models.py                  # Rule dataclass
│   ├── results.py                 # ForwardResult, BackwardResult
│   ├── sample_data.py             # 16 rules tam giác
│   ├── utils.py                   # Parse utilities
│   └── web/                       # Sub-module (deprecated, moved to /web)
│
├── 📂 medical_kb/                 # 🏥 Medical Knowledge Base
│   ├── loader.py                  # Load & manage medical_kb.json
│   ├── form_generator.py          # Generate dynamic symptom forms
│   └── validator.py               # Validate KB consistency
│
├── 📂 data/
│   ├── medical_kb.json            # 109 rules + 20 diseases + 30 symptoms
│   └── generate_medical_kb.py    # Script to generate/update KB
│
├── 📂 web/                        # 🌐 Flask Web Application
│   ├── __init__.py                # Flask app factory + cleanup
│   ├── diagnosis_scorer.py       # 🧠 Smart Diagnosis Scorer (AI core)
│   │
│   ├── 📂 routes/
│   │   ├── __init__.py            # Blueprint exports
│   │   ├── lab_routes.py          # /lab/* - Inference Lab API
│   │   └── medical_routes.py     # /medical/* - Medical Diagnosis API
│   │
│   ├── 📂 templates/
│   │   ├── home.html              # Landing page (choose Lab or Medical)
│   │   ├── index.html             # Inference Lab UI
│   │   └── medical/
│   │       ├── landing.html       # Medical homepage
│   │       ├── wizard.html        # Symptom input wizard
│   │       ├── results.html       # Diagnosis results
│   │       └── error.html         # Error page
│   │
│   └── 📂 static/
│       ├── app.js                 # Inference Lab JavaScript
│       ├── generated/             # Auto-generated graphs (auto-cleanup)
│       └── medical/
│           ├── medical.css        # Medical UI styles
│           ├── medical.js         # Medical wizard logic
│           └── images/            # Medical assets
│
├── 📂 tests/                      # ✅ Automated test suite (pytest)
│   └── test_medical_diagnosis.py  # Integration tests for medical API
│
├── run.py                         # 🚀 Main entry point
├── requirements.txt               # Python dependencies
└── README.md                      # Documentation (this file)
```

### 📦 Modules chính

| Module | Mô tả | Key Files |
|--------|-------|-----------|
| **inference_lab** | Engine suy diễn core | `forward.py`, `backward.py`, `graphs.py` |
| **medical_kb** | Knowledge base y tế | `loader.py`, `medical_kb.json` |
| **web** | Flask application | `routes/`, `templates/`, `static/` |
| **web.diagnosis_scorer** | AI scoring system | `diagnosis_scorer.py` |
| **tests** | Pytest integration suite | `tests/test_medical_diagnosis.py` |

## 🚀 Hướng dẫn Cài đặt

### Yêu cầu hệ thống

- **Python**: ≥ 3.10
- **Graphviz**: ≥ 2.38 (cho visualization)
- **OS**: Windows / macOS / Linux

### Bước 1: Clone repository

```bash
git clone https://github.com/dungle03/HCSTT_InferenceLAB.git
cd intelligent-diagnosis-system
```

### Bước 2: Tạo môi trường ảo (Virtual Environment)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Bước 3: Cài đặt Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencies:**
```
Flask==3.1.2      # Web framework
networkx==3.5     # Graph algorithms
graphviz==0.21    # Graph visualization
pytest==8.2.0     # Test runner (development)
```

### Bước 4: Cài đặt Graphviz (System)

Graphviz cần được cài đặt ở cấp hệ điều hành để xuất đồ thị FPG/RPG.

**Windows:**
1. Tải installer từ: https://graphviz.org/download/
2. Chạy installer và chọn "Add Graphviz to system PATH"
3. Verify: `dot -V` trong PowerShell

**macOS (Homebrew):**
```bash
brew install graphviz
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install graphviz
```

**Verify installation:**
```bash
dot -V
# Output: dot - graphviz version X.X.X
```

### Bước 5: Chạy ứng dụng

```bash
python run.py
```

**Console output:**
```
============================================================
🧠 Intelligent Diagnosis System
============================================================
✅ Inference Lab: http://127.0.0.1:5000/lab
✅ Medical Diagnosis: http://127.0.0.1:5000/medical
============================================================
 * Running on http://127.0.0.1:5000
```

### Bước 6: Truy cập trong trình duyệt

- **🏠 Home**: http://127.0.0.1:5000
- **🔬 Inference Lab**: http://127.0.0.1:5000/lab  
- **🏥 Medical Diagnosis**: http://127.0.0.1:5000/medical

---

## 📖 Hướng dẫn Sử dụng

### 🔬 Inference Lab

1. Truy cập http://127.0.0.1:5000/lab
2. **Load Sample Data**: Click "Load Triangle Rules" để nạp 16 luật tam giác
3. **Chọn Mode**: Forward hoặc Backward
4. **Cấu hình Options**:
   - Forward: Stack/Queue + Min/Max
   - Backward: Min/Max priority
5. **Nhập Facts**: Ví dụ: `a=3, b=4`
6. **Nhập Goals**: Ví dụ: `c, dien_tich`
7. **Run Inference**: Xem kết quả và đồ thị FPG/RPG

### 🏥 Medical Diagnosis

1. Truy cập http://127.0.0.1:5000/medical
2. Click **"Bắt đầu Chẩn đoán"**
3. **Nhập triệu chứng** theo wizard:
   - Nhiệt độ (°C)
   - Các triệu chứng: Ho, Đau đầu, Khó thở...
   - SpO2 (%)
   - Tuổi
4. **Submit**: Hệ thống chạy inference và chấm điểm
5. **Xem kết quả**:
   - Top 2-3 bệnh có khả năng cao nhất
   - Confidence score (0-100%)
   - Severity level (Low/Medium/High)
   - Treatment recommendations
   - Matched symptoms

---

## 🧪 Testing

### Automated Tests

```bash
# Chạy toàn bộ bộ test tích hợp Medical Diagnosis
pytest tests/test_medical_diagnosis.py
```

Các bài test này gửi payload giả lập tới `/medical/api/diagnose` để đảm bảo kết quả trả về ổn định:

- **test_severe_upper_respiratory_symptoms_surface_pharyngitis**: xác nhận triệu chứng hô hấp nặng ưu tiên chẩn đoán `viem_hong` với độ tin cậy đủ cao.
- **test_digestive_symptoms_rank_food_poisoning_or_gastritis_highest**: đảm bảo triệu chứng đường tiêu hoá ưu tiên `ngo_doc_thuc_pham`/`viem_da_day`.

> 💡 *Pytest cần được cài (đã khai báo trong `requirements.txt`). Nếu muốn chạy tất cả test sau này, hãy mở rộng thư mục `tests/` và dùng `pytest tests/`.*

### Manual Testing Checklist

#### Inference Lab
- [ ] Load triangle sample data
- [ ] Forward inference với Stack + Min
- [ ] Forward inference với Queue + Max
- [ ] Backward inference với Min priority
- [ ] Backward inference với Max priority
- [ ] View FPG graph (SVG)
- [ ] View RPG graph (SVG)
- [ ] Custom rules input
- [ ] Parse errors handling

#### Medical Diagnosis
- [ ] Symptom wizard form navigation
- [ ] Temperature input (°C)
- [ ] Boolean symptoms (checkboxes)
- [ ] SpO2 input (%)
- [ ] Age input
- [ ] Submit và receive results
- [ ] Top 2-3 diagnoses display
- [ ] Confidence scores (0-100%)
- [ ] Severity colors (Low/Medium/High)
- [ ] Treatment recommendations
- [ ] Edge case: No symptoms → Error message
- [ ] Edge case: Ambiguous symptoms → Multiple diagnoses

---

## 🛠 Development

### Thêm bệnh mới vào Medical KB

Edit `data/medical_kb.json`:

```json
{
  "diseases": [
    {
      "id": "D021",
      "variable": "benh_moi",
      "label": "Tên Bệnh Mới",
      "severity": "Moderate",
      "description": "Mô tả bệnh..."
    }
  ],
  "rules": [
    {
      "id": "R110",
      "module": "RESP",
      "premises": ["trieu_chung_1", "trieu_chung_2", "trieu_chung_3"],
      "conclusion": "benh_moi",
      "description": "Rule mô tả..."
    }
  ],
  "recommendations": [
    {
      "condition": "benh_moi",
      "recommendation": "Khuyến nghị điều trị..."
    }
  ]
}
```

### Thêm trọng số triệu chứng cho Smart Scorer

Edit `web/diagnosis_scorer.py`:

```python
self.symptom_weights = {
    "benh_moi": {
        "trieu_chung_1": 0.90,  # Triệu chứng đặc trưng
        "trieu_chung_2": 0.75,  # Triệu chứng phổ biến
        "trieu_chung_3": 0.60,  # Triệu chứng phụ
        "trieu_chung_trai_nguoc": -0.40,  # Phản bác
    }
}

self.priors = {
    "benh_moi": 0.05,  # 5% xác suất tiền nghiệm
}
```

### Tùy chỉnh UI

- **Inference Lab UI**: `web/templates/index.html` + `web/static/app.js`
- **Medical UI**: `web/templates/medical/` + `web/static/medical/`
- **Styles**: Sử dụng Tailwind CSS CDN (đã có sẵn)

### Debug Mode

Enable Flask debug mode:

```python
# run.py
app.run(host="127.0.0.1", port=5000, debug=True)  # Change to True
```

**Lưu ý**: Debug mode tự động reload khi code thay đổi.

---

## 📊 Knowledge Base Details

### 🏥 Medical KB Structure

**File**: `data/medical_kb.json`

```json
{
  "version": "1.0.0",
  "metadata": {
    "total_rules": 109,
    "total_symptoms": 30,
    "total_diseases": 20
  },
  "modules": [
    { "code": "SYMP", "name": "Triệu chứng cơ bản", "rules": 15 },
    { "code": "RESP", "name": "Hô hấp", "rules": 32 },
    { "code": "DIGE", "name": "Tiêu hóa", "rules": 22 },
    { "code": "CARD", "name": "Tim mạch", "rules": 15 },
    { "code": "ENDO", "name": "Nội tiết", "rules": 10 },
    { "code": "EMER", "name": "Cấp cứu", "rules": 10 },
    { "code": "RECO", "name": "Khuyến nghị", "rules": 5 }
  ]
}
```

#### Diseases (20 bệnh)

| ID | Variable | Label | Severity |
|----|----------|-------|----------|
| D001 | cam_thuong | Cảm cúm thông thường | Mild |
| D002 | nghi_covid | Nghi ngờ COVID-19 | Moderate |
| D003 | covid_19 | COVID-19 | Moderate |
| D004 | covid_nhe | COVID-19 thể nhẹ | Mild |
| D005 | covid_nang | COVID-19 thể nặng | Severe |
| D006 | viem_phoi | Viêm phổi | Severe |
| D007 | hen_suyen | Hen suyễn | Moderate |
| D008 | viem_hong | Viêm họng | Mild |
| D009 | viem_da_day | Viêm dạ dày | Moderate |
| D010 | ngo_doc_thuc_pham | Ngộ độc thực phẩm | Moderate |
| ... | ... | ... | ... |

#### Symptoms (30+ triệu chứng)

| ID | Variable | Label | Type |
|----|----------|-------|------|
| S001 | nhiet_do_cao | Nhiệt độ cao | Derived |
| S002 | sot | Sốt | Input |
| S003 | sot_cao | Sốt cao | Derived |
| S004 | ho | Ho | Input |
| S005 | ho_khan | Ho khan | Input |
| S006 | ho_co_dam | Ho có đàm | Input |
| S007 | kho_tho | Khó thở | Input |
| S008 | dau_nguc | Đau ngực | Input |
| S009 | mat_vi_giac | Mất vị giác | Input |
| S010 | mat_khu_giac | Mất khứu giác | Input |
| ... | ... | ... | ... |

### 🔬 Triangle Rules (Inference Lab)

**16 luật** trong `inference_lab/sample_data.py`:

| Rule | Premises | Conclusion |
|------|----------|------------|
| R1 | a, b | c (Pythagorean) |
| R2 | a, c | b |
| R3 | b, c | a |
| R4 | a, b | dien_tich |
| R5 | a, c | dien_tich |
| R6 | b, c | dien_tich |
| R7 | a, goc_A | b |
| R8 | b, goc_A | a |
| ... | ... | ... |

**Sample Facts**: `a=3`, `b=4`  
**Sample Goals**: `c`, `dien_tich`

---

## 🤖 Smart Diagnosis Algorithm

### Weighted Evidence Accumulation

Thuật toán chấm điểm thông minh dựa trên nhiều yếu tố:

```python
final_score = (
    base_score             # Tích lũy bằng chứng dương (0-70)
    + prior_bonus          # Xác suất tiền nghiệm (0-25)
    + combo_bonus          # Tổ hợp triệu chứng đặc trưng (0-25)
    + count_adjustment     # Điều chỉnh theo số triệu chứng (0-15)
    - negative_evidence    # Triệu chứng trái ngược (0-50)
    - severity_penalty     # Phạt bệnh nhẹ có triệu chứng nặng (0-35)
)
```

### Example Scoring

**Input**: `sot=38.5°C, ho=true, mat_vi_giac=true, mat_khu_giac=true, kho_tho=true`

**Output**:
```
COVID-19: 78.5% (High confidence)
  ✅ Matched: mat_vi_giac (0.95), mat_khu_giac (0.95), sot (0.85), ho (0.80), kho_tho (0.85)
  🎁 Combo bonus: +18 (mat_vi_giac + mat_khu_giac)
  📊 Prior bonus: +2.0 (8% prevalence)
  
Viêm phổi: 45.2% (Medium confidence)
  ✅ Matched: sot (0.80), ho (0.75), kho_tho (0.95)
  ⚠️ Missing: sot_cao (0.90), ho_co_dam (0.90), dau_nguc (0.85)
  
Cảm cúm: 32.1% (Low confidence)
  ✅ Matched: sot (0.75), ho (0.85)
  ➖ Negative: mat_vi_giac (-0.40), mat_khu_giac (-0.40)
```

---

## 🎓 Educational Use Cases

### Cho Giảng viên
- ✅ Dạy Forward/Backward Chaining với visualization
- ✅ Demo FPG/RPG graph generation
- ✅ Giải thích THOA (Stack vs Queue)
- ✅ So sánh Min/Max priority strategies
- ✅ Case study: Medical Expert System

### Cho Sinh viên
- ✅ Học cách build rule-based system
- ✅ Hiểu workflow của inference engine
- ✅ Practice với custom rules
- ✅ Phân tích knowledge base structure
- ✅ Nghiên cứu Smart Scoring Algorithm

### Đề tài mở rộng
- 🔬 Thêm các domains khác (automotive, finance...)
- 🧪 Implement Certainty Factor (CF)
- 📊 Thêm explanation module
- 🤖 Tích hợp Machine Learning
- 📱 Mobile-responsive UI

---

## 🐛 Troubleshooting

### Graphviz not found

**Error**: `graphviz.backend.ExecutableNotFound: failed to execute ['dot', '-V']`

**Solution**:
1. Cài Graphviz system package (xem Bước 4)
2. Restart terminal/IDE
3. Verify: `dot -V`
4. Nếu vẫn lỗi, add manually to PATH:
   - Windows: `C:\Program Files\Graphviz\bin`
   - macOS: `/usr/local/bin` (Homebrew)

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'inference_lab'`

**Solution**:
```bash
# Ensure you're in project root
cd intelligent-diagnosis-system

# Activate venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # macOS/Linux

# Re-install
pip install -r requirements.txt
```

### Medical KB not found

**Error**: `FileNotFoundError: Medical KB file not found`

**Solution**:
```bash
# Check if file exists
ls data/medical_kb.json

# If missing, regenerate
python data/generate_medical_kb.py
```

### Port 5000 already in use

**Error**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Or use different port
# Edit run.py: app.run(port=5001)
```

---

## 📚 References

### Inference Algorithms
- **Forward Chaining**: Russell & Norvig, "Artificial Intelligence: A Modern Approach", Chapter 9
- **Backward Chaining**: Nilsson, "Principles of Artificial Intelligence"
- **RETE Algorithm**: Forgy, Charles L. (1982)

### Medical Knowledge Engineering
- **Expert Systems in Medicine**: Shortliffe, "Computer-Based Medical Consultations: MYCIN"
- **Certainty Factor**: Buchanan & Shortliffe (1984)
- **Clinical Decision Support**: Berner, E. S. (2007)

### Graphviz Visualization
- **Graphviz Documentation**: https://graphviz.org/documentation/
- **NetworkX**: https://networkx.org/documentation/

---

## 📞 Contact & Support

### GitHub Repository
🔗 https://github.com/dungle03/HCSTT_InferenceLAB

### Issues & Bug Reports
📌 https://github.com/dungle03/HCSTT_InferenceLAB/issues

### Author
👨‍💻 **Dung Lee**
- GitHub: [@dungle03](https://github.com/dungle03)
- Project: Intelligent Diagnosis System
- Course: Hệ Cơ Sở Tri Thức (Knowledge-Based Systems)

---

## 📝 License

```
MIT License

Copyright (c) 2025 Dung Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🌟 Acknowledgments

- **Flask**: Micro web framework for Python
- **NetworkX**: Graph library for Python
- **Graphviz**: Graph visualization software
- **Tailwind CSS**: Utility-first CSS framework
- **VS Code**: Code editor
- **GitHub Copilot**: AI pair programmer

---

## 🎯 Project Status

- ✅ **Core Features**: Complete
- ✅ **Medical KB**: 109 rules, 20 diseases
- ✅ **Smart Scorer**: Implemented
- ✅ **UI/UX**: Responsive design
- ✅ **Documentation**: Comprehensive README
- 🚧 **Unit Tests**: In progress
- 🚧 **Deployment**: Future work

**Last Updated**: October 24, 2025  
**Version**: 1.0.0
