"""Optional: load sample feedback so summaries have data to show.

Usage:  python seed_data.py
"""

import database as db

SAMPLE = [
    ("Asha Patil", "Python Programming", 5, "Very practical, loved the projects."),
    ("Ravi Kumar", "Python Programming", 4, "Good pace, more exercises please."),
    ("Meena Joshi", "Data Structures", 3, "Concepts were fine, examples were dry."),
    ("John D'Souza", "Data Structures", 4, "Trees and graphs explained well."),
    ("Priya Nair", "Database Systems", 5, "SQL labs were excellent."),
    ("Karan Shah", "Database Systems", 5, "Best course this semester."),
    ("Sneha Rao", "Web Development", 3, "Too much theory."),
    ("Vikram Desai", "Web Development", 2, "Labs were outdated."),
    ("Anjali Kulkarni", "Python Programming", 5, "Instructor was very helpful."),
    ("Rahul Hegde", "Data Structures", 4, ""),
]

if __name__ == "__main__":
    db.init_db()
    for row in SAMPLE:
        db.add_feedback(*row)
    print(f"Inserted {len(SAMPLE)} sample records into {db.DB_PATH.name}")
