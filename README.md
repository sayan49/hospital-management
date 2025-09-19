# 🏥 Hospital Management (Charity Project)

A free web-based patient management system for doctors and nurses.

## 🚀 Tech Stack
- Backend: FastAPI + SQLite
- Frontend: React + Tailwind
- Hosting: Render (Backend), Netlify (Frontend)

## 🛠️ Local Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Access API: http://127.0.0.1:8000/docs

### Frontend
```bash
cd frontend
npm install
npm start
```

## 🌍 Deployment (Free)
1. Push this repo to GitHub.
2. Deploy `backend/` to Render.com → select "FastAPI".
3. Deploy `frontend/` to Netlify.com → link GitHub repo.
4. Update `frontend/src/config.js` with backend Render URL.

Done! 🎉
