# SmartFood City

AI-powered surplus food management and redistribution platform.

## Phase 1
- FastAPI backend
- SQLite database
- SQLAlchemy ORM
- Donor, receiver, volunteer, and donation foundation
- Health check endpoint

## Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
