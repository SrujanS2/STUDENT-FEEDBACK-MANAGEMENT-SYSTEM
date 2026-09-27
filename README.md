# Student Feedback Management System

A simple web application to collect and analyse student feedback on courses, built with **Python, Streamlit and SQLite**.

---

## Table of contents

1. [Features](#features)
2. [Tech stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Quick start (Windows, one click)](#quick-start-windows-one-click)
5. [Step-by-step setup and run](#step-by-step-setup-and-run)
6. [Using the application](#using-the-application)
7. [Sample data and resetting the database](#sample-data-and-resetting-the-database)
8. [Running the tests](#running-the-tests)
9. [Project structure](#project-structure)
10. [Database design](#database-design)
11. [Git workflow](#git-workflow)
12. [Troubleshooting](#troubleshooting)

---

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

- **Python** 3.10 or newer
- **Streamlit**: web UI
- **SQLite**: via Python's built-in `sqlite3` module (database file: `feedback.db`)
- **pandas**: tables and charts
- **pytest**: automated tests
- **Virtual environment** (`venv`) and **Git**

---

## Prerequisites

Install these once:

| Tool | Check it is installed | Download |
|------|-----------------------|----------|
| Python 3.10+ | `python --version` (Windows) / `python3 --version` (macOS/Linux) | https://www.python.org/downloads/ |
| Git | `git --version` | https://git-scm.com/downloads |

> **Windows:** while installing Python, tick **"Add python.exe to PATH"**.

No separate database installation is needed; SQLite ships with Python.

---

## Quick start (Windows, one click)

1. Open the project folder.
2. Double-click **`run_app.bat`**.

The script creates the virtual environment (first run only), installs the requirements, and starts the app. Your browser opens at **http://localhost:8501**. Keep the black console window open while using the app, and close it to stop the app.

---

## Step-by-step setup and run

### 1. Get the code

Clone the repository:

```bash
git clone https://github.com/SrujanS2/STUDENT-FEEDBACK-MANAGEMENT-SYSTEM.git
cd STUDENT-FEEDBACK-MANAGEMENT-SYSTEM
git checkout feature/category-summary
```

Or, if you already have the project folder, open a terminal inside it.

### 2. Create a virtual environment

| OS / shell | Command |
|------------|---------|
| Windows (Command Prompt / PowerShell) | `python -m venv venv` |
| macOS / Linux | `python3 -m venv venv` |

This only needs to be done once. The `venv/` folder is ignored by Git.

### 3. Activate the virtual environment

| OS / shell | Command |
|------------|---------|
| Windows – Command Prompt | `venv\Scripts\activate` |
| Windows – PowerShell | `venv\Scripts\Activate.ps1` |
| Windows – Git Bash | `source venv/Scripts/activate` |
| macOS / Linux | `source venv/bin/activate` |

When it is active, your prompt starts with `(venv)`. Activate it every time you open a new terminal.

### 4. Install the dependencies

```bash
pip install -r requirements.txt
```

This installs `streamlit`, `pandas` and `pytest`.

### 5. (Optional) Load sample data

```bash
python seed_data.py
```

This inserts 10 sample feedback records across 4 courses, so the summary pages have data to show.

### 6. Run the application

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser if it does not open automatically.

- **Stop the app:** press `Ctrl + C` in the terminal.
- **Use a different port:** `streamlit run app.py --server.port 8502`
- **Leave the virtual environment:** `deactivate`

### Summary: all commands (Windows Command Prompt)

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py
streamlit run app.py
```

### Summary: all commands (macOS / Linux)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed_data.py
streamlit run app.py
```

---

## Using the application

Use the sidebar on the left to switch between pages.

1. **Submit Feedback**: enter Student Name and Course Name (both required), choose a Rating from 1 to 5 with the slider, add optional Comments, and click **Submit Feedback**. A green message confirms the record was saved with its feedback ID. Missing fields show a red error.
2. **View Feedback Records**: shows all feedback, newest first. Filter by one or more courses, or search by student name.
3. **Rating Summary**: shows the overall average rating, the highest-rated course (with its average and number of responses), the total record count, and a rating-distribution chart.
4. **Course-wise Summary**: shows each course's total feedback, average, lowest and highest rating, plus a bar chart. Click **Download summary as CSV** to export it.
5. **Database Info**: confirms `feedback.db` is connected and shows the `feedback` table columns, the `CREATE TABLE` SQL and the row count.

---

## Sample data and resetting the database

- `feedback.db` is created automatically in the project folder the first time the app starts.
- The committed `feedback.db` already contains the sample data used for the screenshots.
- **Start with an empty database:** stop the app, delete `feedback.db`, then run `streamlit run app.py` again.
- **Add the sample data again:** `python seed_data.py`. Each run adds 10 more rows.
- **Inspect the database directly (optional):** open `feedback.db` in [DB Browser for SQLite](https://sqlitebrowser.org/), or run:

  ```bash
  python -c "import sqlite3; print(sqlite3.connect('feedback.db').execute('SELECT * FROM feedback').fetchall())"
  ```

---

## Running the tests

With the virtual environment active, run this from the project folder:

```bash
python -m pytest -v
```

Expected result: **27 passed**. The tests use temporary databases, so your `feedback.db` is never modified.

| File | What it covers |
|------|----------------|
| `tests/test_database.py` | Table creation and columns, inserts, validation (empty fields, rating 0 / 6 / 3.5), SQL-injection safety, average rating, highest-rated course and tie-break, course-wise summary, empty-database cases |
| `tests/test_app.py` | Headless Streamlit UI tests: successful submit, empty-form errors, every page renders with and without data, summary metric values |

---

## Project structure

```
├── app.py                  # Streamlit UI (5 pages)
├── database.py             # All SQLite access: create table, insert, queries
├── seed_data.py            # Optional: loads 10 sample feedback records
├── feedback.db             # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
├── run_app.bat             # Windows one-click setup + run
├── .streamlit/config.toml  # Light theme and server settings
├── .gitignore              # Excludes venv, caches
├── tests/
│   ├── test_database.py    # Unit tests for every feature + validation
│   └── test_app.py         # Headless Streamlit UI tests (AppTest)
├── screenshots/            # Evidence screenshots
├── README.md               # This file
├── files.md                # Description of every project file
├── PROMPTS.md              # All AI prompts used during development
└── PROJECT_REPORT.md       # Assessment project report
```

---

## Database design

Database **`feedback.db`**, table **`feedback`**:

| Column | Type | Constraints |
|--------|------|-------------|
| feedback_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| student_name | TEXT | NOT NULL |
| course_name | TEXT | NOT NULL |
| rating | INTEGER | NOT NULL, CHECK (rating BETWEEN 1 AND 5) |
| comments | TEXT | optional |

```sql
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name  TEXT    NOT NULL,
    course_name   TEXT    NOT NULL,
    rating        INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comments      TEXT
);
```

---

## Git workflow

Repository: https://github.com/SrujanS2/STUDENT-FEEDBACK-MANAGEMENT-SYSTEM

| Branch | Contents |
|--------|----------|
| `main` | Core app: submit, view, average rating, highest-rated course |
| `feature/category-summary` | Course-wise rating summary, documentation and screenshots |

Commands used:

```bash
git init -b main
git config user.name "Srujankumar M Singannavar"
git config user.email "singannavarsrujan@gmail.com"
git add .
git commit -m "feat: student feedback app with submit, view, average and top-rated course"
git checkout -b feature/category-summary
git add app.py tests/test_app.py
git commit -m "feat(summary): add course-wise rating summary page"
git add PROMPTS.md PROJECT_REPORT.md screenshots
git commit -m "docs: add project report, prompt log and evidence screenshots"
git remote add origin https://github.com/SrujanS2/STUDENT-FEEDBACK-MANAGEMENT-SYSTEM.git
git push -u origin feature/category-summary
git push -u origin main
```

Useful checks: `git branch -a`, `git log --oneline --graph --all`, `git status`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `'python' is not recognized` | Reinstall Python with **Add to PATH** ticked, or use `py` instead of `python` (Windows). |
| PowerShell: *"running scripts is disabled on this system"* when activating | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt with `venv\Scripts\activate`. |
| `'streamlit' is not recognized` / `No module named streamlit` | The virtual environment is not active. Activate it (step 3) and run `pip install -r requirements.txt`. |
| `Port 8501 is already in use` | Stop the other Streamlit window, or run `streamlit run app.py --server.port 8502`. |
| Streamlit asks for an email on first run | Press Enter to skip. |
| Summary pages say "No feedback yet" | Submit some feedback or run `python seed_data.py`. |
| `database is locked` | Close any other program that has `feedback.db` open (e.g. DB Browser), then retry. |
| Git: *"detected dubious ownership"* | `git config --global --add safe.directory "*"` |
| `git push` rejected after history was rewritten | `git push --force-with-lease origin feature/category-summary` |
