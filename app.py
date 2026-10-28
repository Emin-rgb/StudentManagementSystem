from student_service import StudentService
from models import Student
from exceptions import StudentNotFoundError
from exceptions import (
    StudentNotFoundError,
    DuplicateStudentError
)

student_service = StudentService()

def get_gpa():
    while True:
        try:
            gpa = float(input("GPA: "))

            if 0 <= gpa <= 100:
                return gpa

            print("GPA must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


def get_student_id():
    while True:
        student_id = input("Student ID: ").strip()

        if student_id:
            return student_id

        print("Student ID cannot be empty.")


def get_email():
    while True:
        email = input("Email: ").strip()

        if "@" in email and "." in email:
            return email

        print("Please enter a valid email address.")


def add_student_menu():
    student_id = get_student_id()
    name = input("Name: ")
    surname = input("Surname: ")
    email = get_email()
    major = input("Major: ")
    gpa = get_gpa()

    student = Student(
        student_id,
        name,
        surname,
        email,
        major,
        gpa
    )

    try:
        student_service.add(student)

    except ValueError as e:
        print(f"Error: {e}")

    except (StudentNotFoundError, DuplicateStudentError) as e:
        print(f"Error: {e}")

def view_students():
    students = student_service.get_all()

    if not students:
        print("\nNo students found.")
        return

    print("\n" + "=" * 85)
    print(f"{'ID':<12}{'Name':<15}{'Surname':<15}{'Major':<22}{'GPA':<8}")
    print("=" * 85)

    for student in students:
        print(
            f"{student.student_id:<12}"
            f"{student.name:<15}"
            f"{student.surname:<15}"
            f"{student.major:<22}"
            f"{student.gpa:<8.2f}"
        )

    print("=" * 85)


def update_student_menu():
    student_id = get_student_id()

    name = input("New name: ")
    surname = input("New surname: ")
    email = get_email()
    major = input("New major: ")
    gpa = get_gpa()

    student = Student(
        student_id,
        name,
        surname,
        email,
        major,
        gpa
    )

    try:
        student_service.update(student)
    except ValueError as e:
        print(f"Error: {e}")


def delete_student_menu():
    student_id = get_student_id()

    try:
        student_service.delete(student_id)
    except StudentNotFoundError as e:
        print(f"Error: {e}")

def run():
    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        print("7. Sort Students by GPA")
        print("8. Filter Students by Major")
        print("9. Filter and Sort Students")
        print("10. Student Statistics")
        print("11. Students by Major")

        choice = input("Choose an option: ")

        if choice == "1":
            add_student_menu()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student_menu()

        elif choice == "4":
            update_student_menu()

        elif choice == "5":
            delete_student_menu()

        elif choice == "6":
            print("Goodbye!")
            break
        elif choice == "7":
            sort_students_menu()
        elif choice == "8":
            filter_students_menu()
        elif choice == "9":
            filter_and_sort_menu()
        elif choice == "10":
            student_statistics_menu()
        elif choice == "11":
            students_by_major_menu()

        else:
            print("Invalid option.")

def search_student_menu():
    keyword = input("Enter student ID, name, or surname: ").strip()

    students = student_service.search(keyword)

    if not students:
        print("No students found.")
        return

    for student in students:
        print("------------------------")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name} {student.surname}")
        print(f"Email: {student.email}")
        print(f"Major: {student.major}")
        print(f"GPA: {student.gpa}")


def sort_students_menu():
    print("\nSort students by GPA")
    print("1. Highest to lowest")
    print("2. Lowest to highest")

    choice = input("Choose an option: ")

    if choice == "1":
        students = student_service.sort_by_gpa(descending=True)
    elif choice == "2":
        students = student_service.sort_by_gpa(descending=False)
    else:
        print("Invalid option.")
        return

    if not students:
        print("No students found.")
        return

    for student in students:
        print("------------------------")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name} {student.surname}")
        print(f"Major: {student.major}")
        print(f"GPA: {student.gpa}")


def filter_students_menu():
    major = input("Enter major to filter by: ").strip()

    if not major:
        print("Major cannot be empty.")
        return

    students = student_service.filter_by_major(major)

    if not students:
        print("No students found for this major.")
        return

    print(f"\nStudents matching major: {major}")

    for student in students:
        print("------------------------")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name} {student.surname}")
        print(f"Major: {student.major}")
        print(f"GPA: {student.gpa}")


def filter_and_sort_menu():
    major = input("Enter major: ").strip()

    if not major:
        print("Major cannot be empty.")
        return

    print("1. Highest GPA first")
    print("2. Lowest GPA first")

    choice = input("Choose sorting order: ")

    if choice == "1":
        descending = True
    elif choice == "2":
        descending = False
    else:
        print("Invalid option.")
        return

    students = student_service.filter_and_sort(
        major,
        descending
    )

    if not students:
        print("No students found for this major.")
        return

    for student in students:
        print("------------------------")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name} {student.surname}")
        print(f"Major: {student.major}")
        print(f"GPA: {student.gpa}")

def student_statistics_menu():
    stats = student_service.get_statistics()

    print("\n===== Student Statistics =====")
    print(f"Total students: {stats['total_students']}")

    if stats["total_students"] == 0:
        print("No GPA data available yet.")
        return

    print(f"Average GPA: {stats['average_gpa']:.2f}")
    print(f"Highest GPA: {stats['highest_gpa']:.2f}")
    print(f"Lowest GPA: {stats['lowest_gpa']:.2f}")

def students_by_major_menu():
    rows = student_service.get_counts_by_major()

    print("\n===== Students by Major =====")

    if not rows:
        print("No students found.")
        return

    for row in rows:
        print(f"{row['major']}: {row['student_count']}")

