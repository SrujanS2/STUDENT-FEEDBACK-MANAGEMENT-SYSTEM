# Student Feedback Management System

A simple web application to collect and analyse student feedback on courses, built with **Python, Streamlit and SQLite**.

## Features

| # | Feature | Where in the app |
|---|---------|------------------|
| 1 | Submit Feedback (student name, course name, rating 1–5, comments) with validation | **Submit Feedback** page |
| 2 | View Feedback Records, with course filter and student-name search | **View Feedback Records** page |
| 3 | Average Rating across all feedback | **Rating Summary** page |
| 4 | Highest Rated Course (highest average; ties → more responses, then A–Z) | **Rating Summary** page |
| 5 | Course-wise Rating Summary (count, avg, min, max, chart, CSV download) | **Course-wise Summary** page |
| – | Database Info: shows `feedback.db` is created and the table schema | **Database Info** page |

## Tech stack

- Python 3.10+
- Streamlit (UI)
- SQLite via Python's built-in `sqlite3` (database file: `feedback.db`)
- pandas (tables/charts), pytest (tests)
- Virtual environment (`venv`) and Git

## Project structure

```
├── app.py               # Streamlit UI (5 pages)
├── database.py          # All SQLite access: create table, insert, queries
├── seed_data.py         # Optional: loads 10 sample feedback records
├── requirements.txt
├── run_app.bat          # Windows one-click setup + run
├── .streamlit/config.toml  # Light theme
├── tests/
│   ├── test_database.py # Unit tests for every feature + validation
│   └── test_app.py      # Headless Streamlit UI tests (AppTest)
├── screenshots/         # Evidence screenshots
├── PROMPTS.md           # All AI prompts used during development
└── PROJECT_REPORT.md    # Assessment project report
```

## Database design

Database `feedback.db`, table `feedback`:

| Column | Type | Constraints |
|--------|------|-------------|
| feedback_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| student_name | TEXT | NOT NULL |
| course_name | TEXT | NOT NULL |
| rating | INTEGER | NOT NULL, CHECK (rating BETWEEN 1 AND 5) |
| comments | TEXT | optional |

The database and table are created automatically the first time the app starts. The committed `feedback.db` contains the sample data used for the screenshots.

## Setup and run

### Windows

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py        :: optional sample data
streamlit run app.py
```

Or just double-click `run_app.bat`.

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed_data.py        # optional sample data
streamlit run app.py
```

The app opens at http://localhost:8501.

## Running tests

```bash
python -m pytest -v
```

27 tests cover table creation, inserts, validation (empty fields, out-of-range ratings), SQL-injection safety, all five features, empty-database edge cases, and headless UI flows.

## Git workflow

```bash
git init
git add .
git commit -m "feat: student feedback app with submit, view, average and top course"
git checkout -b feature/category-summary
git add .
git commit -m "feat(summary): add course-wise rating summary page"
git remote add origin https://github.com/<your-user>/student-feedback-management-system.git
git push -u origin feature/category-summary
```
