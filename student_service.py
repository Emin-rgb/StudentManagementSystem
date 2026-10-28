from database import (
    add_student,
    get_students,
    search_students,
    update_student,
    delete_student,
    sort_students_by_gpa,
    filter_students_by_major,
    filter_and_sort_students,
    get_student_statistics,
    get_student_counts_by_major
)
from exceptions import StudentNotFoundError


class StudentService:

    def add(self, student):
        self.validate_student(student)
        add_student(student)
        

    def get_all(self):
        return get_students()

    def search(self, keyword):
        return search_students(keyword)

    def update(self, student):
        self.validate_student(student)
        update_student(student)

    def delete(self, student_id):
        students = self.get_all()

        student_exists = any(
            student.student_id == student_id
            for student in students
        )

        if not student_exists:
            raise StudentNotFoundError(
                f"Student '{student_id}' was not found."
            )

        delete_student(student_id)

    def validate_student(self, student):
        if not student.name.strip():
            raise ValueError("Name cannot be empty.")

        if not student.surname.strip():
            raise ValueError("Surname cannot be empty.")

        if not student.email.strip():
            raise ValueError("Email cannot be empty.")

        if "@" not in student.email:
            raise ValueError("Invalid email.")

        if not student.major.strip():
            raise ValueError("Major cannot be empty.")

        if not 0 <= student.gpa <= 100:
            raise ValueError("GPA must be between 0 and 100.")

    def sort_by_gpa(self, descending=True):
        return sort_students_by_gpa(descending)

    def filter_by_major(self, major):
        return filter_students_by_major(major)
    
    def filter_and_sort(self, major, descending=True):
        return filter_and_sort_students(major, descending)

    def get_statistics(self):
        return get_student_statistics()

    def get_counts_by_major(self):
        return get_student_counts_by_major()