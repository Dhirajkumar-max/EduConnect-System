# EduConnect

EduConnect is an education community platform that connects students, teachers, and schools. Students discover courses and apply for admissions, teachers publish courses and apply to schools, and institutions manage their communities — with social features (feed, likes, comments, follows, messaging), real-time notifications over WebSocket, and role-based dashboards.

## Tech stack

- **Frontend:** React 19, Vite, custom CSS (light/dark theme)
- **Backend:** FastAPI (Python 3.12), Motor (async MongoDB driver)
- **Database:** MongoDB (local or MongoDB Atlas)
- **Auth:** JWT bearer tokens, bcrypt password hashing, role-based access (student / teacher / school)
- **Media:** Cloudinary for post image/video uploads
- **Real-time:** WebSockets for live messages and notifications

## Features

- JWT authentication with signup/login, banned-user enforcement, and role-based dashboards
- Social feed: create posts (with optional Cloudinary-hosted media), like, comment, save, share links
- Course library: create, browse, and enroll
- Learning notes: share and browse resource links
- People discovery: search users, follow/unfollow
- Direct messages with live delivery and notification badges
- Admissions workflow: student applications, teacher applications, school review (approve/reject)
- Admin controls: verify/ban members, notification center, online presence
- Responsive UI with day/night theme toggle

## Repository layout

```
frontend/   React + Vite application (deployed to GitHub Pages)
backend/    FastAPI application (deployed to Render)
render.yaml Render service definition
.github/    GitHub Actions workflow for Pages deployment
```

## Quick start

### Prerequisites

- Node.js 20.19+ or 22.12+
- Python 3.12+
- MongoDB running locally, or an Atlas connection string

### Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate            # Windows
pip install -r requirements.txt
copy .env.example .env             # fill in the values
uvicorn main:app --reload
```

The API serves at `http://127.0.0.1:8000` with interactive docs at `/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app serves at `http://localhost:5173` and talks to the backend configured via `VITE_API_URL`.

## Environment variables

Backend (`.env`, see `backend/.env.example`):

| Variable | Purpose |
| --- | --- |
| `MONGO_URL` | MongoDB connection URI |
| `DATABASE_NAME` | Database name |
| `JWT_SECRET_KEY` | Random secret, at least 32 characters |
| `CORS_ORIGINS` | Comma-separated allowed origins |
| `CLOUDINARY_CLOUD_NAME` / `CLOUDINARY_API_KEY` / `CLOUDINARY_API_SECRET` | Media uploads |

Frontend (`.env`, see `frontend/.env.example`):

| Variable | Purpose |
| --- | --- |
| `VITE_API_URL` | Backend base URL (no trailing slash) |

Never commit real credentials. The Cloudinary credentials that were previously hard-coded in `backend/app/utils/cloudinary_config.py` were leaked in Git history and must be rotated in the Cloudinary console.

## Deployment

The app deploys in two parts:

- **Frontend → GitHub Pages.** A workflow (`.github/workflows/deploy-pages.yml`) builds and deploys on every push to `main`. It reads the repository variable `VITE_API_URL` (set under **Settings → Secrets and variables → Actions → Variables**), which must be the HTTPS URL of the deployed backend.
- **Backend → Render.** `render.yaml` defines the service (`pip install -r requirements.txt`, then `uvicorn main:app`). Connect the repository in the Render dashboard, review the generated service, and set the secret environment variables (`MONGO_URL`, `CLOUDINARY_*`) in the dashboard.
- **Database → MongoDB Atlas.** Create a free cluster, get a connection string, and use it as `MONGO_URL` in Render.

After the backend is deployed, set `VITE_API_URL` to its URL and push (or re-run the workflow) so the frontend build points at it. GitHub Pages serves the site at `https://dhirajkumar-max.github.io/EduConnect-System/`.

## Security notes

- Tokens expire after 60 minutes; WebSocket connections require a valid token.
- Administrator accounts cannot be created through public signup; create the first admin directly in the database.
- Keep dependencies pinned and rotate any credential that has ever been committed.
