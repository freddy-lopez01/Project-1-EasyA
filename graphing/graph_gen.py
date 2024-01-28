import pandas as pd
import matplotlib.pyplot as plt
import logging
from data_fetch import DataFetcher


# a dictionary containing user selection
user_selection = {
    "graph_type": "single_class",  # options: single_class, department, class_level_dept
    "class_code": "CIS313",  # relevant if graph type is single_class; specific class code (e.g., CIS 422)
    # "department": "Computer Information Science",  # relevant for single_dept and class_level_dept
    "class_level": "200",  # relevant if graph type is class_level_dept; specific class level (e.g., 100, 200)
    "instructor_type": "All Instructors",  # other option: "Faculty"
    #"grade_type": "Percent As",  # other option: "Percent Ds/Fs"
    "grade_type": "Percent As", # true/false
    "class_count": True  # whether to show the number of classes taught by each instructor
}

db_path = "../Databases/GradeDatabase.sqlite"


fetcher = DataFetcher(user_selection, db_path)
fetcher.fetch_data()

main_df = fetcher.main_data
class_count = fetcher.class_count
main_df = main_df.merge(class_count, on='instructor', how='left')
instructor_data = fetcher.instructor_data
grades = fetcher.percent_grade.round(2)

def single_class_graph(dataframe: pd.DataFrame, grades: float) -> None:
    """
    Generates a single class bar graph

    Parameters:
    - dataframe (pd.DataFrame): The dataframe containing instructor data.
    - title_grade_type (str): The grade type to be displayed in the title.
    - class_code (str): The class code to be displayed in the title.
    """
    # plot percent As based on instructor
    ax = dataframe.plot(kind="bar", x="instructor", y="Percent As", legend=False)
    ax.set_ylim(0, 100)
    plt.title(f"Distribution of {user_selection['grade_type']} for {user_selection['class_code']}")
    plt.ylabel(f"{user_selection['grade_type']} (%)")
    plt.xlabel("Instructors")
    if user_selection["class_count"] is True:
        for index, row in dataframe.iterrows():
            ax.text(index, row['Percent As'] + 1, f"({row['class_count']})", ha='center')

    plt.xticks(rotation=40, ha='right')
    plt.tight_layout()
    plt.show()

def single_department_graph():
    """
    Generates a single department bar graph
    """
    pass

def class_level_dept_graph():
    """
    Generates
    """
    pass


def main():
    single_class_graph(instructor_data, instructor_data["Percent As"])

if __name__ == "__main__":
    main()
