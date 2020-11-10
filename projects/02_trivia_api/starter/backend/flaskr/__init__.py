from __future__ import print_function
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random

import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    """
  @TODO: Set up CORS. Allow '*' for origins.
  Delete the sample route after completing the TODOs
  """

    """
  @TODO: Use the after_request decorator to set Access-Control-Allow
  """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    # Function for handling pagination
    def pagination(request, data):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        question_details = [question.format() for question in data]
        return question_details[start:end]

    """
    @TODO: Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories", methods=["GET"])
    def get_categories():
        try:
            categories = Category.query.all()

            if len(categories) == 0:
                abort(404)

            formatted_categories = {
                category.id: category.type for category in categories
            }

            return jsonify(
                {
                    "success": True,
                    "categories": formatted_categories,
                }
            )

        except BaseException:
            abort(400)

    """
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination
   at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  """

    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        try:
            current_questions = pagination(
                request, Question.query.order_by(Question.id).all()
            )

            categories = Category.query.all()
            formatted_categories = {
                category.id: category.type for category in categories
            }

            if len(current_questions) == 0:
                abort(404)

            return (
                jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                        "categories": formatted_categories,
                        "current_category": None,
                    }
                ),
                200,
            )

        except BaseException:
            abort(400)

    """
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
  the question will be removed.This removal will persist
  in the database and when you refresh the page.
  """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()

            return jsonify({"success": True, "deleted": question_id})

        except BaseException:
            abort(422)

    """
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  """

    @app.route("/questions", methods=["POST"])
    def create_question():
        data = request.json
        if "searchTerm" in data:
            # try:
            searchTerm = data["searchTerm"]
            questions = Question.query.filter(
                Question.question.like(f"%{searchTerm}%")
            ).all()
            question_detail = [question.format() for question in questions]

            if len(questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": question_detail,
                    "total_questions": len(question_detail),
                    "current_category": None,
                }
            )
        # except:

        try:
            answer = data["answer"]
            question = data["question"]
            difficulty = data["difficulty"]
            category = data["category"]

            new_question = Question(question, answer, category, difficulty)
            new_question.insert()

            return jsonify(
                {
                    "success": True,
                }
            )

        except BaseException:
            abort(400)

    """
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  """

    @app.route("/questions", methods=["POST"])
    def search_question():
        try:
            data = request.json
            searchTerm = data["searchTerm"]
            questions = Question.query.filter(
                Question.question.like(searchTerm)).all()

            return jsonify({"success": True, "question": questions})
        except BaseException:
            abort(400)

    """
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  """

    #   #print(category_details[0]['type'], file=sys.stderr)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def retrieve_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            question_detail = [question.format() for question in questions]

            current_category = Category.query.get(category_id)

            if len(question_detail) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": question_detail,
                    "total_questions": len(question_detail),
                    "current_category": current_category.type,
                }
            )
        except BaseException:
            abort(400)

    """
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  """

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        data = request.json
        category_id = data["quiz_category"]["id"]
        prev_questions = data["previous_questions"]

        try:
            if category_id == 0:
                questions = Question.query.order_by(func.random()).all()

            else:
                questions = (
                    Question.query.order_by(func.random())
                    .filter(Question.category == category_id)
                    .all()
                )

            current_question = None

            for question in questions:
                if question.id not in prev_questions:
                    current_question = question.format()
                    prev_questions.append(current_question)
                    break

            return jsonify(
                {
                    "success": True,
                    "previous_questions": prev_questions,
                    "question": current_question,
                }
            )

        except BaseException:
            abort(400)

    """
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  """

    @app.errorhandler(404)
    def page_not_found(error):
        return (
            jsonify({"success": False,
                     "error": 404,
                     "message": "Page not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(e):
        return (
            jsonify(
                {"success": False,
                 "error": 422,
                 "message": "Unprocessable Entity"}
            ),
            422,
        )

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"success": False, "error": 400,
                        "message": "Bad Request"}), 400

    return app
