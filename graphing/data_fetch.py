import sqlite3
import pandas as pd
import logging
from typing import Union


# setting up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# a dictionary containing user selection
user_selection = {
    "graph_type": "single_class", # options: single_class, single_dept, class_level_dept
    "class_details": {
        "group_code": "CIS415", # relevant if graph type is single_class
        "department": "Computer Information Science", # relevant for single_dpt and class_level_dpt
        "class_level": "415" # relevant if graph type is class_level_dept
    },
"instructor_type": "All Instructors", # other option: "Faculty"
    "grade_type": "Percent As", # other option: "Percents Ds/Fs"
    "class_count": True
}


def fetch_data(user_selection: dict) -> Union[pd.DataFrame, str]:
    graph_type = user_selection["graph_type"]
    class_details = user_selection["class_details"]
    instructor_type = user_selection["instructor_type"]
    grade_type = user_selection["grade_type"]
    class_count = user_selection["class_count"]

    # error handling for unsuccessful connection
    try:
        # establish connectin to SQL database
        with sqlite3.connect("../Databases/GradeDatabase.sqlite") as connection:
            print("-----Connection to SQL database successful-----\n")
            cur = connection.cursor()
            group_code = user_selection["class_details"]["group_code"]
            dataframe = pd.read_sql_query("SELECT * from course_data", connection)
            # single class 
            if graph_type == "single_class":
                # call single_class_query
                single_class_query(group_code, dataframe)
            # single department
                # elif user selects "department"
                    # call department

            # class-level-department
                # elif user selects all class levels in that dept

            # close connection
            return dataframe

    except sqlite3.Error as e:
        logging.error(e)
        return f"An error occurred: {e}"


# functions for each graph type
def single_class_query(group_code: str, dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This function filters the DataFrame for rows where the class_code matches the provided class_code string.

    Parameters:
    - class_code (str): The code of class to filter by
    - dataframe (pd.DataFrame): The DataFrame to filter

    Returns:
    - pd.DataFrame: A Pandas DataFrame containing only the rows with the matching class_code.
    """
    
    try:
        # checking if class_code column exists
        # 
        if "group_code" not in dataframe.columns:
            raise ValueError("The class_code column doesn't exist in the DataFrame")
        logging.info(f"Filtering DataFrame for class code: {group_code}")

        # filter datafram to get rows with matching group_code
        filtered = dataframe.loc[dataframe["group_code"] == group_code]
        if filtered.empty:
            logging.warning(f"Class code: {group_code} not found")
        else:
            print("===== Filtered single class =====")
            print(filtered)
        return filtered

    except ValueError as e:
        logging.error(e)
        # return empty DataFrame if there's an error
        return pd.DataFrame()


def single_dept_query():
    pass


def class_level_dept_query():
    pass


fetch_data(user_selection)



