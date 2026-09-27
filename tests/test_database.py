"""Unit tests for database.py - each test uses a fresh temporary SQLite file."""

import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import database as db  # noqa: E402


@pytest.fixture
def tmp_db(tmp_path):
    path = tmp_path / "test_feedback.db"
    db.init_db(path)
    return path


@pytest.fixture
def seeded_db(tmp_db):
    for name, course, rating, comment in [
        ("Asha", "Python", 5, "Great"),
        ("Ravi", "Python", 4, "Good"),
        ("Meena", "Java", 3, "Okay"),
        ("John", "Java", 2, ""),
        ("Priya", "SQL", 5, "Loved it"),
    ]:
        db.add_feedback(name, course, rating, comment, db_path=tmp_db)
    return tmp_db


# ---- Database creation / table design
def test_database_and_table_created(tmp_db):
    assert tmp_db.exists()
    cols = [c["column"] for c in db.get_table_schema(tmp_db)]
    assert cols == ["feedback_id", "student_name", "course_name", "rating", "comments"]


def test_init_db_is_idempotent(tmp_db):
    db.init_db(tmp_db)  # second call must not fail or wipe data
    db.add_feedback("A", "B", 3, db_path=tmp_db)
    db.init_db(tmp_db)
    assert len(db.get_all_feedback(tmp_db)) == 1


def test_check_constraint_rejects_bad_rating_at_db_level(tmp_db):
    with sqlite3.connect(tmp_db) as conn, pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO feedback (student_name, course_name, rating) "
                     "VALUES ('x', 'y', 9)")


# ---- Feature 1: submit
def test_add_feedback_returns_id_and_trims(tmp_db):
    new_id = db.add_feedback("  Asha ", " Python ", 5, " nice ", db_path=tmp_db)
    rec = db.get_all_feedback(tmp_db)[0]
    assert new_id == rec["feedback_id"] == 1
    assert (rec["student_name"], rec["course_name"], rec["comments"]) == ("Asha", "Python", "nice")


@pytest.mark.parametrize("name,course,rating", [
    ("", "Python", 3), ("   ", "Python", 3), ("Asha", "", 3),
    ("Asha", "Python", 0), ("Asha", "Python", 6), ("Asha", "Python", 3.5),
])
def test_add_feedback_validation(tmp_db, name, course, rating):
    with pytest.raises(ValueError):
        db.add_feedback(name, course, rating, db_path=tmp_db)
    assert db.get_all_feedback(tmp_db) == []


def test_sql_injection_is_stored_as_text(tmp_db):
    evil = "x'); DROP TABLE feedback; --"
    db.add_feedback(evil, "Python", 3, db_path=tmp_db)
    assert db.get_all_feedback(tmp_db)[0]["student_name"] == evil


# ---- Feature 2: view
def test_get_all_feedback_newest_first(seeded_db):
    records = db.get_all_feedback(seeded_db)
    assert len(records) == 5
    assert [r["feedback_id"] for r in records] == [5, 4, 3, 2, 1]


# ---- Feature 3: average
def test_average_rating(seeded_db):
    assert db.get_average_rating(seeded_db) == 3.8  # (5+4+3+2+5)/5


def test_average_rating_empty(tmp_db):
    assert db.get_average_rating(tmp_db) is None


# ---- Feature 4: highest rated course
def test_highest_rated_course(seeded_db):
    top = db.get_highest_rated_course(seeded_db)
    assert top == {"course_name": "SQL", "avg_rating": 5.0, "total_feedback": 1}


def test_highest_rated_tie_prefers_more_responses(seeded_db):
    db.add_feedback("Kiran", "Python", 5, db_path=seeded_db)
    db.add_feedback("Sam", "Python", 5, db_path=seeded_db)
    db.add_feedback("Tara", "Python", 5, db_path=seeded_db)
    # Python avg = (5+4+5+5+5)/5 = 4.8 < SQL 5.0 -> SQL still wins
    assert db.get_highest_rated_course(seeded_db)["course_name"] == "SQL"
    db.add_feedback("Nina", "Cloud", 5, db_path=seeded_db)
    db.add_feedback("Omar", "Cloud", 5, db_path=seeded_db)
    # Cloud and SQL both 5.0; Cloud has 2 responses vs 1 -> Cloud wins
    assert db.get_highest_rated_course(seeded_db)["course_name"] == "Cloud"


def test_highest_rated_course_empty(tmp_db):
    assert db.get_highest_rated_course(tmp_db) is None


# ---- Feature 5: course-wise summary
def test_course_summary(seeded_db):
    summary = {s["course_name"]: s for s in db.get_course_summary(seeded_db)}
    assert set(summary) == {"Python", "Java", "SQL"}
    assert summary["Python"] == {"course_name": "Python", "total_feedback": 2,
                                 "avg_rating": 4.5, "min_rating": 4, "max_rating": 5}
    assert summary["Java"]["avg_rating"] == 2.5
    order = [s["course_name"] for s in db.get_course_summary(seeded_db)]
    assert order == ["SQL", "Python", "Java"]


def test_course_summary_empty(tmp_db):
    assert db.get_course_summary(tmp_db) == []


def test_rating_distribution(seeded_db):
    assert db.get_rating_distribution(seeded_db) == {1: 0, 2: 1, 3: 1, 4: 1, 5: 2}
