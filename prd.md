# 📘 Product Requirements Document (PRD)
## **Product:** Sacha Advisor  
## **Version:** MVP v1.1  
## **Document Owner:** Kunal  
## **Last Updated:** 15 Nov 2025

---

# 1. Overview

**Sacha Advisor** is an AI-powered assistant designed to simplify complex insurance documents.  
Users upload a file (**PDF, JPG/PNG, DOC/DOCX**) and receive a **clear, simple explanation** of the contents — breaking down jargon and using analogies where needed.

### **USP**
Transforms technical insurance language into **human-friendly insights** perfect for first-time buyers.

---

# 2. Goals & Non-Goals

## **Goals**
- Use **OpenAI 4o-mini** for cheap, reliable inference.
- Enforce strict guardrails: only insurance-related uploads allowed.
- Keep UX smooth with animations and a red-themed interface.
- No user authentication.
- Log explanations (not the uploaded file).
- Enforce a strict **10-page limit**.

## **Non-Goals**
- No file storage.
- No financial advice or premium calculations.
- No insurance product recommendations.
- No user accounts or personalization in MVP.

---

# 3. Target Users

| User Type                | Need |
|--------------------------|------|
| Insurance buyers         | Understand policy terms easily |
| First-time buyers        | Clarification of insurance jargon |
| Agents                   | Simplified summaries |
| Comparison shoppers      | Quick clarity about policies |

---

# 4. User Flow

1. User lands on homepage (no login required).  
2. Uploads a file (PDF/JPG/DOC).  
3. System validates file type + 10-page limit.  
4. System checks if the document appears insurance-related.  
5. If valid → extract text → send to OpenAI 4o-mini.  
6. If invalid → return polite refusal.  
7. AI generates simplified breakdown.  
8. React UI displays animated output.  
9. Backend logs:
   - Timestamp  
   - File type  
   - Page count  
   - Output explanation  

---

# 5. Product Features

## 5.1 Core Features

### **A. File Upload**
- Accepts: PDF, DOC/DOCX, JPG, PNG  
- Max size: 10 MB  
- Max pages (PDF): **10 pages**  
- Red-themed animated upload  
- Clear error messages for limits

---

### **B. Insurance Guardrail**
Backend checks if document is insurance-related via:
- Keyword scan  
- Simple rule-based classifier  
- First 1000 characters check  

If not insurance:
> _“This doesn’t look like an insurance policy. Sacha Advisor can only analyse insurance-related documents. Please upload a valid policy document.”_

---

### **C. AI Explanation Engine (OpenAI 4o-mini)**

**LLM Prompt Requirements:**
- Explain in layman terms  
- Simplify technical insurance jargon  
- Use analogies  
- No financial recommendations  
- Highlight key benefits, exclusions, risks  
- Keep tone friendly and conversational

---

### **D. Animated UI Output**
- Loading animation (Lottie)  
- Typing effect for generated output  
- Sectioned results:
  - Summary  
  - Benefits  
  - Exclusions  
  - Risks  
  - Analogy  
  - 5-bullet breakdown  

---

## 5.2 Additional Features

### **Logging (No File Storage)**
Log:
- Explanation text  
- Timestamp  
- File type  
- Page count  
- Extracted text length  

No uploaded files or PII stored.

---

### **Red UI Theme**
- Primary: **#E63946**
- Secondary: **White + Black**
- Smooth, modern animations

---

# 6. Technical Architecture

## 6.1 High-Level Flow

React Frontend
|
|--> File Upload
|
FastAPI Backend
|
|--> Validate file
|--> Enforce 10-page limit
|--> Insurance guardrail
|--> Extract text
|--> Call OpenAI 4o-mini
|--> Log explanation
|
React Frontend
--> Display result with animation



---

# 7. Tech Stack

### **Frontend**
- React + Vite  
- TailwindCSS  
- Framer Motion  
- Lottie animations  

### **Backend**
- Python  
- FastAPI  
- PyPDF2 / pdfplumber  
- python-docx  
- Tesseract OCR  
- SQLite logger  
- OpenAI Python SDK  

### **Model**
- **OpenAI 4o-mini**  
User provides API key.

### **Database**
- **SQLite** (lightweight, local, no setup)
- Stores logs only (not files)

---

# 8. API Contracts

### **POST /upload**
**Request (multipart/form-data):**




### **Success Response**
```json
{
  "status": "success",
  "is_insurance": true,
  "summary": "<simplified explanation>"
}

{
  "status": "error",
  "message": "This is not an insurance-related document."
}

9. Safety & Guardrails
Document Guardrails

Reject:

ID proofs (Aadhaar/PAN/Passport)

Bank statements

Medical reports

Bills

Property agreements

Photos unrelated to insurance

Salary slips

Generic PDFs

Model Guardrails

Prompt explicitly forbids:

Financial recommendations

Premium calculations

Suggesting what policy to buy

Legal advice

Only explain what's written.

10. Success Metrics (MVP)

95% file upload success rate

85% insurance-document detection accuracy

Avg response time < 6 seconds

70%+ positive feedback

0 customer file retention

11. Future Enhancements

Multi-language summaries

Side-by-side insurance comparison

Voice mode

Chat-based follow-up questions

Export explanation as PDF

Browser extension version


backend/
│
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # API keys, env settings
│   ├── routers/
│   │     ├── upload.py         # File upload endpoint
│   │     └── health.py         # Health check endpoint
│   │
│   ├── services/
│   │     ├── file_validation.py   # File type + page limit checks
│   │     ├── insurance_check.py   # Insurance guardrail logic
│   │     ├── extractor.py         # PDF/Word/OCR extraction
│   │     ├── openai_client.py     # Calls OpenAI 4o-mini
│   │     └── logger_service.py    # SQLite logging
│   │
│   ├── utils/
│   │     ├── ocr.py               # Tesseract wrapper
│   │     ├── pdf_utils.py         # PDF helpers
│   │     └── doc_utils.py         # Word helpers
│   │
│   ├── db/
│   │     ├── database.py          # SQLite connection
│   │     └── models.py            # Log model
│   │
│   └── schemas/
│         ├── responses.py         # Response schemas
│         └── logs.py              # Log schemas
│
├── requirements.txt
└── README.md

