from PyQt6.QtWidgets import *
from gui import *
import csv


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        Method to set up window and add button functionality
        :return: None
        """
        super().__init__()
        self.setupUi(self)
        self.students: dict = self.get_file()
        self.update()

        self.button_calc.clicked.connect(lambda: self.calculate())
        self.button_del.clicked.connect(lambda: self.delete())

    def get_file(self) -> dict:
        """
        Method for getting information from a csv file or creating a csv file if none exists
        :return: A dictionary with a key corresponding to a students name and a value of a list containing the student's
        score and grade
        """
        try:
            with open("students.csv", 'r') as file:
                csv_r = csv.reader(file)
                students: dict = {}
                next(csv_r)
                for line in csv_r:
                    students[line[0]] = [float(line[1]), line[2]]
                return students
        except FileNotFoundError:
            with open("students.csv", 'w', newline='') as file:
                csv_w = csv.writer(file)
                csv_w.writerow(['Name', 'Score', 'Grade'])
            return {}

    def calculate(self) -> None:
        """
        Method that adds input values to the dictionary and calculates letter grades for students based on the top
        scorer
        :return: None
        """
        try:
            if float(self.input_score.text()) < 0:
                raise TypeError
            self.students[self.input_student.text()] = [float(self.input_score.text()), '']
            best: float = 0
            for i in self.students:
                if self.students[i][0] > best:
                    best = self.students[i][0]

            for i in self.students:
                if self.students[i][0] >= best - 10:
                    self.students[i][1] = 'A'
                elif self.students[i][0] >= best - 20:
                    self.students[i][1] = 'B'
                elif self.students[i][0] >= best - 30:
                    self.students[i][1] = 'C'
                elif self.students[i][0] >= best - 40:
                    self.students[i][1] = 'D'
                else:
                    self.students[i][1] = 'F'
            self.update()

        except ValueError:
            self.label_main.setText("Input a numeric value for the score")
        except TypeError:
            self.label_main.setText("Input a non-negative value for the score")

    def delete(self) -> None:
        """
        Method for deleting a student's information from dictionary
        :return: None
        """
        try:
            x: str | None = self.students.pop(self.input_del.text())
            if x is None:
                raise KeyError
            self.update()
        except KeyError:
            self.label_main.setText("No student with that name was found")

    def update(self) -> None:
        """
        Method for updating gui and csv file
        :return: None
        """
        with open("students.csv", 'w', newline='') as file:
            csv_w = csv.writer(file)
            csv_w.writerow(['Name', 'Score', 'Grade'])
            for i in self.students:
                csv_w.writerow([i, self.students[i][0], self.students[i][1]])
        self.label_name.setText('Name\n\n'+'\n'.join(self.students.keys()))
        self.label_score.setText('Score\n\n'+'\n'.join([str(x[0]) for x in self.students.values()]))
        self.label_grade.setText('Grade\n\n'+'\n'.join([x[1] for x in self.students.values()]))
        self.label_main.setText("Input a name and score you would like to add or edit")
        self.input_student.clear()
        self.input_score.clear()
        self.input_del.clear()
