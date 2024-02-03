import sqlite3
import pandas as pd
import logging
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
        self.main_data = pd.DataFrame()
        self.class_count = pd.DataFrame()
        self.instructors = pd.DataFrame()
        self.class_data = pd.DataFrame()
        self.instructor_data = pd.DataFrame()
        self.percent_grade = pd.DataFrame()
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
            logger.info("---Successfully connected to SQL database---")
        except sqlite3.Error as e:
            logger.exception(f"---Error occured while connecting to database---")
            # ensures connection is closed
            if self.connection:
                self.connection.close()
                
    def close_connection(self) -> None:
        """
        Closes the SQL database connection.
        """
        if self.connection:
            self.connection.close()

    def fetch_data(self) -> None:
        """
        Fetches data from the database based on the user's selection.
        """
        try:
            # connect to SQL database and get graph_type
            self.connect_to_database()
            query = "SELECT * FROM FacultyByDepartment"
            dataframe = pd.read_sql_query(query, self.connection)
            valid_class_levels = ["100", "200", "300", "400", "500", "600"]


            # store user selections
            faculty = self.user_selection.get("instructor", None)
            logger.info(f"Faculty: {faculty}")
            subject = self.user_selection.get("Subject", None)
            logger.info(f"Subject: {subject}")
            graph_type = self.user_selection.get("graph_type", None)

            logger.info(f"graph_type: {graph_type}")
            single_class = self.user_selection.get("class_code", None)

            logger.info(f"single_class: {single_class}")
            department_code = self.user_selection.get("class_code", None)

            logger.info(f"department_code: {department_code}")
            # strip numbers from department_code
            department = None
            if department_code:
                match = re.match(r"([A-Za-z]+)", department_code)
                if match:
                    department = match.group(1)
            class_level = self.user_selection.get("class_level", None)
            instructor_type = self.user_selection.get("instructor", None)
            grade_type = self.user_selection.get("grade_type",  True)
            show_class_count = self.user_selection.get("class_count", False)

            # for debugging purposes
            """
            logging.info(f"Single class: {single_class}")
            logging.info(f"Department: {department}")
            logging.info(f"Class level department: {class_level}")
            logging.info(f"instructor type: {instructor_type}")
            logging.info(f"grade type: {grade_type}")
            logging.info(f"show_class_count: {show_class_count}")
            """

            # main logic for processing user selection
            if graph_type == "single_class" and single_class:
                filtered_single_class = self.filter_single_class(single_class, dataframe)
                if instructor_type == "Regular Faculty":
                    self.instructor_data = self.get_faculty(filtered_single_class)
                elif instructor_type == "All Instructors":
                    # filter all instructors
                    self.instructor_data = self.get_instructor_class(filtered_single_class)
                if grade_type == "Percent Ds/Fs":
                    # calculate Ds/Fs
                    self.percent_grade = self.calc_percent_DsFs_instructor(self.instructor_data)
                    logger.info(f"-----Filtered with Percent Grade Ds/Fs-----: \n{self.percent_grade}")
                elif grade_type == "Percent As":
                    # calculate As
                    self.percent_grade = self.calc_percent_a_instructor(self.instructor_data)
                    logger.info(f"-----Filtered with Percent As-----: \n{self.percent_grade}")
                # if toggle class count for single class graph
                if show_class_count:
                    """
                    This section takes the class count of each instructor and merges it 
                    with the DataFrame that contains Percent As given by each instructor 
                    """
                    # get class count (DataFrame)
                    self.class_count = self.instructor_class_count(filtered_single_class)
                    # update self.instructor_data DataFrame with percent_grade DataFrame
                    self.instructor_data = self.percent_grade
                    # merge class count DataFrame with self.instructor_data DataFrame
                    self.instructor_data = self.instructor_data.merge(self.class_count, on="instructor")
                    # strip last name
                    self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()
                    logger.info(f"MERGED \n {self.instructor_data}")
                else:
                    # strip last name
                    self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()

            # department only
            elif graph_type == "department" and department:
                filtered_department = self.filter_single_dept(department, dataframe)
                logger.info(f"FILTERED_DEPT \n{filtered_department}")
                if instructor_type == "Regular Faculty":
                    filtered_faculty = self.get_faculty(filtered_department)
                    self.instructor_data = self.get_instructor_class(filtered_faculty)
                elif instructor_type == "All Instructors":
                    self.instructor_data = self.get_instructor_class(filtered_department)
                if grade_type == "Percent Ds/Fs":
                    self.percent_grade = self.calc_percent_DsFs_class(self.instructor_data)
                    logger.info(f"PERCENT GRADE DsFs: \n{self.percent_grade}")
                elif grade_type == "Percent As":
                    self.percent_grade = self.calc_percent_a_class(self.instructor_data)
                    logger.info(f"PERCENT As: \n{self.percent_grade}")

                # if toggle class count for department graph
                if show_class_count:
                    # get class data and class count and merge the two DataFrames together
                    self.class_count = self.instructor_class_count(filtered_department)
                    self.instructor_data = self.instructor_data.merge(self.class_count, on="instructor")
                    self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()
                    logger.info(f"MERGED DATA: \n{self.instructor_data}")
                else:
                    self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()
                    
            # all classes of a particular level within department
            elif graph_type == "class_level_dept":
                filtered_department = self.filter_class_level_dept(subject, class_level, dataframe)

                if class_level and class_level in valid_class_levels:
                    # convert class_level to integer for comparison
                    class_level_int = int(class_level)
                    # filter based on the numeric part of group_code corresponding to the user's selection
                    filtered_department = filtered_department[
                        filtered_department["group_code"].str[3:].astype(int).between(class_level_int, class_level_int + 99)]
                    logger.info(f"Filtered class level {class_level} department: \n{filtered_department}")
                if instructor_type == "Regular Faculty":
                    self.instructor_data = self.get_faculty(filtered_department)
                elif instructor_type == "All Instructors":
                    self.instructor_data = self.get_instructor_class(filtered_department)
                if grade_type == "Percent Ds/Fs":
                    self.percent_grade = self.calc_percent_DsFs_instructor(self.instructor_data)
                elif grade_type == "Percent As":
                    self.percent_grade = self.calc_percent_a_class(self.instructor_data)
                    #self.percent_grade = self.calc_percent_a_instructor(self.instructor_data)
                    logger.info(f"PERCENT As \n{self.percent_grade}")

                if show_class_count:
                    self.class_count = self.instructor_class_count(filtered_department)
                    self.instructor_data = self.instructor_data.merge(self.class_count, on="instructor")
                    logger.info(f"Merged instructor class count to dataframe \n{self.instructor_data}")
                    self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()
                else:
                    self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()
                logger.debug("User selection: %s", self.user_selection)
        except Exception as e:
            logger.exception("Exception occurred during data fetch")
        finally:
            if self.connection:
                self.close_connection()

    def get_instructor(self, group_code: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters list for instructors
        """
        try:
            if dataframe.empty:
                logger.info("DataFrame is empty. No instructors to extract.")
                return pd.DataFrame()
            # Filter the DataFrame for the given class code and get unique instructors
            instructors = dataframe[dataframe["group_code"] == group_code]["instructor"].unique()
            instructors_df = pd.DataFrame(instructors, columns=["instructor"])
            logger.info(f"Instructors extracted: \n{instructors_df}")
            return instructors_df

        except Exception as e:
            logger.exception("Exception occurred during get_instructor")
            return pd.DataFrame()
        finally:
            self.close_connection()

    def filter_single_class(self, group_code: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame for rows matching a single class code.
        """

        try:
            logger.info(f"Filtering DataFrame for single class: {group_code}")
            filtered_class = dataframe.loc[dataframe["group_code"] == group_code]
            logger.info(f"--- Filtered single_class--- \n {filtered_class}")
            return filtered_class

        except Exception as e:
            logger.exception("Exception occurred while filtering single class")
            # return empty DataFrame if there's an error
            return pd.DataFrame()

    def filter_single_dept(self, department: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame for rows matching a single department.
        """
        logger.info(f"Filtering DataFrame for single department: \n {department}")
        try:
            logging.info(f"=====================================DATAFRAME==============================:\n {department}")
            filtered_department = dataframe.loc[dataframe["group_code"].str.contains(department, case=False, na=False)]
            #logging.info(f"---Filtered department---\n {filtered_department}")
            return filtered_department

        except Exception as e:
            logger.exception("Exception occurred while filtering single department")
            return pd.DataFrame()

    def filter_class_level_dept(self, department: str, class_level: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame for rows matching a department and a specific class level (e.g., 400).
        """
        # logger.info(f"Filtering DataFrame for single department: \n {department}")
        try:
            # logger.info(f"Filtering DataFrame for single department: \n {department}")
            logger.info(f"Attempting to filter for {department} department, level {class_level} classes")
            # assuming the class level (e.g., '400') is at the end of the 'group_code' after department code
            pattern = f"[A-Za-z]+{class_level}\\b"  # \b is a word boundary in regex to ensure '400' is at the end
            print(f"Using pattern: {pattern}")
            # filter DataFrame based on the pattern
            filtered = dataframe[dataframe["group_code"].str.contains(pattern, regex=True, na=False)]
            return filtered

        except Exception as e:
            logger.exception("Exception occurred during filtering class level dept")
            return pd.DataFrame()


    def calc_percent_a_class(self, class_grades: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates percentages of As given by each class
        """
        try:
            # get total grades and divide number of As given by total grades
            class_grades["total_grades"] = (
                class_grades["aprec"] +
                class_grades["bprec"] +
                class_grades["cprec"] +
                class_grades["dprec"] +
                class_grades["fprec"]
            )
            class_grades["Percent As"] = (
                (class_grades["aprec"] / class_grades["total_grades"]) * 100
            ).round()
            return class_grades

        except Exception as e:
            logger.exception("Exception occurred while calculating percent As for classes")
            return pd.DataFrame()


    def calc_percent_DsFs_class(self, class_grades: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates percentages of Ds/Fs given by each class
        """
        try:
            # get total grades and divide number of As given by total grades

            class_grades["total_grades"] = (
                class_grades["aprec"] +
                class_grades["bprec"] +
                class_grades["cprec"] +
                class_grades["dprec"] +
                class_grades["fprec"]
            )
            class_grades["Percent Ds/Fs"] = (
                ((class_grades["dprec"] + class_grades["fprec"]) / class_grades["total_grades"]) * 100
            ).round()
            return class_grades

        except Exception as e:
            logger.exception("Error occurred while calculating percent Ds/Fs for classes")
            return pd.DataFrame()


    def calc_percent_a_instructor(self, instructor_grades: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates Percentages of As given by each professor
        """
        try:
            instructor_grades = instructor_grades.copy()
            # sum total number of A grades given by each professor
            instructor_grades["total_grades"] = (
                instructor_grades["aprec"] +
                instructor_grades["bprec"] +
                instructor_grades["cprec"] +
                instructor_grades["dprec"] +
                instructor_grades["fprec"]
            )
            # calculate percent As given by professor
            instructor_grades["Percent As"] = (
                (instructor_grades["aprec"] / instructor_grades["total_grades"]) * 100
            ).round()
            return instructor_grades
        
        except Exception as e:
            logger.exception("Exception occurred while calculating percent As given by instructors")
            # if error occurs, just return empty dataframe
            return pd.DataFrame()

    def calc_percent_DsFs_instructor(self, instructor_grades: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates percentages of Ds/Fs given by each instructor
        """
        try:
            instructor_grades = instructor_grades.copy()
            # sum total number of grades given by professor
            instructor_grades["total_grades"] = (
                instructor_grades["aprec"] +
                instructor_grades["bprec"] +
                instructor_grades["cprec"] +
                instructor_grades["dprec"] +
                instructor_grades["fprec"]
            )
            # calculate percent Ds/Fs given by professor
            instructor_grades["Percent Ds/Fs"] = (
                ((instructor_grades["dprec"] + instructor_grades["fprec"]) / instructor_grades["total_grades"]) * 100
            ).round()
            return instructor_grades

        except Exception as e:
            logger.exception("Exception occurred while calculating percent Ds/Fs given by instructors")
            # if error occurs, return empty dataframe
            return pd.DataFrame()


    def get_class_data(self, dataframe: pd.DataFrame) -> pd.DataFrame | None:
        """
        Gathers data related to that specific class
        """
        try:
            class_data = dataframe.groupby("group_code").agg({
                "aprec": "sum",
                "bprec": "sum",
                "cprec": "sum",
                "dprec": "sum",
                "fprec": "sum"
            }).reset_index()
            logger.info(f"Class data: \n{class_data}")
            return class_data

        except Exception as e:
            logger.exception("Exception occurred while filtering class data")

    def get_instructor_class(self, dataframe: pd.DataFrame) -> pd.DataFrame | None:
        """
        Fetches instructor's name with their corresponding classes and data.
        """
        #dataframe = dataframe.copy()
        #dataframe["instructor"] = dataframe["instructor"].str.strip()
        try:
            # get info from specific instructor 
            instructor_data = dataframe.groupby("instructor").agg({
                "aprec": "sum",
                "bprec": "sum",
                "cprec": "sum",
                "dprec": "sum",
                "fprec": "sum"
            }).reset_index()
            logger.info(f"Instructor data: \n{instructor_data}")
            return instructor_data

        except Exception as e:
            logger.exception("Exception occurred during filtering instructor classes")
            return pd.DataFrame()
        finally:
            self.close_connection()

             
    def get_unique_department_codes(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        For debugging purposes
        """
        try:
            # extract only the alphabetical prefix from 'group_code' using regex
            dataframe['dept_code'] = dataframe['group_code'].str.extract(r'([A-Za-z]+)')
            unique_dept_codes = dataframe['dept_code'].unique()
            logger.info(f"Unique Department Codes: {unique_dept_codes}")
            return pd.DataFrame(unique_dept_codes)

        except Exception as e:
            logger.exception("Exception occurred while filtering unique department codes")
        finally:
            self.close_connection()
        return pd.DataFrame()


    def get_class_count(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates the number of recurring classes and stores them into a new DataFrame
        """
        try:
            class_count_series = dataframe.groupby("group_code").size()
            class_count_df = class_count_series.reset_index()
            class_count_df.columns = ["group_code", "class_count"]
            class_count_df = class_count_df.rename(columns={"index": "instructor"})
            return class_count_df

        except Exception as e:
            logger.exception("Exception occurred during filtering of class counts")
            return pd.DataFrame()


    def instructor_class_count(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Add count of classes taught by each instructor into DataFrame if user selects this option.
        """
        try:
            # get instructor column 
            class_count_series = dataframe.groupby("instructor").size()
            # convert Pandas series to DataFrame
            class_count_df = class_count_series.reset_index()
            class_count_df.columns = ["instructor", "class_count"] 
            class_count_df = class_count_df.rename(columns={"index": "instructor"})
            logger.info(f"Class count by instructor: \n{class_count_df}")
            return class_count_df

        except Exception as e:
            logger.exception("Error occurred while filtering instructor class count")
            return pd.DataFrame()
 
    def get_faculty(self, dataframe: pd.DataFrame) -> pd.DataFrame | None:
        """
        Gets faculty type
        """
        try:
            faculty_df = dataframe.loc[dataframe["fac_type"] == "P"]
            logging.info(f"-----Filtered permentant faculty-----: \n{faculty_df}")
            return faculty_df

        except Exception as e:
            logger.exception("Error occurred while getting faculty information")
            return pd.DataFrame()

# a dictionary containing user selection
user_selection = {
    "graph_type": "single_class",  # options: single_class, department, class_level_dept
    "Subject": "CIS",
    "class_code": "CIS210",  # relevant if graph type is single_class; specific class code (e.g., CIS 422)
     # "department": "Computer Information Science",  # relevant for single_dept and class_level_dept
    "class_level": "300",  # relevant if graph type is class_level_dept; specific class level (e.g., 100, 200)
    "instructor": "Regular Faculty", # All instructors or Regular Faculty
    "grade_type": "Percent Ds/Fs",  # other option: "Percent Ds/Fs"
    #"grade_type": "Percent As",
    "class_count": True,  # whether to show the number of classes taught by each instructor
    "xaxis_course": True,
 }


if __name__ == "__main__":
    #dest = "../Databases/GradeDatabase.sqlite"
    dest = "../Databases/CompleteDatabase.sqlite"
    fetch = DataFetcher(user_selection, dest)
    dataframe = fetch.fetch_data()
