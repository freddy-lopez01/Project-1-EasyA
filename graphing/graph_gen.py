import pandas as pd
import matplotlib.pyplot as plt
import logging
from data_fetch import DataFetcher



def single_class_graph(user_selection: dict, dataframe: pd.DataFrame) -> None:
    """
    Generates a single class bar graph
    Parameters:
    - dataframe (pd.DataFrame): The dataframe containing instructor data.
    - title_grade_type (str): The grade type to be displayed in the title.
    - class_code (str): The class code to be displayed in the title.
    """

    # determine number of unique instructors
    num_instructors = len(dataframe["instructor"].unique())
    # set the width based on the number of instructors
    width = max(10, num_instructors * 0.5) 
    height = 8

    # create a figure with the new dimensions
    plt.figure(figsize=(width, height), constrained_layout=True)
    # plot percent grades based on instructor
    ax = dataframe.plot(kind="bar", x="instructor", y=user_selection["grade_type"], legend=False, width=0.15)
    ax.set_ylim(0, 100)
    plt.title(f"Distribution of {user_selection['grade_type']} for {user_selection['class_code']}")
    plt.ylabel(f"{user_selection['grade_type']} (%)")
    plt.xlabel("Instructors")
    # display number of classes taught by each instructor if toggled
    # update tick labels with class count if flag is True
    if user_selection["class_count"] is True:
        for index, row in dataframe.iterrows():
            ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        tick_labels = [f"{row['instructor']} ({row['class_count']})" for index, row in dataframe.iterrows()]
        ax.set_xticklabels(tick_labels, rotation=40, ha='right')
    else:
        for index, row in dataframe.iterrows():
            ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        ax.set_xticklabels(dataframe['instructor'], rotation=40, ha='right') 
    plt.tight_layout()
    plt.show()
    plt.close()

def single_department_graph(user_selection: dict, dataframe: pd.DataFrame) -> None:
    """
    Generates a single department bar graph
    """
    # determine number of unique instructors
    num_instructors = len(dataframe["instructor"].unique())
    # set the width based on the number of instructors
    width = max(10, num_instructors * 0.5) 
    height = 8

    # create a figure with the new dimensions
    plt.figure(figsize=(width, height), constrained_layout=True)
    
    ax = dataframe.plot(kind="bar", x="instructor", y=user_selection["grade_type"], legend=False, width=0.2)
    ax.set_ylim(0, 100)
    plt.title(f"Distribution of {user_selection['grade_type']} for ")
    plt.ylabel(f"{user_selection['grade_type']} (%)")
    plt.xlabel("Group Codes")
    if user_selection["class_count"] is True:
        for index, row in dataframe.iterrows():
            ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        tick_labels = [f"{row['instructor']} ({row['class_count']})" for index, row in dataframe.iterrows()]
        ax.set_xticklabels(tick_labels, rotation=40, ha='right')
    else:
        for index, row in dataframe.iterrows():
            ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        ax.set_xticklabels(dataframe['instructor'], rotation=40, ha='right') 
    plt.tight_layout()
    plt.show()
    plt.close()

def class_level_dept_graph(user_selection: dict, dataframe: pd.DataFrame) -> None:
    """
    Generates a single bar graph for all classes of a particular level within a department
    """
    num_instructors = len(dataframe["instructor"].unique())
    width = max(10, num_instructors * 0.5)
    height = 8
    plt.figure(figsize=(width, height), constrained_layout=True)
    ax = dataframe.plot(kind="bar", x="instructor", y=user_selection["grade_type"], legend=False, width=0.2)
    ax.set_ylim(0, 100)
    plt.title(f"Distribution of {user_selection['grade_type']} for ")
    plt.ylabel(f"{user_selection['grade_type']} (%)")
    if user_selection["class_count"]:
        plt.xlabel("Group Codes")
    if user_selection["class_count"] is True:
        for index, row in dataframe.iterrows():
            ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        tick_labels = [f"{row['instructor']} ({row['class_count']})" for index, row in dataframe.iterrows()]
        ax.set_xticklabels(tick_labels, rotation=40, ha='right')
    else:
        for index, row in dataframe.iterrows():
            ax.text(index, row[user_selection["grade_type"]] + 1, f"{row[user_selection['grade_type']]}%", ha='center')
        ax.set_xticklabels(dataframe['instructor'], rotation=40, ha='right') 
    plt.tight_layout()
    plt.show()
    plt.close()

def main():

    # a dictionary containing user selection
    user_selection = {
        "graph_type": "class_level_dept",  # options: single_class, department, class_level_dept
        "class_code": "CIS330",  # relevant if graph type is single_class; specific class code (e.g., CIS 422)
        # "department": "Computer Information Science",  # relevant for single_dept and class_level_dept
        "class_level": "200",  # relevant if graph type is class_level_dept; specific class level (e.g., 100, 200)
        "instructor_type": "All Instructors",  # other option: "Faculty"
        "grade_type": "Percent As",  # other option: "Percent Ds/Fs"
        #"grade_type": "Percent Ds/Fs", # true/false
        "class_count": False,  # whether to show the number of classes taught by each instructor
        "xaxis_course": False, # displays courses instead of instructor
        "light_mode": False # True = light mode, False = dark mode
    }

    db_path = "../Databases/GradeDatabase.sqlite"
    fetcher = DataFetcher(user_selection, db_path)
    fetcher.fetch_data()

    instructor_data = fetcher.instructor_data
    class_data = fetcher.class_data

    if not user_selection["light_mode"]:
        plt.style.use('dark_background')
    
    if user_selection["graph_type"] == "single_class":
        single_class_graph(user_selection, instructor_data)
    elif user_selection["graph_type"] == "department":
        single_department_graph(user_selection, instructor_data)
    elif user_selection["graph_type"] == "class_level_dept":
        class_level_dept_graph(user_selection, instructor_data)


if __name__ == "__main__":
    main()



