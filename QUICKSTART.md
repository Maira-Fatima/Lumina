# 🚀 Quick Start Guide

> Get Lumina up and running in just 2 minutes! 

**Navigation:** [Main README](README.md) | [Documentation Hub](docs/DOCUMENTATION_HUB.md) | [Project Status](PROJECT_STATUS.md)

---

## ⚡ Installation (2 minutes)

```bash
# 1. Navigate to project directory
cd "e:\University\4th Sem\AI\Project\Improve 2\lumina"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python -m streamlit run app.py
```

**That's it!** The app opens at `http://localhost:8505` 🎉

---

## 📖 Usage

### 💬 Basic Chat Mode (app.py)
```bash
python -m streamlit run app.py
```

**Features:**
- ✅ Ask questions about programming, AI, data structures, etc.
- ✅ Get instant AI-powered answers with spell correction
- ✅ View related topics and prerequisites
- ✅ Chat history saved automatically

### 🎯 Enhanced Mode (app_enhanced.py)
```bash
python -m streamlit run app_enhanced.py
```

**All basic features PLUS:**
- ✅ MCQ quiz system with 4 options
- Progress tracking
- Personalized recommendations

## Running Tests

```bash
# Run all integration tests
cd tests
python test_integration.py

# Run specific tests
python test_mcq.py
python test_quiz_and_recommendations.py
```

## Project Structure

```
lumina/
├── app.py              # Basic chat interface
├── app_enhanced.py     # Enhanced UI with quiz
├── core/               # NLP & query processing
├── ml_module/          # Machine learning models
├── expert_system/      # Rule-based reasoning
├── adaptive_learning/  # Personalization
├── docs/               # All documentation
├── tests/              # All test files
└── scripts/            # Utility scripts
```

## Documentation

📚 **All documentation is in the `docs/` folder**

Quick links:
- [Complete Documentation Index](docs/README.md)
- [Features Summary](docs/FEATURES_SUMMARY.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Testing Report](docs/TESTING_REPORT.md)

## Key Features

✅ **Intelligent Q&A** - Ask any question, get accurate answers  
✅ **Typo Correction** - Automatically fixes typos (90%+ accuracy)  
✅ **MCQ Quizzes** - Test your knowledge with adaptive difficulty  
✅ **Progress Tracking** - Monitor your learning progress  
✅ **Personalized Recommendations** - Get tailored learning paths  
✅ **7,350+ Knowledge Entries** - Comprehensive knowledge base  
✅ **94-97% ML Accuracy** - Advanced topic & difficulty classification  

## Troubleshooting

**NLTK Data Error?**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

**Import Errors?**
```bash
pip install -r requirements.txt
```

**Cache Issues?**
```bash
streamlit cache clear
```

## Support

- 📖 **[Documentation Hub](docs/DOCUMENTATION_HUB.md)** - Central documentation
- 🔧 **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - For developers
- 🧪 **[Testing Guide](tests/README.md)** - Run tests
- 📊 **[Project Status](PROJECT_STATUS.md)** - Current status

---

**Ready to learn? Start with `python -m streamlit run app.py`!** 🎓
