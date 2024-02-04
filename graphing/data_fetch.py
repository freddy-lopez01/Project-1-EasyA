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
            logger.info(f"Class_level: {class_level}")
            instructor_type = self.user_selection.get("instructor_type", None)
            logger.info(f"Instructor_type: {instructor_type}")
            grade_type = self.user_selection.get("grade_type",  True)
            logger.info(f"grade_type: {grade_type}")
            show_class_count = self.user_selection.get("class_count", False)
            logger.info(f"show class count: {show_class_count}")
            class_data = self.user_selection.get("xaxis_course", False)
            logger.info(f"Show course on x-axis: {class_data}")

            # main logic for processing user selection
            if graph_type == "single_class" and single_class:
                filtered_single_class = self.filter_single_class(single_class, dataframe)
                if instructor_type == "Regular Faculty":
                    self.instructor_data = self.get_faculty(filtered_single_class)
                    # merge data for recurring instructors
                    self.instructor_data = self.merge_instructors(self.instructor_data)
                    logger.info(f"-----Filtered DataFrame for 'Regular Faculty'-----\n{self.instructor_data}")
                elif instructor_type == "All Instructors":
                    # filter all instructors
                    self.instructor_data = self.get_instructor_class(filtered_single_class)
                    logger.info(f"-----Filtered DataFrame for 'All Instructors'-----\n{self.instructor_data}")
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
                    logger.info(f"Final merged DataFrame with class count before graphing \n{self.instructor_data}")
                else:
                    # strip last name
                    self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()
                    logger.info(f"Final merged DataFrame before graphing \n{self.instructor_data}")

            # department only
            elif graph_type == "department" and department:
                filtered_department = self.filter_single_dept(subject, dataframe)
                logger.info(f"-----Filtered DataFrame for 'department'----- \n{filtered_department}")
                if instructor_type == "Regular Faculty":
                    self.instructor_data = self.get_faculty(filtered_department)
                    self.instructor_data = self.merge_instructors(self.instructor_data)
                    logger.info(f"-----Filtered DataFrame for 'Regular Faculty'-----: \n{self.instructor_data}")
                elif instructor_type == "All Instructors":
                    self.instructor_data = self.get_instructor_class(filtered_department)
                    logger.info(f"-----Filtered dataframe for 'All Instructors'-----: \n{self.instructor_data}")
                
                if grade_type == "Percent Ds/Fs":
                    self.percent_grade = self.calc_percent_DsFs_instructor(self.instructor_data)
                    logger.info(f"-----Filtered percent grade DsFs-----: \n{self.percent_grade}")
                elif grade_type == "Percent As":
                    self.percent_grade = self.calc_percent_a_instructor(self.instructor_data)
                    logger.info(f"-----Filtered Percent As-----: \n{self.percent_grade}")

                # if toggle class count for department graph
                if show_class_count:
                    # get class data and class count and merge the two DataFrames together
                    self.class_count = self.instructor_class_count(filtered_department)
                    self.instructor_data = self.percent_grade
                    self.instructor_data = self.instructor_data.merge(self.class_count, on="instructor")
                    self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()

                    logger.info(f"Final merged DataFrame with class count before graphing \n{self.instructor_data}")
                else:
                    self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()
                    logger.info(f"Final merged DataFrame with before graphing \n{self.instructor_data}")
                    
            # user selects all classes of a particular level within department
            elif graph_type == "class_level_dept":
                filtered_department = self.filter_class_level_dept(subject, class_level, dataframe)
                logger.info(f"-----Dataframe before filtering-----: \n{dataframe}")
                logger.info(f"FILTERED CLASS_LEVEL DEPT\n {filtered_department}")

                # if user toggles view xaxis_course, specific course data will be used instead of instructor data
                # otherwise, use instructor data
                if class_data:
                    self.class_data = self.get_class_count(filtered_department)
                    logger.info(f"Filtered Class DataFrame with class count\n{self.class_data}")
                    # get course count on recurring courses and combine the data
                    get_class_data = self.get_class_data(filtered_department)
                    self.class_data = self.class_data.merge(get_class_data, on="group_code")
                    logger.info(f"-----Merged specific course count-----\n{self.class_data}")

                    if grade_type == "Percent Ds/Fs":
                        self.percent_grade = self.calc_percent_DsFs_class(self.class_data)
                        logger.info(f"----Calculated percent Ds/Fs for each course----\n{self.percent_grade}")
                    else:
                        self.percent_grade = self.calc_percent_a_class(self.class_data)
                        logger.info(f"Percent Grade As with class data\n{self.percent_grade}")
                    self.class_data = self.percent_grade

                else:
                    # process instructor data
                    if instructor_type == "Regular Faculty":
                        self.instructor_data = self.get_faculty(filtered_department)
                        self.instructor_data = self.merge_instructors(self.instructor_data)
                        logger.info(f"-----Filtered DataFrame for 'Regular Faculty'-----\n{self.instructor_data}")
                    elif instructor_type == "All Instructors":
                        self.instructor_data = self.get_instructor_class(filtered_department)
                        logger.info(f"-----Filtered DataFrame for 'All Instructors'-----\n{self.instructor_data}")
                    # calculate percent As or Ds/Fs
                    if grade_type == "Percent Ds/Fs":
                        self.percent_grade = self.calc_percent_DsFs_instructor(self.instructor_data)
                        logger.info(f"-----Filtered DataFrame with percent Ds/Fs-----\n{self.percent_grade}")
                    elif grade_type == "Percent As":
                        self.percent_grade = self.calc_percent_a_class(self.instructor_data)
                        logger.info(f"-----Filtered DataFrame with percent As----- \n{self.percent_grade}")
                    # if user toggles show_class_count
                    # strip and keep professors last name
                    if show_class_count:
                        self.class_count = self.instructor_class_count(filtered_department)
                        self.instructor_data = self.instructor_data.merge(self.class_count, on="instructor")
                        self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()
                        logging.info(f"-----Final DataFrame before graphing------ \n{self.instructor_data}")
                    else:
                        self.instructor_data.loc[:, "instructor"] = self.instructor_data["instructor"].str.split(", ", expand=True)[0].str.strip()
                        logging.info(f"-----Final DataFrame before graphing------ \n{self.instructor_data}")
                    logger.debug("User selection: %s", self.user_selection)

        except Exception as e:
            logger.exception("Exception occurred during data fetch")
        finally:
            if self.connection:
                self.close_connection()

    def merge_instructors(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Merge recurring instructors
        """
        try:
            instructor_data = dataframe.groupby("instructor").agg({
                "aprec": "sum",
                "bprec": "sum",
                "cprec": "sum",
                "dprec": "sum",
                "fprec": "sum",
                "fac_type": "first"
            }).reset_index()
            logger.info(f"Merged recurring instructors: \n{instructor_data}")
            return instructor_data 

        except Exception as e:
            logger.exception(f"Exception occurred during merge_instructor")


    def get_instructor(self, group_code: str, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filters list for instructors
        """
        try:
            if dataframe.empty:
                logger.info("DataFrame is empty. No instructors to extract.")
                return pd.DataFrame()
            # filter the DataFrame for the given class code and get unique instructors
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

    def filter_class_level_dept(self, subject: str, class_level: str, dataframe: pd.DataFrame) -> pd.DataFrame:

        """
        Filters the DataFrame for rows matching a department and a specific class level (e.g., 400).
        """
        try:
            filtered_dept = self.filter_single_dept(subject, dataframe)
            logging.info(f"----Filtered Department-----: \n {filtered_dept}")

            # calculate class level range based on the provided class_level
            class_level_int = int(class_level)
            class_level_range_start = class_level_int // 100 * 100
            class_level_range_end = class_level_range_start + 99
            logging.info(f"Class level range: {class_level_range_start} to {class_level_range_end}")

            # using regex to match any number of letters followed by the class level range numbers
            regex_pattern = f"^{subject}\d{{{len(class_level)}}}[A-Za-z]*$"
            #regex_pattern = f"^{subject}[0-9]{{{len(class_level)}}}$"
            class_level_series = filtered_dept["group_code"].str.extract(f'({regex_pattern})')[0]
            #class_level_series = filtered_dept["group_code"].str.extract('(\d+)$')[0].astype(int)
            class_level_series = class_level_series.str.extract('(\d+)')[0].dropna().astype(int)

            filtered_department = filtered_dept[class_level_series.between(class_level_range_start, class_level_range_end)]
            #filtered_department = filtered_dept[
            #   filtered_dept["group_code"].str.match(regex_pattern) & 
            #   class_level_series.between(class_level_range_start, class_level_range_end)]
            #logging.info(f"-----Filtered Class Level: \n{filtered_department}")
            return filtered_department

        except Exception as e:
            logger.exception(f"Exception occurred during filtering class level dept {e}")
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
        logging.info(f"----DataFrame before calculating Percent As-----\n{instructor_grades}")
        try:
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
        logging.info(f"DataFrame before filtering instructor_class: \n{dataframe}")
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
            class_count_df = class_count_df.rename(columns={"index": "group_code"})
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


"""
# a dictionary containing user selection
user_selection = {
    "graph_type": "class_level_dept",  # options: single_class, department, class_level_dept
    "Subject": "CIS",
    "class_code": "CIS415",  # relevant if graph type is single_class; specific class code (e.g., CIS 422)
     # "department": "Computer Information Science",  # relevant for single_dept and class_level_dept
    "class_level": "300",  # relevant if graph type is class_level_dept; specific class level (e.g., 100, 200)
    "instructor_type": "All Instructors", # All instructors or Regular Faculty
    #"instructor_type": "Regular Faculty",
    #"grade_type": "Percent Ds/Fs",  # other option: "Percent Ds/Fs"
    "grade_type": "Percent As",
    "class_count": True,  # whether to show the number of classes taught by each instructor
    "xaxis_course": False,
 }

if __name__ == "__main__":
    dest = "../Databases/CompleteDatabase.sqlite"
    fetch = DataFetcher(user_selection, dest)

    dataframe = fetch.fetch_data()

"""
