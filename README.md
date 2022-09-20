# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 


### Endpoints 
#### GET /categories
- General:
    - Returns a list of categories objects, status value
    
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "data": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    }
  ],
  "message": "Fetched Categories Successfully",
  "status": true
}
```

#### GET /questions
- General:
    - Returns a list of questions objects, status value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
    
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
  {
  "data": {
    "categories": [
      {
        "id": 1,
        "type": "Science"
      },
      {
        "id": 2,
        "type": "Art"
      }
    ],
    "questions": [
      {
        "answer": "The Sumerians",
        "category": 1,
        "difficulty": 2,
        "id": 26,
        "question": "Who invented writing?"
      }
    ],
    "total_questions": 1
  },
  "message": "Fetched Questions Successfully",
  "status": true
}
}
```

#### GET /categories/{category_id}/questions
- General:
    - Returns a list of questions objects, status value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
    
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

``` {
  "data": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "message": "Fetched Questions Successfully",
  "status": true
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, difficulty and category. Returns the id of the created book, status value to update the frontend. 
- `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{
    "question": "Who invented writing?",
    "answer": "The Sumerians",
    "category": "1",
    "difficulty": "2"
}'`
```
{
  "data": {
    "answer": "The Sumerians",
    "category": 1,
    "difficulty": 2,
    "id": 27,
    "question": "Who invented writing?"
  },
  "message": "New Question added successfully",
  "status": true
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, status value, and question list. 
- `curl -X DELETE http://127.0.0.1:5000/questions/16`
```
{
  
  "data": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
  ],
  "deleted": 24,
  "success": true
}
```


## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
