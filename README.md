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
   
3. Install poetry
   ```
    pip install poetry
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
    

After that you will see the message `Superuser created successfully` if everything went well.

```
LearnIT
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ branches
│  ├─ config
│  ├─ description
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  ├─ sendemail-validate.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  ├─ develop
│  │     │  ├─ fix_add_module
│  │     │  └─ main
│  │     └─ remotes
│  │        └─ origin
│  │           ├─ HEAD
│  │           └─ fix_add_module
│  ├─ objects
│  │  ├─ 1c
│  │  │  └─ 92ddf0ad882f291ed8683a37c22f61985bb181
│  │  ├─ 1f
│  │  │  └─ 28adbdacbbec041eb8c1fa5a09b433b256ab67
│  │  ├─ 4a
│  │  │  └─ e17f78367ac0a29c8d9fc6f173d7ec31f11783
│  │  ├─ 5a
│  │  │  └─ 96f9af24d1868a7656bf123d896fadaa6e21ab
│  │  ├─ a5
│  │  │  └─ d301d9baeae62888cdce82c2b693843f1153d1
│  │  ├─ e0
│  │  │  └─ cceab36bfa73f87ae4d76ca623306962af753d
│  │  ├─ info
│  │  └─ pack
│  │     ├─ pack-64c6d347e368a768e5ff7b5bbb83c3113bde9893.idx
│  │     ├─ pack-64c6d347e368a768e5ff7b5bbb83c3113bde9893.pack
│  │     └─ pack-64c6d347e368a768e5ff7b5bbb83c3113bde9893.rev
│  ├─ packed-refs
│  └─ refs
│     ├─ heads
│     │  ├─ develop
│     │  ├─ fix_add_module
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     ├─ HEAD
│     │     └─ fix_add_module
│     └─ tags
├─ .gitignore
├─ Dockerfile
├─ README.md
├─ alembic
│  ├─ README
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions
│     ├─ 2023_08_21_0936-c62a40b37efb_initial_migration.py
│     ├─ 2023_09_19_1957-1b6d39fe39eb_update_user_table.py
│     ├─ 2023_10_04_2214-33abd766448b_drop_item_table.py
│     ├─ 2023_10_09_1111-5fa539f8775e_add_course_table.py
│     ├─ 2023_11_04_0213-fe78a57f29e6_created_module_model.py
│     ├─ 2023_11_10_2232-194125e44d48_init_invitation_table.py
│     ├─ 2023_11_19_2158-a6e23831dce1_nullable_true_for_invitation_user_id.py
│     └─ 2023_12_01_1123-641446871ae9_lessons.py
├─ alembic.ini
├─ app
│  ├─ __init__.py
│  ├─ api
│  │  ├─ __init__.py
│  │  ├─ auth
│  │  │  ├─ __init__.py
│  │  │  └─ routes.py
│  │  ├─ auth_bearer.py
│  │  ├─ courses
│  │  │  ├─ __init__.py
│  │  │  └─ routes.py
│  │  ├─ routers.py
│  │  ├─ s3.py
│  │  └─ users
│  │     ├─ __init__.py
│  │     └─ routes.py
│  ├─ core
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  └─ security.py
│  ├─ crud
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ crud_course.py
│  │  ├─ crud_lessons.py
│  │  ├─ crud_module.py
│  │  └─ crud_user.py
│  ├─ db
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ base_class.py
│  │  └─ session.py
│  ├─ dependencies
│  │  ├─ base.py
│  │  ├─ course.py
│  │  ├─ lessons.py
│  │  └─ users.py
│  ├─ filters.py
│  ├─ main.py
│  ├─ models
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ course.py
│  │  ├─ lessons.py
│  │  ├─ module.py
│  │  └─ user.py
│  ├─ repositories
│  │  ├─ base_repository.py
│  │  └─ user_repository.py
│  ├─ schemas
│  │  ├─ __init__.py
│  │  ├─ course.py
│  │  ├─ lessons.py
│  │  ├─ module.py
│  │  ├─ msg.py
│  │  ├─ token.py
│  │  └─ user.py
│  ├─ scripts
│  │  ├─ __init__.py
│  │  └─ superuser.py
│  ├─ services
│  │  ├─ celery.py
│  │  ├─ s3.py
│  │  └─ user_service.py
│  └─ utils.py
├─ docker-compose.yml
├─ pyproject.toml
└─ tests
   └─ __init__.py

```