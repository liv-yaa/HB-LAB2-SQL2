"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright' # name of database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # For a faster connection to
    # SQL alchemy

    db.app = app # Creating an app attribute on the database instance
    db.init_app(app) # Then, initializing the app connection to the database


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    # db_cursor is the result of the query (results of the query are called "cursors")
    # This has been bound to the method that executeds the query on db.session
    # The QUERY is a constant and it's pased in as the first parameter to that
    # execute function. The second param is a dictionary. 
    # The key is the what we will pass to SQLalchemy, it is equal to :github in the SQL Query above 
    # (: notation is used for SQLAlchemy instead of {{ }} as with Jinja)
    # The value is what the user will input
    db_cursor = db.session.execute(QUERY, {'github': github})

    # row is bound to an item (tuple of 3 items (first name, last name and github)) that is retrieved by applying the SQLAlchemy method fetchone() on our cursor (results from our query), db_cursor
    row = db_cursor.fetchone()

    # print statement by unpacking row through indexing
    # could use f string for this print statement as well
    print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    pass


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    pass


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    pass


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    pass


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
