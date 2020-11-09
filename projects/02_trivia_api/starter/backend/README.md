# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET '/questions'
POST 'questions'
POST '/quizzes'
GET '/categories/<int:category_id>/questions'
DELETE '/questions/<int:question_id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches all available questions available and displays 10 questions per page.
- Request Arguments: None
- Returns: a list of questions, success value, categories, and total number of questions


 DELETE '/questions/<int:question_id>'
- Deletes a question using the question's id .
- Returns id of deleted question upon success.
{
      "success": True,
      "deleted": 3
}

GET '/categories/<int:category_id>/questions'
- Gets questions by category id.
- Returns JSON object with paginated questions related to the selected category.
{
    "success": True,
    "total_questions": 1,
    "current_category": "History",
    "questions": [
          {
              "answer": "Blood",
              "category": 1,
              "difficulty": 4,
              "id": 22,
              "question": "Hematology is a branch of medicine involving the study of what?"
          }
    ]
}

POST '/questions'
- Searches for questions using a keyword and also creates new questions
- Request Arguments: None
- Returns: Result varies based on if its a create or search request.
Search:
{
      "success" : True,
      "questions": [
          {
              "answer": "Blood",
              "category": 1,
              "difficulty": 4,
              "id": 22,
              "question": "Hematology is a branch of medicine involving the study of what?"
          }
      ]
      "total_questions" : 1
}

Create:
{
    "success" : True
}

POST '/quizzes'
- Enables the quiz to be played by categories
- Uses JSON request parameters of category and previous questions.
- Returns JSON object with up to 5 random questions except the previous questions
{
    "success" : True,
    "question": {
                      "answer": "Edward Scissorhands",
                      "category": 5,
                      "difficulty": 3,
                      "id": 2,
                      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                  },
    "previous_questions": [
                  {
                      "answer": "Lake Victoria",
                      "category": 5,
                      "difficulty": 4,
                      "id": 4,
                      "question": "What is the largest lake in Africa?"
                  },
                  {
                      "answer": "Agra",
                      "category": 4,
                      "difficulty": 2,
                      "id": 10,
                      "question": "The Taj Mahal is located in which Indian city?"
                  },
                   {
                      "answer": "The Palace of Versailles",
                      "category": 2,
                      "difficulty": 4,
                      "id": 8,
                      "question": "In which royal palace would you find the Hall of Mirrors?"
                  }
              ]
}

```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
