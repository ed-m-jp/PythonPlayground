# MyFirstPythonApi

# Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation and Setup](#installation-and-setup)
   - [Prerequisites](#prerequisites)
   - [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [ScoreDTO example](#scoresto-example)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## Introduction
MyFirstPythonApi is a Python-based web API focused on managing baseball scores. This project serves as a hands-on learning experience, designed to enhance my skills and understanding of Python, particularly in building and working with APIs.

The API provides a suite of functionalities centered around baseball score management. It allows users to perform a variety of operations such as:
- **Retrieving Scores**: Fetching score details by a specific ID.
- **Creating Scores**: Adding new score entries.
- **Updating Scores**: Modifying existing score data.
- **Deleting Scores**: Removing score entries.
- **Searching Scores**: Looking up scores based on certain criteria.

As a personal journey into Python, this project has been a valuable stepping stone in learning the language and its ecosystem.

## Installation and Setup

### Prerequisites
- Python 3.11 for now, we will make this more flexible later.
- Verify that pip is installed. You can check this by running pip --version in your terminal or command prompt. If pip is not installed, you'll need to install it first. It usually comes bundled with Python.

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone [your-repo-link]
   cd MyFirstPythonApi
   ```

2. To install the project dependencies, run:
   ```bash
   pip install pipenv
   pipenv install
   ```

### Running the Application
To run the application, execute the following command:
```bash
uvicorn app.main:app --reload
```
This command starts the FastAPI server, making the API accessible at http://localhost:8000.

Also you can access the swagger at http://localhost:8000/docs

### ScoreDTO Example
The `ScoreDTO` represents the structure of a baseball score data object. Here is an example of how a `ScoreDTO` might look:

```json
{
  "id": 1,
  "player_name": "John Doe",
  "player_team": "Dream Team",
  "score": 5,
  "match_date": "2023-01-01"
}
```
This example shows a score data transfer object with an ID, player name, player team, score value, and the match date. This structure is typically used in responses for retrieving and creating score entries.

### API Endpoints

#### Get a Score by ID
- **GET /scores/{score_id}**
  - Description: Retrieve a specific baseball score by its ID.
  - Parameters:
    - `score_id` (path): The unique identifier of the score.
  - Responses:
    - `200`: Successful retrieval of the score.
    - `404`: Score not found.
    - `422`: Validation error.

#### Update a Score by ID
- **PATCH /scores/{score_id}**
  - Description: Update an existing baseball score by its ID.
  - Parameters:
    - `score_id` (path): The unique identifier of the score to be updated.
  - Request Body: Score data to update.
  - Responses:
    - `200`: Successful update of the score.
    - `404`: Score not found.
    - `422`: Validation error.

#### Delete a Score by ID
- **DELETE /scores/{score_id}**
  - Description: Delete a specific baseball score by its ID.
  - Parameters:
    - `score_id` (path): The unique identifier of the score to be deleted.
  - Responses:
    - `204`: Successful deletion of the score.
    - `404`: Score not found.
    - `422`: Validation error.

#### Create a New Score
- **POST /scores**
  - Description: Create a new baseball score.
  - Request Body: Details of the score to be created.
  - Responses:
    - `201`: Successful creation of the score.
    - `422`: Validation error.

#### Search Scores
- **GET /scores**
  - Description: Search for baseball scores based on various criteria and return a paginated response.
  - Query Parameters:
    - `min_score`: Minimum score filter (optional).
    - `start_date`: Start date of the range filter (optional).
    - `end_date`: End date of the range filter (optional).
    - `page`: Page number of the results (optional).
    - `page_size`: Number of results per page (optional).
  - Responses:
    - `200`: Successful retrieval of the score list.
    - `422`: Validation error.


### Testing
Coming soon.

### Authors
MAIRE Edward

## Acknowledgments

This project, "MyFirstPythonApi", makes use of several open-source software and libraries. We would like to acknowledge and thank the following:

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- [Uvicorn](https://www.uvicorn.org/): An ASGI web server implementation for Python.
- [SQLAlchemy](https://www.sqlalchemy.org/): The Python SQL toolkit and Object-Relational Mapping (ORM) library.
- [python-dotenv](https://pypi.org/project/python-dotenv/): A Python module that reads key-value pairs from a `.env` file and sets them as environment variables.
- [Flake8](https://flake8.pycqa.org/en/latest/): A tool for style guide enforcement and linting for Python.

Special thanks to the developers and maintainers of these projects for their valuable contributions to the open-source community.
