# Fastapi Blog

|   **Resource**    | **Version** |
|:-----------------:|:-----------:|
|      Python       |   3.11.9    |
|      pipenv       |  2024.0.3   |
|      fastapi      |   0.115.1   |
|       motor       |    3.6.0    |
|     pydantic      |    2.9.2    |
|      uvicorn      |   0.30.6    |
|  email-validator  |    2.2.0    |
|      passlib      |    1.7.4    |
|       pyjwt       |    2.9.0    |
|   python-dotenv   |    1.0.1    |
|      bcrypt       |    4.0.1    |
| python-multipart  |   0.0.10    |

### Run the project

1. pipenv shell
2. uvicorn src.main:app --reload

### Create admin user

python -m src.seed

### Run the tests and generate a coverage report

pytest --cov --cov-report=html

## Run the project from Docker

### Build the Docker image:

sudo docker-compose -f docker/docker-compose.yml build

### Start the containers:

sudo docker-compose -f docker/docker-compose.yml up

### Stop the containers:

sudo docker-compose -f docker/docker-compose.yml down
