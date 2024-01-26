import sqlite3
import pandas as pd
import logging
import inspect
import re

# setting up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

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
        if self.connection:
            self.connection.close()

    def fetch_data(self) -> pd.DataFrame:
        """
        Fetches data from the database based on the user's selection.
        """
        try:
            # connect to SQL database and get graph_type
            self.connect_to_database()
            query = "SELECT * FROM course_data"
            dataframe = pd.read_sql_query(query, self.connection)

            # store user selections
            single_class = self.user_selection.get("class_code", None)
            department_code = self.user_selection.get("class_code", None)
            department = None
            if department_code:
                match = re.match(r"([A-Za-z]+)", department_code)
                if match:
                    department = match.group(1)
            class_level = self.user_selection.get("class_level", None)
            instructor_type = self.user_selection.get("instructor_type", "All Instructors")
            grade_type = self.user_selection.get("grade_type", "Percent As")
            show_class_count = self.user_selection.get("class_count", False)

            logging.info(f"Single class: {single_class}")
            logging.info(f"Department: {department}")
            logging.info(f"Class level department: {class_level}")
            logging.info(f"instructor type: {instructor_type}")
            logging.info(f"grade type: {grade_type}")
            logging.info(f"show_class_count: {show_class_count}")

            # main logic for processing user selection
            if single_class is None:
                filtered_single_class = self.filter_single_class(single_class, dataframe)
                if instructor_type == "Regular Faculty":
                    # filter regular faculty
                    pass
                else:
                    # filter all instructors
                    all_instructors = self.get_instructor(single_class, dataframe)
                if grade_type == "Percent Ds/Fs":
                    # calculate Ds/Fs
                    percent_DF = self.calc_percent_DF(filtered_single_class)
                    logging.info(f"The percentage of 'D/F' grades for {single_class} is: {percent_DF}%")
                elif grade_type == "Percent As":
                    # calculate As
                    percent_As = self.calc_percent_a(filtered_single_class)
                    logging.info(f"The percentage of 'A' grades for {single_class} is: {percent_As}%")
                    logging.info(f"Percent A: {percent_As}")

                    #if show_class_count:
                    #class_count = self.class_count(dataframe)
                    #inn = self.get_instructor_class(dataframe)
            elif department:
                filtered_department = self.filter_single_dept(department, dataframe)
                if instructor_type == "Regular Faculty":
                    pass
                elif instructor_type == "All Instructors":
                    # filter all instructors
                    all_instructors = self.get_instructor(department, dataframe)
                    #logging.info(f"All instructors: {all_instructors}")
                if grade_type == "Percent Ds/Fs":
                    percent_DF = self.calc_percent_DF(filtered_department)
                elif grade_type == "Percent As":
                    percent_DF = self.calc_percent_a(filtered_department)

        except sqlite3.Error as e:
            logging.error(e)
            return pd.DataFrame()
        finally:
            if self.connection:
                self.close_connection()

    def get_instructor(self, group_code: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters list for instructors
        """
        try:
            # Filter the DataFrame for the given class code and get unique instructors
            instructors = dataframe[dataframe["group_code"] == group_code]["instructor"].unique()
            instructors_df = pd.DataFrame(instructors, columns=['instructor'])
            logging.info(f"Instructors extracted: {instructors_df}")
            return instructors_df

        except sqlite3.Error as e:
            logging.error(e)
            return pd.DataFrame()
        finally:
            self.close_connection()

    def filter_single_class(self, group_code: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame for rows matching a single class code.
        """
        try:
            logging.info(f"Filtering DataFrame for single class: {group_code}")
            filtered_class = dataframe.loc[dataframe["group_code"] == group_code]
            logging.info(f"--- Filtered single_class--- \n {filtered_class}")
            return filtered_class

        except Exception as e:
            logging.error(e)
            # return empty DataFrame if there's an error
            return pd.DataFrame()

    def filter_single_dept(self, department: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame for rows matching a single department.
        """
        logging.info("Filtering DataFrame for single department")
        try:
            filtered_department = dataframe.loc[dataframe["group_code"].str.contains(department, case=False, na=False)]
            logging.info(f"---Filtered department---\n {filtered_department}")
            return filtered_department

        except Exception as e:
            logging.error(e)
            return pd.DataFrame()

    def filter_class_level_dept(self, department: str, class_level: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame for rows matching a department and a specific class level (e.g., 400).
        """
        try:
            logging.info(f"Attempting to filter for {department} department, level {class_level} classes")
            # assuming the class level (e.g., '400') is at the end of the 'group_code' after department code
            pattern = f"[A-Za-z]+{class_level}\\b"  # \b is a word boundary in regex to ensure '400' is at the end
            print(f"Using pattern: {pattern}")
            # filter DataFrame based on the pattern
            filtered = dataframe[dataframe['group_code'].str.contains(pattern, regex=True, na=False)]
            return filtered

        except Exception as e:
            logging.error(f"An error occurred while filtering: {e}")
            return pd.DataFrame()

    def calc_percent_a(self, dataframe: pd.DataFrame) -> float:
        """
        Calculate percentages of As by class, department, or class of particular level within department.
        """
        try:
            total_grades = dataframe[['aprec', 'bprec', 'cprec', 'dprec', 'fprec']].sum().sum()
            if total_grades > 0:
                total_as = dataframe['aprec'].sum()
                percent_as = (total_as / total_grades) * 100
                logging.info(f"Percent As: {percent_as}%")
                return percent_as
            else:
                logging.info("No grades data found to calculate percentages")

        except Exception as e:
            logging.error(f"Error occurred during calculation: {e}")


    def calc_percent_DF(self, dataframe:pd.DataFrame) -> float:
        """
        Calculate percentages of As by class, department, or class of particular level within department.
        """
        try:
            total_grades = dataframe[["aprec", "bprec", "cprec", "dprec", "fprec"]].sum().sum()
            if total_grades > 0:
                total_DF = dataframe["dprec"].sum() + dataframe["fprec"].sum()
                percent_DF = (total_DF / total_grades) * 100
                logging.info(f"Percent Ds/Fs: {percent_DF}%")
                return percent_DF
            else:
                logging.info("No grades data found to calculate percentages")
        
        except Exception as e:
            logging.error(f"Error occurred during calculation: {e}")


    def get_instructor_class(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Fetches instructor's name with their corresponding classes.
        """
        try:
            # group instructor 
            instructor_classes = dataframe.groupby("instructor")["group_code"].apply(list).reset_index()  
        except sqlite3.Error as e:
            logging.error(e)
            return pd.DataFrame()
        finally:
            self.close_connection()

             
    def get_unique_department_codes(self) -> pd.DataFrame:
        """
        For debugging purposes
        """
        try:
            self.connect_to_database()
            query = "SELECT group_code FROM course_data"
            dataframe = pd.read_sql_query(query, self.connection)
            # extract only the alphabetical prefix from 'group_code' using regex
            dataframe['dept_code'] = dataframe['group_code'].str.extract(r'([A-Za-z]+)')
            unique_dept_codes = dataframe['dept_code'].unique()
            return pd.DataFrame(unique_dept_codes)

        except sqlite3.Error as e:
            logging.error(e)
        finally:
            self.close_connection()
        return pd.DataFrame()

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

    def class_count(self, dataframe: pd.DataFrame) -> int:
        """
        Add count of classes taught by each instructor into DataFrame if user selects this option.
        """
        try:
            # get instructor (column), and corresponding classes (row)
            instructor_class = dataframe[dataframe["instructor", ""]]
            logging.info(f"Instructor: {instructor_class}")
            # count number of unique classes the professor taught
            # return count

        except Exception as e:
            logging.error(f"Error occured in class_count(): {e}")
            



# a dictionary containing user selection
user_selection = {
    "graph_type": "department",  # options: single_class, single_dept, class_level_dept
    "class_code": "CIS420",  # relevant if graph type is single_class; specific class code (e.g., CS 422)
    "department": "Computer Information Science",  # relevant for single_dept and class_level_dept
    "class_level": "400",  # relevant if graph type is class_level_dept; specific class level (e.g., 100, 200)
    "instructor_type": "All Instructors",  # other option: "Faculty"
    "grade_type": "Percent As",  # other option: "Percent Ds/Fs"
    "class_count": True  # whether to show the number of classes taught by each instructor
}


if __name__ == "__main__":
    dest = "../Databases/GradeDatabase.sqlite"

    fetch = DataFetcher(user_selection, dest)
    dataframe = fetch.fetch_data()
    #unique_dept_codes = fetch.get_unique_department_codes()
    #print(unique_dept_codes)

    #s1 = pd.Series(['CIS330', 'AAOT', 'CIT330', 'CIS111'])
    #print(s1.str.contains("CIS330"))

