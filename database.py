import sqlite3
from models import Student
from exceptions import StudentNotFoundError, DuplicateStudentError

DATABASE_NAME = "students.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            major TEXT NOT NULL,
            gpa REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def add_student(student):
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO students
            (student_id, name, surname, email, major, gpa)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            student.student_id,
            student.name,
            student.surname,
            student.email,
            student.major,
            student.gpa
        ))

        connection.commit()
        print("Student added successfully.")

    except sqlite3.IntegrityError as e:
        if "students.email" in str(e):
            raise DuplicateStudentError(
                "This email is already registered."
            ) from e

        elif "students.student_id" in str(e):
            raise DuplicateStudentError(
                "This student ID is already registered."
            ) from e

        else:
            raise

    finally:
        connection.close()
def get_students():
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM students
    """).fetchall()

    connection.close()

    students = []

    for row in rows:
        student = Student(
            row["student_id"],
            row["name"],
            row["surname"],
            row["email"],
            row["major"],
            row["gpa"]
        )

        students.append(student)

    return students


def update_student(student):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            UPDATE students
            SET name = ?, surname = ?, email = ?, major = ?, gpa = ?
            WHERE student_id = ?
        """, (
            student.name,
            student.surname,
            student.email,
            student.major,
            student.gpa,
            student.student_id
        ))

        if cursor.rowcount == 0:
            connection.rollback()
            raise StudentNotFoundError(
                f"Student '{student.student_id}' was not found."
            )

        connection.commit()
        print("Student updated successfully.")

    except sqlite3.IntegrityError as e:
        connection.rollback()

        if "students.email" in str(e):
            raise DuplicateStudentError(
                "This email is already registered."
            ) from e

        elif "students.student_id" in str(e):
            raise DuplicateStudentError(
                "This student ID is already registered."
            ) from e

        else:
            raise

    finally:
        connection.close()

def delete_student(student_id):
    connection = get_connection()

    cursor = connection.execute("""
        DELETE FROM students
        WHERE student_id = ?
    """, (student_id,))

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        print("Error: Student not found.")
    else:
        print("Student deleted successfully.")

def search_students(keyword):
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM students
        WHERE student_id LIKE ?
           OR name LIKE ?
           OR surname LIKE ?
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    )).fetchall()

    connection.close()

    students = []

    for row in rows:
        student = Student(
            row["student_id"],
            row["name"],
            row["surname"],
            row["email"],
            row["major"],
            row["gpa"]
        )

        students.append(student)

    return students


def sort_students_by_gpa(descending=True):
    connection = get_connection()

    order = "DESC" if descending else "ASC"

    students = connection.execute(f"""
        SELECT * FROM students
        ORDER BY gpa {order}
    """).fetchall()

    connection.close()

    return [
        Student(
            row["student_id"],
            row["name"],
            row["surname"],
            row["email"],
            row["major"],
            row["gpa"]
        )
        for row in students
    ]

def filter_students_by_major(major):
    connection = get_connection()

    rows = connection.execute("""
        SELECT * FROM students
        WHERE major LIKE ?
        ORDER BY name ASC
    """, (f"%{major}%",)).fetchall()

    connection.close()

    return [
        Student(
            row["student_id"],
            row["name"],
            row["surname"],
            row["email"],
            row["major"],
            row["gpa"]
        )
        for row in rows
    ]


def filter_and_sort_students(major, descending=True):
    connection = get_connection()

    order = "DESC" if descending else "ASC"

    rows = connection.execute(f"""
        SELECT * FROM students
        WHERE major LIKE ?
        ORDER BY gpa {order}
    """, (f"%{major}%",)).fetchall()

    connection.close()

    return [
        Student(
            row["student_id"],
            row["name"],
            row["surname"],
            row["email"],
            row["major"],
            row["gpa"]
        )
        for row in rows
    ]

def get_student_statistics():
    connection = get_connection()

    stats = connection.execute("""
        SELECT
            COUNT(*) AS total_students,
            AVG(gpa) AS average_gpa,
            MAX(gpa) AS highest_gpa,
            MIN(gpa) AS lowest_gpa
        FROM students
    """).fetchone()

    connection.close()

    return stats

def get_student_counts_by_major():
    connection = get_connection()

    rows = connection.execute("""
        SELECT major, COUNT(*) AS student_count
        FROM students
        GROUP BY major
        ORDER BY student_count DESC, major ASC
    """).fetchall()

    connection.close()
    return rows
