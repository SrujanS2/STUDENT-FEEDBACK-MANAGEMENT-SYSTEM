"""Data-access layer for the Student Feedback Management System.

All SQLite access lives here so the Streamlit UI (app.py) stays thin and
the logic can be unit-tested without a browser.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "feedback.db"

MIN_RATING = 1
MAX_RATING = 5

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name  TEXT    NOT NULL,
    course_name   TEXT    NOT NULL,
    rating        INTEGER NOT NULL CHECK (rating BETWEEN {MIN_RATING} AND {MAX_RATING}),
    comments      TEXT
);
"""


def get_connection(db_path=None):
    """Open a connection; rows behave like dicts (row['course_name'])."""
    conn = sqlite3.connect(str(db_path or DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    """Create feedback.db and the feedback table if they don't exist."""
    with get_connection(db_path) as conn:
        conn.execute(CREATE_TABLE_SQL)


def validate_feedback(student_name, course_name, rating):
    """Return a list of validation error messages (empty list = valid)."""
    errors = []
    if not student_name or not student_name.strip():
        errors.append("Student name is required.")
    if not course_name or not course_name.strip():
        errors.append("Course name is required.")
    if not isinstance(rating, int) or not MIN_RATING <= rating <= MAX_RATING:
        errors.append(f"Rating must be a whole number from {MIN_RATING} to {MAX_RATING}.")
    return errors


def add_feedback(student_name, course_name, rating, comments="", db_path=None):
    """Feature 1 - insert one feedback record and return its new feedback_id."""
    errors = validate_feedback(student_name, course_name, rating)
    if errors:
        raise ValueError(" ".join(errors))
    with get_connection(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO feedback (student_name, course_name, rating, comments) "
            "VALUES (?, ?, ?, ?)",
            (student_name.strip(), course_name.strip(), rating, (comments or "").strip()),
        )
        return cur.lastrowid


def get_all_feedback(db_path=None):
    """Feature 2 - every feedback record, newest first."""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT feedback_id, student_name, course_name, rating, comments "
            "FROM feedback ORDER BY feedback_id DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_average_rating(db_path=None):
    """Feature 3 - overall average rating (None when there is no feedback)."""
    with get_connection(db_path) as conn:
        avg = conn.execute("SELECT AVG(rating) FROM feedback").fetchone()[0]
    return round(avg, 2) if avg is not None else None


def get_highest_rated_course(db_path=None):
    """Feature 4 - course with the highest average rating.

    Ties are broken by number of responses (more feedback wins), then by
    course name alphabetically, so the result is deterministic.
    Returns a dict or None when there is no feedback.
    """
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT course_name, ROUND(AVG(rating), 2) AS avg_rating, "
            "COUNT(*) AS total_feedback "
            "FROM feedback GROUP BY course_name "
            "ORDER BY AVG(rating) DESC, COUNT(*) DESC, course_name ASC LIMIT 1"
        ).fetchone()
    return dict(row) if row else None


def get_course_summary(db_path=None):
    """Feature 5 - per-course count, average, min and max rating."""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT course_name, COUNT(*) AS total_feedback, "
            "ROUND(AVG(rating), 2) AS avg_rating, "
            "MIN(rating) AS min_rating, MAX(rating) AS max_rating "
            "FROM feedback GROUP BY course_name "
            "ORDER BY avg_rating DESC, course_name ASC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_rating_distribution(db_path=None):
    """How many feedback entries received each rating value (1..5)."""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT rating, COUNT(*) AS count FROM feedback GROUP BY rating"
        ).fetchall()
    counts = {r["rating"]: r["count"] for r in rows}
    return {r: counts.get(r, 0) for r in range(MIN_RATING, MAX_RATING + 1)}


def get_table_schema(db_path=None):
    """Column metadata for the feedback table (used on the Database page)."""
    with get_connection(db_path) as conn:
        rows = conn.execute("PRAGMA table_info(feedback)").fetchall()
    return [
        {"column": r["name"], "type": r["type"], "not_null": bool(r["notnull"]),
         "primary_key": bool(r["pk"])}
        for r in rows
    ]
