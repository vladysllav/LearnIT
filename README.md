# LearnIT Education Platform

This is a Learning Management System (LMS) developed using FastAPI and SQLAlchemy. It provides a platform for course creators to create and manage programming courses, and for students to learn from these courses.

## Installation and Usage with Docker

Here's how to get the project up and running using docker and docker compose

### Prerequisites

- Docker and docker-compose

### Setup

1. Clone this repository:

    ```
    git clone git@github.com:vladysllav/LearnIT.git
    ```
   
2. Copy .env file and fill environment variables
   ```
   cp .env.example .env
   ```
3. Build docker images:
   ```
   docker compose build
   ```
4. Run docker images
   ```
   docker compose up
   ```
Your application should now be running at `http://localhost:8000`
## Installation and Usage

Here's how to get the project up and running on your local machine for development and testing. First of all you need to install libraries from prerequisites.

### Prerequisites

- Python 3.11
- Poetry (Python dependency management tool)
- PostgreSQL

### Setup

1. Clone this repository:

    ```
    git clone git@github.com:vladysllav/LearnIT.git
    ```

2. Navigate to the project directory:

    ```
    cd LearnIT
    ```

3. Install the project dependencies:

    ```
    poetry install
    ```

4. Then you need to setup your database and set environment variable in .env file with needed data:

    ```
    cp .env.example .env
    ```

    Make sure to **update all environment variables**.
5. Run alembic migrations:
   ```
   alembic upgrade head
   ```
6. Run the application:

    ```
    python -m app.main
    ```

Your application should now be running at `http://localhost:8000`.

### Create a superuser

To create a superuser you need to connect to the docker container and run the script:

    ```
    docker exec -it learnit-web-1 python3 -m app.scripts.superuser <email> <password> <first_name> <last_name>
    ```

After that you will see a message `Superuser created successfully` if everything went well.
