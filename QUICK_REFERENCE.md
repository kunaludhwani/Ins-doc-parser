# 🎯 Sacha Advisor - Quick Reference Card

## 📱 Startup Commands

### Windows
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

### Mac/Linux
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Docker
```bash
docker-compose up
```

---

## 🌐 Access Points

| Service | URL | Port |
|---------|-----|------|
| Frontend | http://localhost:5173 | 5173 |
| Backend API | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/docs | 8000 |
| Health Check | http://localhost:8000/health | 8000 |

---

## 🔑 API Quick Reference

### Health Check
```bash
curl http://localhost:8000/health
```

### Upload Document
```bash
curl -X POST -F "file=@policy.pdf" http://localhost:8000/api/upload
```

### Response Format
```json
{
  "status": "success",
  "is_insurance": true,
  "summary": "📋 Summary\n..."
}
```

---

## ⚙️ Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| .env | API keys & settings | `backend/.env` |
| config.py | App configuration | `backend/app/config.py` |
| vite.config.js | Frontend build config | `frontend/vite.config.js` |
| tailwind.config.js | CSS configuration | `frontend/tailwind.config.js` |

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| API key error | Add OPENAI_API_KEY to `backend/.env` |
| Port in use | Kill process on port 8000 or 5173 |
| CORS error | Backend must run before frontend |
| Module not found | Run `pip install -r requirements.txt` |
| npm errors | Delete `node_modules`, run `npm install` |

---

## 📦 File Upload Limits

| Limit | Value |
|-------|-------|
| Max File Size | 10 MB |
| Max PDF Pages | 10 pages |
| Supported Formats | PDF, DOC, DOCX, JPG, PNG |

---

## 🔍 Key Files to Know

**Backend**
- `backend/app/main.py` - FastAPI app entry point
- `backend/app/routers/upload.py` - Upload endpoint logic
- `backend/app/services/` - Business logic services
- `backend/app/config.py` - Configuration settings

**Frontend**
- `frontend/src/App.jsx` - Main React component
- `frontend/src/components/` - Reusable components
- `frontend/vite.config.js` - Build configuration
- `frontend/tailwind.config.js` - Styling config

---

## 📋 Environment Variables

**Required:**
```
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

**Optional (defaults in config.py):**
```
OPENAI_MODEL=gpt-4o-mini
MAX_FILE_SIZE_MB=10
MAX_PAGES=10
DATABASE_PATH=sacha_advisor.db
```

---

## 🎨 UI Color Reference

| Element | Color | Hex |
|---------|-------|-----|
| Primary | Red | #E63946 |
| Primary Dark | Dark Red | #D62828 |
| Light Background | Light Red | #F1FAEE |
| Text | Gray | #333333 |

---

## 📊 Database

**Location:** `backend/sacha_advisor.db`  
**Type:** SQLite  
**Tables:** `request_logs`

**Columns:**
- id (auto-increment)
- timestamp (DATETIME)
- file_type (TEXT)
- page_count (INTEGER)
- text_length (INTEGER)
- explanation (TEXT)

---

## 🚀 Deployment Checklist

- [ ] Add OPENAI_API_KEY to environment
- [ ] Run setup script: `setup.bat` (Windows) or `./setup.sh` (Mac/Linux)
- [ ] Verify backend: `http://localhost:8000/health`
- [ ] Verify frontend: `http://localhost:5173`
- [ ] Test with sample insurance PDF
- [ ] Check logs in `backend/sacha_advisor.db`

---

## 📚 Documentation Map

| Document | Purpose | Location |
|----------|---------|----------|
| README.md | Overview | Root |
| SETUP.md | Detailed setup | Root |
| GETTING_STARTED.md | Quick checklist | Root |
| BUILD_SUMMARY.md | What was built | Root |
| prd.md | Product spec | Root |
| backend/README.md | Backend docs | backend/ |
| frontend/README.md | Frontend docs | frontend/ |

---

## 🔗 Useful Links

- **OpenAI API Keys:** https://platform.openai.com/api-keys
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Tailwind CSS:** https://tailwindcss.com/
- **Vite:** https://vitejs.dev/

---

## 💾 Database Query Examples

```sql
-- All logs
SELECT * FROM request_logs;

-- Logs from today
SELECT * FROM request_logs WHERE DATE(timestamp) = DATE('now');

-- Insurance documents processed
SELECT file_type, COUNT(*) as count FROM request_logs GROUP BY file_type;

-- Latest explanation
SELECT timestamp, file_type, explanation FROM request_logs ORDER BY timestamp DESC LIMIT 1;
```

---

## 🧪 Testing Workflow

1. **Backend Health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Frontend Load:**
   - Open http://localhost:5173

3. **Upload Test:**
   - Drag PDF onto upload area
   - Wait 5-10 seconds for response

4. **Check Logs:**
   - Open `backend/sacha_advisor.db` in SQLite client

---

## 🛡️ Security Notes

✅ No file storage - only explanations logged  
✅ Insurance document validation built-in  
✅ API key stored locally in .env  
✅ CORS enabled for localhost  
✅ Input validation on all endpoints  

⚠️ In production:
- Update CORS_ORIGINS to your domain
- Use HTTPS
- Set DEBUG=False
- Use environment variable manager

---

## 🎓 Learning Resources

- **FastAPI Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **React Tutorial:** https://react.dev/learn
- **OpenAI API Guide:** https://platform.openai.com/docs/guides
- **Tailwind Tutorial:** https://tailwindcss.com/docs

---

**Version:** 1.1.0  
**Last Updated:** November 15, 2025  
**Status:** ✅ Production Ready
