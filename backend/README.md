# Sacha Advisor - Backend

AI-powered insurance document explainer backend built with FastAPI.

## Features

- 📄 Multi-format support: PDF, DOC/DOCX, JPG/PNG
- 🔒 10-page limit enforcement
- 🛡️ Insurance document validation
- 🤖 OpenAI GPT-4o-mini integration
- 📊 SQLite logging
- 🎯 Simple, focused API

## Prerequisites

- Python 3.9+
- Tesseract OCR (for image processing)
- OpenAI API key

### Installing Tesseract OCR

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location (usually `C:\Program Files\Tesseract-OCR`)
3. Add to PATH or set in code

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

## Setup

1. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create `.env` file in backend directory:**
```env
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /api/upload
Upload and analyze insurance document

**Request:**
- Form-data with `file` field
- Supported formats: PDF, DOC, DOCX, JPG, PNG
- Max size: 10 MB
- Max pages (PDF): 10

**Response:**
```json
{
  "status": "success",
  "is_insurance": true,
  "summary": "Detailed explanation..."
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Error description"
}
```

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "Sacha Advisor API"
}
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Configuration
│   ├── routers/
│   │   ├── upload.py        # Upload endpoint
│   │   └── health.py        # Health check
│   ├── services/
│   │   ├── file_validation.py
│   │   ├── insurance_check.py
│   │   ├── extractor.py
│   │   ├── openai_client.py
│   │   └── logger_service.py
│   ├── utils/
│   │   ├── ocr.py
│   │   ├── pdf_utils.py
│   │   └── doc_utils.py
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   └── schemas/
│       ├── responses.py
│       └── logs.py
├── requirements.txt
└── README.md
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| OPENAI_API_KEY | OpenAI API key | - |
| OPENAI_MODEL | Model to use | gpt-4o-mini |
| MAX_FILE_SIZE_MB | Max file size | 10 |
| MAX_PAGES | Max PDF pages | 10 |
| DATABASE_PATH | SQLite DB path | sacha_advisor.db |

## Testing

Test the API with curl:

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@path/to/insurance.pdf"
```

## License

MIT
