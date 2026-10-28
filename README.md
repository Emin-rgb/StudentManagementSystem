# Student Management System

A command-line Student Management System built with Python and SQLite. The project provides functionality for managing student records, validating student information, and viewing student statistics.

## Features

- Add new students
- View all student records
- Search for students
- Update student information
- Delete student records
- Validate student information
- Prevent duplicate student IDs and email addresses
- Sort students by GPA
- Filter students by major
- Filter and sort students together
- View statistics, including average, highest, and lowest GPA
- Count students by major
- Store student records in an SQLite database

## Technologies

- Python
- SQLite
- Object-oriented programming
- Dataclasses
- Custom exceptions

## Project Structure

- `main.py` — Application entry point
- `app.py` — Command-line menu and user interaction
- `student_service.py` — Business logic and validation
- `database.py` — Database operations and queries
- `models.py` — Student data model
- `exceptions.py` — Custom exceptions
- `students.db` — SQLite database

## How to Run

1. Install Python.
2. Open a terminal in the project directory.
3. Run:

   ```bash
   python main.py
   ```

The application initializes the database and opens the main menu.

## Purpose

This project was created to practice Python programming, database integration, object-oriented design, data validation, and application structure.