# 🧠 Intelligent Diagnosis System

Hệ thống chẩn đoán thông minh kết hợp **Inference Lab** (suy diễn tiến/lùi) và **Medical Diagnosis** (chẩn đoán y tế thông minh).

## ✨ Tính năng

### 🔬 Inference Lab
- **Suy diễn tiến** (Forward Chaining) - Từ sự kiện đến kết luận
- **Suy diễn lùi** (Backward Chaining) - Từ mục tiêu về sự kiện  
- **Trực quan hóa FPG/RPG** - Đồ thị suy diễn đẹp mắt
- **Tam giác & Công thức** - Bài toán tam giác với knowledge base

### 🏥 Medical Diagnosis
- **Chẩn đoán bệnh** từ triệu chứng (100+ rules)
- **Điểm tin cậy thông minh** - Weighted evidence accumulation
- **Chẩn đoán phân biệt** - Top 2-3 bệnh có khả năng
- **UI hiện đại** - Tailwind CSS responsive

## 📁 Cấu trúc Project

```
intelligent-diagnosis-system/
├── inference_lab/          # Core inference engine
│   ├── forward.py          # Forward chaining algorithm
│   ├── backward.py         # Backward chaining algorithm
│   ├── graphs.py           # FPG/RPG graph generation
│   └── ...
├── medical_kb/             # Medical knowledge base
│   ├── loader.py           # Load medical_kb.json
│   └── form_generator.py  # Generate symptom forms
├── data/
│   └── medical_kb.json     # 100 medical diagnosis rules
├── web/                    # Web application
│   ├── __init__.py         # Flask app factory
│   ├── diagnosis_scorer.py # Smart diagnosis scorer
│   ├── routes/
│   │   ├── lab_routes.py   # Inference Lab routes
│   │   └── medical_routes.py # Medical diagnosis routes
│   ├── templates/
│   │   ├── home.html       # Landing page
│   │   ├── index.html      # Inference Lab UI
│   │   └── medical/        # Medical UI templates
│   └── static/
│       ├── app.js          # Inference Lab JS
│       └── medical/        # Medical assets
├── run.py                  # Main entry point
├── requirements.txt
└── README.md
```

## 🚀 Cài đặt & Chạy

### Bước 1: Clone repository

```bash
git clone <your-repo-url>
cd intelligent-diagnosis-system
```

### Bước 2: Tạo virtual environment

```bash
python -m venv .venv
```

**Windows:**
```powershell
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 4: Chạy ứng dụng

```bash
python run.py
```

Mở trình duyệt:
- **Home**: http://127.0.0.1:5000
- **Inference Lab**: http://127.0.0.1:5000/lab  
- **Medical Diagnosis**: http://127.0.0.1:5000/medical

## 🔧 Hoàn tất Tái cấu trúc

### ⚠️ CẦN LÀM:

1. **Sửa imports trong các file:**
   - `web/routes/lab_routes.py` 
   - `web/routes/medical_routes.py`
   - `web/__main__.py`

   **Thay đổi:**
   ```python
   # CŨ
   from inference_lab.web.diagnosis_scorer import ...
   from inference_lab import ...
   
   # MỚI  
   from web.diagnosis_scorer import ...
   from inference_lab import ...
   ```

2. **Test cả 2 chức năng:**
   ```bash
   python run.py
   ```
   - ✅ Inference Lab: Load dữ liệu tam giác, chạy suy diễn
   - ✅ Medical Diagnosis: Nhập triệu chứng, xem kết quả

3. **Commit vào git:**
   ```bash
   git init
   git add .
   git commit -m "feat: Complete project restructure with Inference Lab + Medical Diagnosis"
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

## 📊 Knowledge Base

### Medical KB
- **File**: `data/medical_kb.json`
- **Rules**: 100+ medical diagnosis rules
- **Diseases**: 10 bệnh phổ biến (cảm cúm, COVID-19, viêm phổi, ...)
- **Symptoms**: 30+ triệu chứng

### Inference Rules
- **Tam giác**: 20+ rules về cạnh, góc, diện tích
- **Custom**: Tự tạo rules trong Inference Lab UI

## 🛠 Development

### Thêm bệnh mới

Edit `data/medical_kb.json`:

```json
{
  "diseases": {
    "benh_moi": {
      "label": "Tên bệnh mới",
      "severity": "Moderate",
      "conditions": ["trieu_chung_1", "trieu_chung_2"],
      "recommendations": ["Khuyến nghị điều trị..."]
    }
  }
}
```

### Thêm route mới

Tạo file trong `web/routes/` và register trong `web/__init__.py`.

## 📝 License

MIT License - Feel free to use for learning and research.

## 👨‍💻 Author

Developed with ❤️ for AI & Knowledge-Based Systems course.

---

**🎯 Next Steps:**
1. Open new VS Code window: `code .`
2. Fix imports (see above)
3. Test: `python run.py`
4. Commit & Push to GitHub
