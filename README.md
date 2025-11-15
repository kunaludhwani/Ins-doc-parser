# 📘 Sacha Advisor

**AI-Powered Insurance Document Explainer**

Sacha Advisor transforms complex insurance documents into clear, human-friendly explanations using OpenAI's GPT-4o-mini model.

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 📤 **Easy Upload** - Drag-and-drop support for PDF, DOC, DOCX, JPG, PNG
- 🤖 **AI-Powered** - Uses OpenAI GPT-4o-mini for intelligent explanations
- 🎨 **Beautiful UI** - Red-themed interface with smooth animations
- ⚡ **Fast Processing** - Average response time under 6 seconds
- 🔐 **Privacy First** - No file storage, explanations only
- 🛡️ **Smart Validation** - Detects non-insurance documents automatically

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API key (get one [here](https://platform.openai.com/api-keys))

### Installation

**1. Backend Setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Create .env file and add your OpenAI API key
copy .env.example .env
```

**2. Frontend Setup**
```bash
cd frontend
npm install
```

### Running the App

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # On Windows
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser! 🎉

---

## 📚 Documentation

- **[Setup & Installation Guide](./SETUP.md)** - Detailed installation and configuration
- **[Product Requirements](./prd.md)** - Full product specification
- **[Backend README](./backend/README.md)** - Backend documentation
- **[Frontend README](./frontend/README.md)** - Frontend documentation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│      React Frontend (Vite)          │
│   - File Upload with Drag-Drop      │
│   - Animated Result Display         │
│   - Red Theme with Tailwind CSS     │
└──────────────┬──────────────────────┘
               │
               │ HTTP/POST
               │
┌──────────────▼──────────────────────┐
│      FastAPI Backend                │
│   ├─ File Validation (10MB, 10pg)  │
│   ├─ Text Extraction (PDF/DOC/OCR) │
│   ├─ Insurance Guardrail Check      │
│   ├─ OpenAI GPT-4o-mini Call       │
│   └─ SQLite Logging                 │
└──────────────┬──────────────────────┘
               │
               │ API
               │
┌──────────────▼──────────────────────┐
│      OpenAI GPT-4o-mini             │
│   - Intelligent explanation         │
│   - No financial advice             │
│   - Simple, friendly tone           │
└─────────────────────────────────────┘
```

---

## 📂 Project Structure

```
Sacha Advisor/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # Entry point
│   │   ├── config.py          # Settings
│   │   ├── routers/           # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Utilities
│   │   ├── db/                # Database
│   │   └── schemas/           # Data models
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.jsx            # Main app
│   │   └── index.css          # Global styles
│   ├── package.json
│   └── vite.config.js
│
├── prd.md                      # Product specification
├── SETUP.md                    # Detailed setup guide
└── README.md                   # This file
```

---

## 🔑 Key Technologies

**Backend:**
- FastAPI - Modern web framework
- PyPDF2 - PDF text extraction
- python-docx - Word document handling
- pytesseract - Image OCR
- SQLite - Lightweight database
- OpenAI API - AI explanations

**Frontend:**
- React 18 - UI framework
- Vite - Fast build tool
- Tailwind CSS - Styling
- Framer Motion - Animations

---

## 🎯 Supported File Formats

| Format | Size Limit | Pages Limit | Extraction Method |
|--------|-----------|-------------|-------------------|
| PDF | 10 MB | 10 | Text extraction |
| DOC | 10 MB | N/A | Word parser |
| DOCX | 10 MB | N/A | Word parser |
| JPG | 10 MB | N/A | OCR |
| PNG | 10 MB | N/A | OCR |

---

## 🛡️ Safety & Guardrails

### What Sacha Advisor DOES:
✅ Simplify insurance terminology  
✅ Highlight benefits and exclusions  
✅ Explain coverage and limitations  
✅ Use analogies for clarity  

### What Sacha Advisor DOES NOT:
❌ Recommend specific insurance products  
❌ Provide financial or legal advice  
❌ Calculate premiums  
❌ Store uploaded files  
❌ Process non-insurance documents  

---

## 📊 API Response Example

### Successful Upload:
```json
{
  "status": "success",
  "is_insurance": true,
  "summary": "📋 Summary\nThis is a comprehensive health insurance policy...\n\n✅ Key Benefits\n- Covers hospitalization...\n\n❌ Exclusions\n- Pre-existing conditions (waiting period)..."
}
```

### Failed Upload:
```json
{
  "status": "error",
  "message": "This doesn't look like an insurance policy. Sacha Advisor can only analyse insurance-related documents. Please upload a valid policy document."
}
```

---

## 🌟 UI Theme

- **Primary Color:** `#E63946` (Red)
- **Background:** Light gradient with white accents
- **Animations:** Smooth transitions with Framer Motion
- **Responsive:** Mobile-friendly design

---

## 📈 Performance Metrics

- **File Upload Success Rate:** 95%+
- **Insurance Detection Accuracy:** 85%+
- **Average Response Time:** 5-6 seconds
- **Database:** SQLite (no external dependencies)

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| API key error | Ensure `.env` file exists with valid `OPENAI_API_KEY` |
| CORS error | Backend must run on `http://localhost:8000` |
| OCR not working | Install Tesseract (see SETUP.md) |
| PDF extraction fails | Ensure PDF is text-based (not scanned image) |
| Frontend can't connect | Verify backend is running before starting frontend |

See [SETUP.md](./SETUP.md) for detailed troubleshooting.

---

## 🚀 Deployment

### Backend Deployment (Heroku/Railway/Render)
```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

### Frontend Deployment (Vercel/Netlify)
```bash
cd frontend
npm run build
# Deploy dist/ folder to Vercel/Netlify
```

---

## 🎓 Future Enhancements

- [ ] Multi-language summaries
- [ ] Side-by-side policy comparison
- [ ] Voice mode for explanations
- [ ] Chat-based follow-up questions
- [ ] Export explanation as PDF
- [ ] Browser extension version
- [ ] User authentication
- [ ] Personalized saved documents

---

## 📝 License

MIT License - Feel free to use for personal and commercial projects

---

## 🤝 Support & Contact

- **Issues:** Open an issue on GitHub
- **Questions:** Check the documentation
- **Feedback:** We'd love to hear from you!

---

## 👥 Credits

Built with ❤️ using FastAPI, React, and OpenAI

**Sacha Advisor v1.1** - Making insurance simple for everyone 📘✨
