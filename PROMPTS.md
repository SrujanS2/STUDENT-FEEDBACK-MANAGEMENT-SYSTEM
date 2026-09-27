# Prompts Used During Development

Tool: Claude (AI-assisted development). Each prompt below corresponds to one stage of the expected workflow; the "Outcome" line records what the AI produced and what was changed as a result.

---

## Prompt 1 – Requirements Generation

> You are a senior software analyst. I am building a **Student Feedback Management System** as a simple web app using **Python, Streamlit and SQLite** (database `feedback.db`, table `feedback` with columns feedback_id, student_name, course_name, rating, comments).
> Required features: (1) Submit Feedback, (2) View Feedback Records, (3) Average Rating, (4) Highest Rated Course, (5) Course-wise Rating Summary.
> Produce: functional requirements for each feature, input validation rules, edge cases (empty database, ties, invalid rating), non-functional requirements (simplicity, runs locally in a virtual environment), and acceptance criteria I can test against.

**Outcome:** Requirements list with validation rules (name/course required, rating integer 1–5, comments optional), edge cases (no records → friendly message instead of crash; tie-break rule for highest-rated course), and acceptance criteria used later as test cases.

---

## Prompt 2 – Database Design

> Design the SQLite schema for `feedback.db` with a single table `feedback` using exactly these columns: feedback_id, student_name, course_name, rating, comments.
> Choose appropriate data types and constraints: auto-generated primary key, NOT NULL where required, and a CHECK constraint so rating can only be 1 to 5.
> Also give me the SQL queries for: insert a record (parameterised, to prevent SQL injection), list all records newest first, overall average rating, highest-rated course by average (deterministic tie-break), and a per-course summary with count, average, min and max rating.

**Outcome:** `CREATE TABLE IF NOT EXISTS feedback (...)` with `INTEGER PRIMARY KEY AUTOINCREMENT` and `CHECK (rating BETWEEN 1 AND 5)`; aggregate queries using `AVG`, `COUNT`, `MIN`, `MAX` and `GROUP BY course_name`. Tie-break: higher average → more responses → course name A–Z.

---

## Prompt 3 – Application Development (Code Generation)

> Generate a clean, modular Python project for the Student Feedback Management System:
> - `database.py`: all SQLite access (init_db, validate_feedback, add_feedback, get_all_feedback, get_average_rating, get_highest_rated_course, get_course_summary). Use parameterised queries, `sqlite3.Row`, and accept an optional `db_path` so functions are testable against a temporary database.
> - `app.py`: a Streamlit app with sidebar navigation and one page per feature — Submit Feedback (form with Student Name, Course Name, Rating slider 1–5, Comments; show success/error messages), View Feedback Records (table with course filter and name search), Rating Summary (average rating + highest-rated course as metrics + rating distribution chart), Course-wise Summary (table + bar chart + CSV download), and a Database Info page showing the table schema.
> - Handle the empty-database case on every page. Use a light theme. Add docstrings and keep the UI layer thin.
> - Also produce `requirements.txt` and a `.gitignore` that excludes venv and `__pycache__`.

**Outcome:** `database.py`, `app.py`, `requirements.txt`, `.gitignore`, `.streamlit/config.toml` (light theme).

---

## Prompt 4 – Testing

> Write pytest unit tests for `database.py` using a temporary database per test (tmp_path fixture). Cover: table creation and column names, idempotent init, DB-level CHECK constraint, insert + whitespace trimming, validation failures (empty/blank name, empty course, rating 0, 6 and 3.5), SQL-injection string stored as plain text, newest-first ordering, average rating, highest-rated course including tie-break, course summary values and order, rating distribution, and empty-database cases.
> Then write UI tests using `streamlit.testing.v1.AppTest` that submit the form successfully, submit it empty (expect 2 errors), render every page with and without data, and check the summary metric values.

**Outcome:** `tests/test_database.py` (20 tests) and `tests/test_app.py` (7 tests).

---

## Prompt 5 – Improvement: fix failing UI test

> One AppTest fails with `sqlite3.OperationalError: no such table: feedback` in `test_summary_metrics_values`. The test inserts rows before the app has run once. Fix it without changing application behaviour.

**Outcome:** The autouse fixture now calls `db.init_db()` after pointing `DB_PATH` at the temp file. All 27 tests pass.

---

## Prompt 6 – Improvement: UI polish after reviewing screenshots

> On the Rating Summary page the "Highest Rated Course" metric shows a green up-arrow delta, which wrongly suggests a trend. Replace it with a plain caption showing the average and response count. Make the rating distribution chart use numeric 1–5 on the x-axis with axis labels, and make the course-wise chart horizontal so long course names are readable.

**Outcome:** Metric delta replaced by caption; charts relabelled; course chart made horizontal; `streamlit>=1.40` pinned for the chart parameters used.

---

## Prompt 7 – Improvement: sample data and Windows convenience

> Add a `seed_data.py` script that inserts 10 realistic sample feedback rows across 4 courses, and a `run_app.bat` that creates the venv if missing, installs requirements and starts Streamlit.

**Outcome:** `seed_data.py`, `run_app.bat`.

---

## Prompt 8 – Documentation

> Write a README (features, tech stack, structure, schema, setup for Windows and macOS/Linux, how to run tests, Git workflow) and a project report with sections: Problem Statement, Features Implemented, Database Design, Screenshots, Prompts Used, Testing Performed, Learning Outcomes.

**Outcome:** `README.md`, `PROJECT_REPORT.md`.

---

## Prompt 9 – Git Operations

> Give me the Git commands to initialise the repository, make a first commit of the core app, create branch `feature/category-summary`, commit the course-wise summary work on that branch with a conventional commit message, add a GitHub remote and push the branch.

**Outcome:** Commands listed in README → "Git workflow" and executed; see screenshots 06 and 07.
