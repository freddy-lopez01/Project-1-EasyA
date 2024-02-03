import pandas as pd
import matplotlib.pyplot as plt
import logging
from data_fetch import DataFetcher
#from graphing.data_fetch import DataFetcher

# setting up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

def single_class_graph(user_selection: dict, dataframe: pd.DataFrame) -> None:
    """
    Generates a single class bar graph
    Parameters:
    - dataframe (pd.DataFrame): The dataframe containing instructor data.
    """
    logger.debug(f"DataFrame columns: {dataframe.columns}")
    try:
        # dynamically adjust plot size based on the number of unique instructors or classes
        num_instructors = len(dataframe["instructor"].unique())
        width = max(10, num_instructors * 0.5)
        height = 8

        # create figure and axes
        fig, ax = plt.subplots(figsize=(width, height), constrained_layout=True)

        # plotting graph and bar graph changes color based on grade type
        if user_selection["grade_type"] == "Percent As":
            dataframe.plot(kind="bar", x="instructor", y=user_selection["grade_type"], ax=ax, legend=False, width=0.15, color="green")
        else:
            dataframe.plot(kind="bar", x="instructor", y=user_selection["grade_type"], ax=ax, legend=False, width=0.15, color="red")

        # title and labels
        ax.set_ylim(0, 100)
        plt.title(f"Distribution of {user_selection['grade_type']} for {user_selection['class_code']}")
        plt.ylabel(f"{user_selection['grade_type']} (%)")

        # display graph x-axis title based on user selection of "All Instructors" or "Regular Faculty"
        if user_selection["class_count"] and user_selection["instructor"] == "Regular Faculty":
            plt.xlabel(f"{user_selection['instructor']} (class count)")
        elif user_selection["class_count"] and user_selection["instructor"] == "All Instructors":
            plt.xlabel(f"{user_selection['instructor']} (class_count)")
        else:
            plt.xlabel("Instructors")

        # display numbers and set tick labels
        if user_selection["class_count"] is True:
            tick_labels = [f"{row['instructor']} ({row['class_count']})" for index, row in dataframe.iterrows()]
            for index, row in dataframe.iterrows():
                ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        else:
            tick_labels = dataframe["instructor"]
            for index, row in dataframe.iterrows():
                ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')

        ax.set_xticklabels(tick_labels, rotation=40, ha='right')

        # show and close figure
        return plt.show()
        #plt.close(fig)
    except Exception as e:
        logger.error(f"========single_class_graph: {e}=======")

def single_department_graph(user_selection: dict, dataframe: pd.DataFrame) -> None:
    """
    Generates a single department bar graph
    """
    # determine number of unique instructors
    logger.debug(f"DataFrame columns: {dataframe.columns}")
    try: 

        # dynamically adjust plot size based on the number of unique instructors or classes
        num_instructors = len(dataframe["instructor"].unique())
        width = max(10, num_instructors * 0.5) 
        height = 8

        # create a figure with the new dimensions
        fig, ax = plt.subplots(figsize=(width, height), constrained_layout=True)
        
        # plotting graph and bar graph changes color based on grade type
        if user_selection["grade_type"] == "Percent As":
            dataframe.plot(kind="bar", x="instructor", y=user_selection["grade_type"], ax=ax, legend=False, width=0.2, color="green")
        else:
            dataframe.plot(kind="bar", x="instructor", y=user_selection["grade_type"], ax=ax, legend=False, width=0.2, color="red")


        plt.title(f"Distribution of {user_selection['grade_type']}s in ... Department")
        plt.ylabel(f"{user_selection['grade_type']} (%)")
        ax.set_ylim(0, 100)

        # display graph x-axis title based on user selection of "All Instructors" or "Regular Faculty"
        if user_selection["class_count"] and user_selection["instructor"] == "Regular Faculty":
            plt.xlabel(f"{user_selection['instructor']} (class count)")
        elif user_selection["class_count"] and user_selection["instructor"] == "All Instructors":
            plt.xlabel(f"{user_selection['instructor']} (class_count)")
        else:
            plt.xlabel("Instructors")

        # display numbers and tick labels
        if user_selection["class_count"] is True:
            tick_labels = [f"{row['instructor']} ({row['class_count']})" for index, row in dataframe.iterrows()]
            for index, row in dataframe.iterrows():
                ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        else:
            tick_labels = dataframe["instructor"]
            for index, row in dataframe.iterrows():
                ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')

        ax.set_xticklabels(tick_labels, rotation=40, ha='right')
        return plt.show()
        #plt.close(fig)
    except Exception as e:
        logger.error(f"single_department_graph()========================{e}===========================")

def class_level_dept_graph(user_selection: dict, dataframe: pd.DataFrame) -> None:
    """
    Generates a single bar graph for all classes of a particular level within a department
    """

    logger.debug(f"DataFrame columns: {dataframe.columns}")
    try:
        # dynamically adjust plot size based on the number of unique instructors or classes
        num_instructors = len(dataframe["instructor"].unique())
        width = max(10, num_instructors * 0.5)
        height = 8
        fig, ax = plt.subplots(figsize=(width, height), constrained_layout=True)

        # plotting graph and bar graphs changes colors based on grade type
        if user_selection["grade_type"] == "Percent As":
            ax = dataframe.plot(kind="bar", x="instructor", y=user_selection["grade_type"], ax=ax, legend=False, width=0.2, color="green")
        else:
            ax = dataframe.plot(kind="bar", x="instructor", y=user_selection["grade_type"], ax=ax, legend=False, width=0.2, color="red")

        # graph title
        plt.title(f"Distribution of {user_selection['grade_type']} for Level {user_selection['class_level']} in ... Department")
        plt.ylabel(f"{user_selection['grade_type']} (%)")
        ax.set_ylim(0, 100)


        # display graph x-axis title based on user selection of "All Instructors" or "Regular Faculty"
        if user_selection["class_count"] and user_selection["instructor"] == "Regular Faculty":
            plt.xlabel(f"{user_selection['instructor']} (class count)")
        elif user_selection["class_count"] and user_selection["instructor"] == "All Instructors":
            plt.xlabel(f"{user_selection['instructor']} (class_count)")
        else:
            plt.xlabel("Instructors")

        # display each instructors class count on x-axis if toggled
        if user_selection["class_count"] is True:
            tick_labels = [f"{row['instructor']} ({row['class_count']})" for index, row in dataframe.iterrows()]
            for index, row in dataframe.iterrows():
                ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        # otherwise, don't display instructors class count
        else:
            tick_labels = (dataframe["instructor"])
            for index, row in dataframe.iterrows():
                ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        ax.set_xticklabels(tick_labels, rotation=40, ha='right')                
        return plt.show()
        #plt.close(fig) 
        
    except Exception as e:
        logger.error(f"class_level_dept_graph()========================={e}=======================")

    #def main(user_selection: dict):
def main():
    # a dictionary containing user selectioN
    user_selection = {
    "graph_type": "class_level_dept",  # options: single_class, department, class_level_dept
    "Subject": "CIS",
    "class_code": "CIS415",  # relevant if graph type is single_class; specific class code (e.g., CIS 422)
        # "department": "Computer Information Science",  # relevant for single_dept and class_level_dept
    "class_level": "400",  # relevant if graph type is class_level_dept; specific class level (e.g., 100, 200)
        #"instructor": "All Instructors", # All instructors or Regular Faculty
    "instructor": "Regular Faculty",
        #"grade_type": "Percent Ds/Fs",  # other option: "Percent Ds/Fs"
    "grade_type": "Percent As",
    "class_count": True,  # whether to show the number of classes taught by each instructor
    "light_mode": False,
    "xaxis_course": True,
    }

    db_path = "../Databases/CompleteDatabase.sqlite"
    fetcher = DataFetcher(user_selection, db_path)
    fetcher.fetch_data()

    instructor_data = fetcher.instructor_data
    logger.info(f"INSTRUCTOR DATA GRAPH: \n {instructor_data}")
    class_data = fetcher.class_data

    if not user_selection["light_mode"]:
        plt.style.use('dark_background')
    
    if user_selection["graph_type"] == "single_class":
        single_class_graph(user_selection, instructor_data)
        return 
    elif user_selection["graph_type"] == "department":
        single_department_graph(user_selection, instructor_data)
        return 
    elif user_selection["graph_type"] == "class_level_dept":
        class_level_dept_graph(user_selection, instructor_data)
        return

if __name__ == "__main__":
    main()
