# Sacha Advisor - Setup & Installation Guide

## 📋 Project Overview

**Sacha Advisor** is an AI-powered assistant that simplifies complex insurance documents using OpenAI's GPT-4o-mini model.

### Tech Stack

**Backend:**
- FastAPI (Python)
- SQLite for logging
- PyPDF2, python-docx, Tesseract OCR for text extraction
- OpenAI API integration

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- Framer Motion (animations)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- Tesseract OCR (for image text extraction)

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

**Get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create a new secret key
3. Copy and paste it in `.env`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### 3. Run Backend

```bash
cd backend

# Activate virtual environment (if not already activated)
venv\Scripts\activate

# Start FastAPI server
uvicorn app.main:app --reload
```

The API will be running on `http://localhost:8000`

---

## 📦 Installation Details

### Backend Dependencies

**Core:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation

**File Handling:**
- `PyPDF2` - PDF extraction
- `python-docx` - Word document extraction
- `Pillow` - Image processing
- `pytesseract` - OCR for images

**AI & Logging:**
- `openai` - OpenAI API client
- `python-dotenv` - Environment variables

**Utilities:**
- `python-multipart` - Multipart form data

### Frontend Dependencies

**Core:**
- `react` - UI framework
- `react-dom` - React DOM rendering

**Styling & Animation:**
- `tailwindcss` - Utility-first CSS
- `framer-motion` - Animation library
- `autoprefixer` & `postcss` - CSS processing

**HTTP:**
- `axios` - HTTP client (optional, using fetch API instead)

---

## 📁 Project Structure

```
Sacha Advisor/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry
│   │   ├── config.py            # Configuration
│   │   ├── db/
│   │   │   ├── database.py      # SQLite setup
│   │   │   └── models.py        # Data models
│   │   ├── routers/
│   │   │   ├── upload.py        # Upload endpoint
│   │   │   └── health.py        # Health check
│   │   ├── services/
│   │   │   ├── file_validation.py
│   │   │   ├── insurance_check.py
│   │   │   ├── extractor.py
│   │   │   ├── openai_client.py
│   │   │   └── logger_service.py
│   │   ├── utils/
│   │   │   ├── ocr.py
│   │   │   ├── pdf_utils.py
│   │   │   └── doc_utils.py
│   │   └── schemas/
│   │       ├── responses.py
│   │       └── logs.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Header.jsx
    │   │   ├── FileUpload.jsx
    │   │   ├── LoadingSpinner.jsx
    │   │   ├── ResultDisplay.jsx
    │   │   └── ResultSection.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── vite.config.js
    ├── tailwind.config.js
    ├── package.json
    └── README.md
```

---

## 🔌 API Endpoints

### Health Check
**GET** `/health`
```json
{
  "status": "healthy",
  "service": "Sacha Advisor API"
}
```

### Upload Document
**POST** `/api/upload`

**Request:** multipart/form-data
- `file` (required) - PDF, DOC, DOCX, JPG, or PNG

**Response (Success):**
```json
{
  "status": "success",
  "is_insurance": true,
  "summary": "📋 Summary\n[Explanation...]"
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "This doesn't look like an insurance policy..."
}
```

---

## 🎨 UI Features

- **Red-themed interface** with primary color `#E63946`
- **Drag-and-drop** file upload
- **Loading animation** with spinner
- **Typing effect** for AI explanations
- **Responsive design** for mobile and desktop
- **Smooth animations** with Framer Motion

---

## 🔐 Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

Optional configurations in `app/config.py`:
- `OPENAI_MODEL` - Default: "gpt-4o-mini"
- `MAX_FILE_SIZE_MB` - Default: 10
- `MAX_PAGES` - Default: 10
- `DATABASE_PATH` - Default: "sacha_advisor.db"

---

## 📝 Testing

### Manual Testing

1. **Test Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test File Upload:**
   ```bash
   curl -X POST -F "file=@path/to/file.pdf" http://localhost:8000/api/upload
   ```

3. **Open Frontend:**
   Navigate to `http://localhost:5173` in browser

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors in Python
**Solution:** Ensure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: OpenAI API key error
**Solution:** Verify `.env` file exists and contains correct API key
```bash
type .env  # Windows
cat .env   # Mac/Linux
```

### Issue: CORS errors
**Solution:** Ensure backend is running on `http://localhost:8000` and frontend proxy is configured in `vite.config.js`

### Issue: OCR not working for images
**Solution:** Install Tesseract OCR
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Mac: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

### Issue: PDF extraction fails
**Solution:** Ensure PDFs are readable text-based PDFs (not scanned images)

---

## 🚢 Deployment

### Backend (Heroku/Railway)
```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT" > Procfile

# Push to deployment platform
```

### Frontend (Vercel/Netlify)
```bash
cd frontend
npm run build
# Deploy dist/ folder
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

---

## 📄 License

This project is open source and available for personal and commercial use.

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API logs
3. Verify environment configuration

**Enjoy using Sacha Advisor! 🎉**
