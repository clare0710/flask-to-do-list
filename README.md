# To-Do List Application

This is a Flask-based to-do list application that uses Bootstrap, PostgreSQL, Docker and Pytest. It allows users to create, read, update, and delete tasks in their own account. Also, receive email notification when there is item expired.

## Project Setup

### Environment Variables
This project requires some environment variables to be set in the .env file. Replace the environment variables with your own values. For the mail password, make sure to generate an app password for gmail and replace the password value with it.

### Create an Environment

To create a virtual environment on Windows, run the following command in the root of the project:
```bash
py -3 -m venv venv
```

To activate the environment, run:
```bash
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Run Tests
Before running the tests, make sure you have activated the virtual environment. Additionally, the tests require a local database to be set up. To run the tests, use:
```bash
pytest
```

## Docker Commands
This project can be run using Docker compose. To build the images, run:
```bash
docker compose build
```

To start the containers, run:
```bash
docker compose up -d
```

To stop the containers, run:
```bash
docker compose down
```
