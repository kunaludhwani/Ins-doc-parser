# 🚀 Sacha Advisor - Getting Started Checklist

## Pre-Setup Requirements

- [ ] Python 3.9 or higher installed
- [ ] Node.js 16+ and npm installed
- [ ] OpenAI API key (from https://platform.openai.com/api-keys)
- [ ] Git installed (optional, for version control)

## Quick Setup (Windows)

1. [ ] **Run Setup Script**
   ```bash
   setup.bat
   ```
   This will automatically set up both backend and frontend

2. [ ] **Add OpenAI API Key**
   - Open `backend/.env`
   - Replace `your_openai_api_key_here` with your actual key
   - Save the file

3. [ ] **Start Backend** (Terminal 1)
   ```bash
   cd backend
   venv\Scripts\activate
   uvicorn app.main:app --reload
   ```
   ✅ Backend should be running on `http://localhost:8000`

4. [ ] **Start Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```
   ✅ Frontend should be running on `http://localhost:5173`

5. [ ] **Open in Browser**
   - Navigate to `http://localhost:5173`
   - You should see the Sacha Advisor interface

## Quick Setup (Mac/Linux)

1. [ ] **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. [ ] **Add OpenAI API Key**
   - Open `backend/.env`
   - Replace `your_openai_api_key_here` with your actual key

3. [ ] **Start Backend** (Terminal 1)
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

4. [ ] **Start Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

5. [ ] **Open in Browser**
   - Navigate to `http://localhost:5173`

## Docker Setup (Optional)

1. [ ] **Install Docker & Docker Compose**
   - Download from https://www.docker.com/products/docker-desktop

2. [ ] **Create `.env` file**
   ```bash
   cd backend
   cp .env.example .env
   # Add your OpenAI API key
   ```

3. [ ] **Run with Docker Compose**
   ```bash
   docker-compose up
   ```
   Both services will start automatically

4. [ ] **Access Applications**
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:5173`

## Testing the Application

1. [ ] **Test Health Check**
   ```bash
   curl http://localhost:8000/health
   ```

2. [ ] **Try a Sample Upload**
   - Go to `http://localhost:5173`
   - Drag and drop or click to select an insurance PDF
   - Wait for the AI explanation

3. [ ] **Check Database**
   - Find `sacha_advisor.db` in the `backend` folder
   - This SQLite database contains logs of all requests

## Troubleshooting Checklist

### Backend Won't Start

- [ ] Check Python version: `python --version` (need 3.9+)
- [ ] Verify virtual environment is activated
- [ ] Ensure all dependencies are installed: `pip install -r requirements.txt`
- [ ] Check for port conflicts: Is port 8000 already in use?
- [ ] Verify `.env` file exists with OPENAI_API_KEY

### Frontend Won't Start

- [ ] Check Node version: `node --version` (need 16+)
- [ ] Delete `node_modules` and reinstall: `npm install`
- [ ] Clear npm cache: `npm cache clean --force`
- [ ] Check for port conflicts: Is port 5173 already in use?

### API Connection Error

- [ ] Ensure backend is running on `http://localhost:8000`
- [ ] Check backend logs for errors
- [ ] Verify CORS settings in `backend/app/config.py`
- [ ] Try accessing `http://localhost:8000/health` in browser

### OpenAI API Error

- [ ] Verify API key is correct in `.env`
- [ ] Check API key is valid at https://platform.openai.com/api-keys
- [ ] Ensure you have API credits/billing set up
- [ ] Check for rate limiting

### File Upload Issues

- [ ] File must be under 10 MB
- [ ] PDFs must have 10 pages or fewer
- [ ] Supported formats: PDF, DOC, DOCX, JPG, PNG
- [ ] PDFs must be text-based (not scanned images)
- [ ] File must be a valid insurance document

### Image/OCR Issues

- [ ] Tesseract OCR must be installed
  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
  - Mac: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

## Project Structure Quick Reference

```
Sacha Advisor/
├── backend/                # Python FastAPI server
│   ├── app/               
│   │   ├── main.py        # Entry point
│   │   ├── routers/       # API routes
│   │   ├── services/      # Business logic
│   │   ├── utils/         # Utilities
│   │   ├── db/            # Database
│   │   └── schemas/       # Data models
│   ├── requirements.txt
│   ├── .env               # Environment variables (create this!)
│   └── .env.example       # Template
│
├── frontend/              # React + Vite app
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── README.md             # Main documentation
├── SETUP.md              # Detailed setup guide
├── prd.md                # Product requirements
├── setup.bat             # Windows setup script
├── setup.sh              # Mac/Linux setup script
└── docker-compose.yml    # Docker deployment
```

## Key Files to Modify

1. **`backend/.env`** - Add your OpenAI API key here
2. **`backend/app/config.py`** - Adjust settings (file size, page limits, etc.)
3. **`frontend/vite.config.js`** - Update API proxy if needed

## Documentation Files

- **README.md** - Overview and quick start
- **SETUP.md** - Detailed installation guide
- **backend/README.md** - Backend documentation
- **frontend/README.md** - Frontend documentation
- **prd.md** - Product requirements specification

## Development Tips

### Code Style

- Python: Follow PEP 8
- JavaScript/React: Use ES6+ with proper naming conventions
- Format code before committing

### Database

- SQLite database: `backend/sacha_advisor.db`
- Auto-created on first run
- Stores request logs only (no files)

### Environment Variables

Backend only reads from `.env` file:
```
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

### Hot Reload

- Backend: Automatically reloads with `--reload` flag
- Frontend: Hot module replacement (HMR) enabled in Vite

## Deployment Checklist

- [ ] Environment variables set correctly
- [ ] Database initialized and working
- [ ] All dependencies installed
- [ ] CORS settings updated for production domain
- [ ] Error logging configured
- [ ] Rate limiting implemented (optional)
- [ ] Security headers added
- [ ] SSL/HTTPS enabled (production)

## Performance Notes

- Average response time: 5-6 seconds
- File upload limit: 10 MB
- PDF page limit: 10 pages
- Insurance detection accuracy: ~85%

## Support & Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev/
- OpenAI API: https://platform.openai.com/docs/
- Tailwind CSS: https://tailwindcss.com/
- Vite: https://vitejs.dev/

## Next Steps

1. ✅ Complete setup above
2. 📝 Review the PRD (prd.md) to understand the product
3. 🧪 Test with sample insurance documents
4. 🚀 Deploy to your preferred platform
5. 📊 Monitor logs and user feedback

---

**Questions?** Check the SETUP.md file for detailed troubleshooting and additional information.

**Ready to go?** Start the services and enjoy Sacha Advisor! 🎉
