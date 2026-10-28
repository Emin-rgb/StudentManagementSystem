from dataclasses import dataclass


@dataclass
class Student:
    student_id: str
    name: str
    surname: str
    email: str
    major: str
    gpa: float