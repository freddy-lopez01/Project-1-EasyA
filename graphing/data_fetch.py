import sqlite3
import pandas as pd

# a dictionary containing user selection
user_selection = {
    "graph_type": "single_class", # options: single_class, single_dept, class_level_dept
    "class_details": {
        "class_name": "CS415", # relevant if graph type is single_class
        "department": "Computer Information Science", # relevant for single_dpt and class_level_dpt
        "class_level": "415" # relevant if graph type is class_level_dept
    },
    "instructor_type": "All Instructors", # other option: "Faculty"
    "grade_type": "Percent As", # other option: "Percents Ds/Fs"
    "class_count": True
}

def fetch_data(str: user_selection):
    graph_type = user_selection["graph_type"]
    class_details = user_selection["class_details"]
    instructor_type = user_selection["instructor_type"]
    grade_type = user_selection["grade_type"]
    class_count = user_selection["class_count"]

    print(f"Graph type: {graph_type}")
    print(f"Class details: {class_details}")
    print(f"Instructor type: {instructor_type}")
    print(f"Grade type: {grade_type}")
    print(f"Class count: {class_count}")

fetch_data(user_selection)


