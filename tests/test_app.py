"""UI tests using Streamlit's headless AppTest runner (no browser needed)."""

import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import database as db  # noqa: E402

APP = str(ROOT / "app.py")


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "ui_test.db")
    db.init_db()


def run_page(page):
    at = AppTest.from_file(APP).run()
    at.sidebar.radio[0].set_value(page).run()
    return at


def test_submit_feedback_success():
    at = run_page("Submit Feedback")
    at.text_input[0].input("Asha")
    at.text_input[1].input("Python")
    at.slider[0].set_value(5)
    at.text_area[0].input("Great course")
    at.button[0].click().run()
    assert not at.exception
    assert "saved successfully" in at.success[0].value
    assert db.get_all_feedback()[0]["student_name"] == "Asha"


def test_submit_feedback_validation_error():
    at = run_page("Submit Feedback")
    at.button[0].click().run()
    assert len(at.error) == 2  # name + course missing
    assert db.get_all_feedback() == []


@pytest.mark.parametrize("page", ["View Feedback Records", "Rating Summary",
                                  "Database Info"])
def test_pages_render_empty_and_populated(page):
    at = run_page(page)
    assert not at.exception
    db.add_feedback("Asha", "Python", 5)
    db.add_feedback("Ravi", "Java", 3)
    at = run_page(page)
    assert not at.exception


def test_summary_metrics_values():
    db.add_feedback("Asha", "Python", 5)
    db.add_feedback("Ravi", "Java", 3)
    at = run_page("Rating Summary")
    values = {m.label: m.value for m in at.metric}
    assert values["Average Rating (all courses)"] == "4.0 / 5"
    assert values["Highest Rated Course"] == "Python"
    assert values["Total Feedback Records"] == "2"
