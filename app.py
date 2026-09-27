"""Student Feedback Management System - Streamlit UI.

Run with:  streamlit run app.py
"""

import pandas as pd
import streamlit as st

import database as db

st.set_page_config(page_title="Student Feedback Management System",
                   page_icon="📝", layout="wide")

db.init_db()

PAGES = [
    "Submit Feedback",
    "View Feedback Records",
    "Rating Summary",
    "Course-wise Summary",
    "Database Info",
]

st.sidebar.title("📝 Student Feedback")
st.sidebar.caption("Management System")
page = st.sidebar.radio("Navigate", PAGES)
st.sidebar.divider()
st.sidebar.caption(f"Database: `{db.DB_PATH.name}`")

st.title("Student Feedback Management System")


# ---------------------------------------------------------------- Feature 1
def submit_page():
    st.header("Submit Feedback")
    with st.form("feedback_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        student_name = col1.text_input("Student Name *")
        course_name = col2.text_input("Course Name *")
        rating = st.slider("Rating *", min_value=db.MIN_RATING,
                           max_value=db.MAX_RATING, value=4,
                           help="1 = Poor, 5 = Excellent")
        comments = st.text_area("Comments", placeholder="Optional")
        submitted = st.form_submit_button("Submit Feedback", type="primary")

    if submitted:
        errors = db.validate_feedback(student_name, course_name, rating)
        if errors:
            for e in errors:
                st.error(e)
        else:
            new_id = db.add_feedback(student_name, course_name, rating, comments)
            st.success(f"Feedback #{new_id} from **{student_name.strip()}** for "
                       f"**{course_name.strip()}** saved successfully "
                       f"({'★' * rating}{'☆' * (db.MAX_RATING - rating)}).")


# ---------------------------------------------------------------- Feature 2
def view_page():
    st.header("View Feedback Records")
    records = db.get_all_feedback()
    if not records:
        st.info("No feedback yet. Submit some from the **Submit Feedback** page.")
        return

    df = pd.DataFrame(records)
    col1, col2 = st.columns(2)
    courses = sorted(df["course_name"].unique())
    course_filter = col1.multiselect("Filter by course", courses)
    search = col2.text_input("Search student name")
    if course_filter:
        df = df[df["course_name"].isin(course_filter)]
    if search:
        df = df[df["student_name"].str.contains(search, case=False, na=False)]

    st.caption(f"Showing {len(df)} of {len(records)} records")
    st.dataframe(
        df.rename(columns={"feedback_id": "ID", "student_name": "Student Name",
                           "course_name": "Course Name", "rating": "Rating",
                           "comments": "Comments"}),
        use_container_width=True, hide_index=True,
    )


# ------------------------------------------------------- Features 3 and 4
def summary_page():
    st.header("Rating Summary")
    avg = db.get_average_rating()
    if avg is None:
        st.info("No feedback yet - summary will appear once records exist.")
        return
    top = db.get_highest_rated_course()
    total = len(db.get_all_feedback())

    c1, c2, c3 = st.columns(3)
    c1.metric("Average Rating (all courses)", f"{avg} / {db.MAX_RATING}")
    c2.metric("Highest Rated Course", top["course_name"])
    c2.caption(f"⭐ {top['avg_rating']} average from {top['total_feedback']} response(s)")
    c3.metric("Total Feedback Records", total)

    st.subheader("Rating Distribution")
    dist = db.get_rating_distribution()
    dist_df = pd.DataFrame({"Rating": list(dist.keys()),
                            "Responses": list(dist.values())})
    st.bar_chart(dist_df, x="Rating", y="Responses", color="#2563eb",
                 x_label="Rating (1-5)", y_label="Number of responses")


# ---------------------------------------------------------------- Feature 5
def course_summary_page():
    st.header("Course-wise Rating Summary")
    summary = db.get_course_summary()
    if not summary:
        st.info("No feedback yet - course summary will appear once records exist.")
        return
    df = pd.DataFrame(summary).rename(columns={
        "course_name": "Course Name", "total_feedback": "Total Feedback",
        "avg_rating": "Average Rating", "min_rating": "Lowest Rating",
        "max_rating": "Highest Rating"})
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Average Rating by Course")
    st.bar_chart(df, x="Course Name", y="Average Rating", color="#16a34a",
                 horizontal=True, x_label="Average rating (out of 5)", y_label="")

    st.download_button("Download summary as CSV", df.to_csv(index=False),
                       file_name="course_summary.csv", mime="text/csv")


# ------------------------------------------------------------ DB evidence
def database_page():
    st.header("Database Info")
    st.success(f"SQLite database **{db.DB_PATH.name}** is connected and table "
               f"**feedback** exists.")
    st.subheader("Table: feedback")
    st.dataframe(pd.DataFrame(db.get_table_schema()), use_container_width=True,
                 hide_index=True)
    st.code(db.CREATE_TABLE_SQL.strip(), language="sql")
    st.metric("Rows in feedback table", len(db.get_all_feedback()))


{
    "Submit Feedback": submit_page,
    "View Feedback Records": view_page,
    "Rating Summary": summary_page,
    "Course-wise Summary": course_summary_page,
    "Database Info": database_page,
}[page]()
