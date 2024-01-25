import sqlite3
from types import NoneType
import pandas as pd
import logging
from typing import Union

# setting up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataFetcher:
    def __init__(self, user_selection: dict, database_path: str):
        """
        Initializes the DataFetcher with user's selection and database path.

        Parameters:
        - user_selection (dict): The user's selection criteria.
        - database_path (str): The path to the SQLite database.
        """
        self.user_selection = user_selection
        self.database_path = database_path
        self.connection = None 
        self.cursor = None

    def connect_to_database(self) -> None:
        """
        Establishes a connection to the SQL database and logs success or error.
        """
        try:
            # establish connection to SQL database
            self.connection = sqlite3.connect(self.database_path)
            self.cursor = self.connection.cursor()
            logging.info("---Successfully connected to SQL database---")

        except sqlite3.Error as e:
            logging.error(f"---Error occured while connecting to database: {e}---")
            # ensures connection is closed
            if self.connection:
                self.connection.close()
                


    def close_connection(self) -> None:
        """
        Closes the SQL database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logging.info("---SQL database connection closed---")


    def fetch_data(self) -> Union[pd.DataFrame, str]:
        """
        Fetches data from the database based on the user's selection.
        """
        # make connection with DB 
        # get user input
        # if user input == single class
            # call filter_single_class
        # elif user_input == single_dept
            # call filter_single_dept
        # elif user_input == class_level_dept 
            # call filter_class_level_dept
        try:
            self.connect_to_database()
            graph_type = self.user_selection["graph_type"]
            print(f"---graph type: {graph_type}---")

        except sqlite3.Error as e:
            logging.error(e)
            return f"An error occurred: {e}"


    def filter_single_class(self, class_code: str) -> pd.DataFrame:
        """
        Filters the DataFrame for rows matching a single class code.
        """
        pass

    def filter_single_dept(self, department: str) -> pd.DataFrame:
        """
        Filters the DataFrame for rows matching a single department.
        """
        pass

    def filter_class_level_dept(self, department: str, class_level: str) -> pd.DataFrame:
        """
        Filters the DataFrame for rows matching a department and class level.
        """
        pass

    def calc_percent_a(self) -> pd.DataFrame:
        """
        Calculate percentages of As by class or department.
        """
        pass

    def compare_instructor_type(self) -> pd.DataFrame:
        """
        Split data into two DataFrames, one for "All Instructors" and one for "Regular Faculty", and calculate percentage of As for each.
        """
        pass

    def easy_As_vs_just_pass(self, grade_type: str) -> pd.DataFrame:
        """
        Calculates percentages for two different grade types, "Percent As" and "Percent Ds or Fs" based on user selection.
        """
        pass

    def class_count(self) -> pd.DataFrame:
        """
        Add count of classes taight by each instructor into DataFrame if user selects this option.
        """
        pass



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

def single_detpt_query():
    pass


def class_level_dept_query():
    pass

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

dest = "../Databases/GradeDatabase.sqlite"

fetch = DataFetcher(user_selection, dest)
dataframe = fetch.fetch_data()





