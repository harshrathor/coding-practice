
import json
from pathlib import Path

DATA_FILE = Path("students.json")


class StudentManagementSystem:
    def __init__(self):
        self.students = self.load_students()

    def load_students(self):
        if DATA_FILE.exists():
            try:
                with DATA_FILE.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                    return {str(k): v for k, v in data.items()}
            except (json.JSONDecodeError, OSError):
                print("Warning: Could not read student data.")
        return {}

    def save_students(self):
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.students, file, indent=4)
            
    def add_student(self):
        student_id = input("Enter student ID: ").strip()

        if not student_id:
            print("Student ID cannot be empty.")
            return

        if student_id in self.students:
            print("Student ID already exists.")
            return

        name = input("Enter student name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        try:
            age = int(input("Enter age: "))
            if age <= 0:
                print("Age must be positive.")
                return

            marks = float(input("Enter marks (0-100): "))
            if not 0 <= marks <= 100:
                print("Marks must be between 0 and 100.")
                return
        except ValueError:
            print("Please enter valid numbers.")
            return

        self.students[student_id] = {
            "name": name,
            "age": age,
            "marks": marks
        }
        self.save_students()
        print("Student added successfully!")

    def calculate_grade(self, marks):
        if marks >= 90:
            return "A+"
        elif marks >= 80:
            return "A"
        elif marks >= 70:
            return "B"
        elif marks >= 60:
            return "C"
        elif marks >= 40:
            return "D"
        return "F"

    def view_students(self):
        if not self.students:
            print("No student records found.")
            return

        print("\n--- STUDENT RECORDS ---")
        print(f"{'ID':<12}{'Name':<20}{'Age':<8}"
              f"{'Marks':<10}{'Grade':<8}")
        print("-" * 58)

        for student_id, student in sorted(self.students.items()):
            grade = self.calculate_grade(student["marks"])
            print(
                f"{student_id:<12}"
                f"{student['name']:<20}"
                f"{student['age']:<8}"
                f"{student['marks']:<10.2f}"
                f"{grade:<8}"
            )

    def search_student(self):
        student_id = input("Enter student ID to search: ").strip()
        student = self.students.get(student_id)

        if student:
            print("\nStudent found!")
            print("ID:", student_id)
            print("Name:", student["name"])
            print("Age:", student["age"])
            print("Marks:", student["marks"])
            print("Grade:", self.calculate_grade(student["marks"]))
        else:
            print("Student not found.")

    def update_marks(self):
        student_id = input("Enter student ID: ").strip()

        if student_id not in self.students:
            print("Student not found.")
            return

        try:
            marks = float(input("Enter new marks (0-100): "))
            if not 0 <= marks <= 100:
                print("Marks must be between 0 and 100.")
                return
        except ValueError:
            print("Please enter valid marks.")
            return

        self.students[student_id]["marks"] = marks
        self.save_students()
        print("Marks updated successfully!")

    def delete_student(self):
        student_id = input("Enter student ID to delete: ").strip()

        if student_id in self.students:
            del self.students[student_id]
            self.save_students()
            print("Student deleted successfully!")
        else:
            print("Student not found.")

    def show_statistics(self):
        if not self.students:
            print("No records available for statistics.")
            return

        marks = [s["marks"] for s in self.students.values()]
        average = sum(marks) / len(marks)
        topper_id = max(
            self.students,
            key=lambda sid: self.students[sid]["marks"]
        )
        topper = self.students[topper_id]

        print("\n--- CLASS STATISTICS ---")
        print("Total students:", len(self.students))
        print(f"Average marks: {average:.2f}")
        print("Highest marks:", max(marks))
        print("Lowest marks:", min(marks))
        print("Topper:", topper["name"])
        print("Topper's marks:", topper["marks"])

    def run(self):
        while True:
            print("\n===== STUDENT MANAGEMENT SYSTEM =====")
            print("1. Add student")
            print("2. View all students")
            print("3. Search student")
            print("4. Update marks")
            print("5. Delete student")
            print("6. Class statistics")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_marks()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                self.show_statistics()
            elif choice == "7":
                print("Thank you for using the system!")
                break
            else:
                print("Invalid choice. Please select 1-7.")


if __name__ == "__main__":
    app = StudentManagementSystem()
    app.run()
