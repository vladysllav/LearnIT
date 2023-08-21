# LearnIT Education Platform

This is a Learning Management System (LMS) developed using FastAPI and SQLAlchemy. It provides a platform for course creators to create and manage programming courses, and for students to learn from these courses.

## Installation and Usage

Here's how to get the project up and running on your local machine for development and testing.

### Prerequisites

- Python 3.11
- Poetry (Python dependency management tool)
- PostgreSQL

### Setup

1. Clone this repository:

    ```
    git clone https://github.com/your-username/myapp.git
    ```

2. Navigate to the project directory:

    ```
    cd LearnIT
    ```

3. Install the project dependencies:

    ```
    poetry install
    ```

4. Start the PostgreSQL database. If PostgreSQL is installed on your machine, you can usually start it with a command like:

    ```
    pg_ctl start
    ```

    Make sure to update the `SQLALCHEMY_DATABASE_URL` in `app/core/database.py` with your actual database connection details.

5. Run the application:

    ```
    poetry run uvicorn main:app --reload
    ```

Your application should now be running at `http://localhost:8000`.

## Testing

To run the tests for the application, navigate to the project directory in the terminal and run the following command:

    poetry run pytest