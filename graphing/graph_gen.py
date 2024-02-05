import pandas as pd
import matplotlib.pyplot as plt
import logging
from graphing.data_fetch import DataFetcher
#from data_fetch import DataFetcher

# setting up logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def single_class_graph(user_selection: dict, dataframe: pd.DataFrame) -> None:
    """
    Generates a single class bar graph
    Parameters:
    - dataframe (pd.DataFrame): The dataframe containing instructor data.
    """
    logger.debug(f"DataFrame columns: {dataframe.columns}")
    logger.info(f"DataFrame Columns Before graphing: \n{dataframe}")
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
        if user_selection["class_count"] and user_selection["instructor_type"] == "Regular Faculty":
            plt.xlabel(f"{user_selection['instructor_type']} (class count)")
        elif user_selection["class_count"] and user_selection["instructor_type"] == "All Instructors":
            plt.xlabel(f"{user_selection['instructor_type']} (class_count)")
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
        logger.exception(f"Error generating graph: {e}")
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
        if user_selection["class_count"] and user_selection["instructor_type"] == "Regular Faculty":
            plt.xlabel(f"{user_selection['instructor_type']} (class count)")
        elif user_selection["class_count"] and user_selection["instructor_type"] == "All Instructors":
            plt.xlabel(f"{user_selection['instructor_type']} (class_count)")
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
        width = 10
        height = 8
        if user_selection.get("xaxis_course", False):
            num_classes = len(dataframe["group_code"].unique())
            logging.info("NUM UNIQUE CLAS")
            width = max(width, num_classes * 0.5)
        else:
            num_instructors = len(dataframe["instructor"].unique())
            width = max(width, num_instructors * 0.5)

        fig, ax = plt.subplots(figsize=(width, height), constrained_layout=True)

        # determine x-axis
        if user_selection.get("xaxis_course", False):
            x_axis = "group_code"
        else:
            x_axis = "instructor" # default


        # determine color of bar graph
        color = "green" # default
        if user_selection["grade_type"] == "Percent Ds/Fs":
            color = "red"

        # plot graph
        ax = dataframe.plot(kind="bar", x=x_axis, y=user_selection["grade_type"], ax=ax, legend=False, width=0.2, color=color)

        # graph title
        title_suffix = "Instructors"  # Default value
        if user_selection.get("xaxis_course", False):
            title_suffix = "Classes"
        plt.title(f"Distribution of {user_selection['grade_type']} for Level {user_selection['class_level']} in ... Department")
        plt.ylabel(f"{user_selection['grade_type']} (%)")
        ax.set_ylim(0, 100)

        # display graph x-axis title based on user selection of "All Instructors" or "Regular Faculty"
        x_axis_label = "Instructors"  # default value
        if user_selection["class_count"]:
            x_axis_label += " (class count)"
        if user_selection.get("xaxis_course", False):
            x_axis_label = "Classes"  #  will override the above if "xaxis_course" is True
            if user_selection["class_count"]:
                x_axis_label += " (class count)"
        plt.xlabel(x_axis_label)

        # display each instructors class count on x-axis if toggled
        tick_labels = []
        for index, row in dataframe.iterrows():
            label = f"{row[x_axis]}"
            if user_selection.get("class_count", False):
                label += f" ({row['class_count']})"
            tick_labels.append(label)
            # text above bars
            percentage = f"{row[user_selection['grade_type']]}%"
            ax.text(index, row[user_selection["grade_type"]] + 1, percentage, ha='center')
        
        ax.set_xticklabels(tick_labels, rotation=40, ha='right')                
        return plt.show()
        #plt.close(fig) 
        
    except Exception as e:
        logger.error(f"class_level_dept_graph()========================={e}=======================")

def main(user_selection: dict):
#def main():
    # a dictionary containing user selectioN
    """
    user_selection = {
    "graph_type": "class_level_dept",  # options: single_class, department, class_level_dept
    "Subject": "CIS",
    "class_code": "CIS315",  # relevant if graph type is single_class; specific class code (e.g., CIS 422)
        # "department": "Computer Information Science",  # relevant for single_dept and class_level_dept
    "class_level": "300",  # relevant if graph type is class_level_dept; specific class level (e.g., 100, 200)
    #"instructor_type": "All Instructors", # All instructors or Regular Faculty
    "instructor_type": "Regular Faculty",
    #"grade_type": "Percent Ds/Fs",  # other option: "Percent Ds/Fs"
    "grade_type": "Percent As",
    "class_count": False,  # whether to show the number of classes taught by each instructor
    "light_mode": False,
    "xaxis_course": True,
    }
    """
    db_path = "./Databases/CompleteDatabase.sqlite"
    fetcher = DataFetcher(user_selection, db_path)
    fetcher.fetch_data()

    class_data_to_graph = fetcher.class_data
    logger.info(f"CLASS DATA TO GRAPH: \n {class_data_to_graph}")
    instructor_data_to_graph = fetcher.instructor_data
    logger.info(f"INSTRUCTOR DATA TO GRAPH: {instructor_data_to_graph}")

    if not user_selection["light_mode"]:
        plt.style.use('dark_background')
    
    if user_selection["graph_type"] == "single_class":
        single_class_graph(user_selection, instructor_data_to_graph)
        return 
    elif user_selection["graph_type"] == "department":
        single_department_graph(user_selection, instructor_data_to_graph)
        return 
    elif user_selection["graph_type"] == "class_level_dept":
        if user_selection["xaxis_course"] is False:
            class_level_dept_graph(user_selection, instructor_data_to_graph)
        else:
            class_level_dept_graph(user_selection, class_data_to_graph)

        return

