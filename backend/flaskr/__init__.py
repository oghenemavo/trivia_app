import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format()['question'] for question in selection]

    return questions[start:end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    # @cross_origin()
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        data = [category.format() for category in categories]
        return jsonify({
            'status': True,
            'message': 'Fetched Categories Successfully',
            'data': data
        })


    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_questions():
        categories = Category.query.all()
        categories_data = [category.format() for category in categories]

        questions = Question.query.all()
        data = paginate_questions(request, questions)

        return jsonify({
            'status': True,
            'message': 'Fetched Questions Successfully',
            'questions': data,
            'total_questions': len(data),
            'categories': categories_data
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "data": current_question,
                }
            )

        except:
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

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)

        try:
            question = Question(
                category=new_category,
                difficulty=new_difficulty,
                question=new_question,
                answer=new_answer,
            )
            question.insert()

            return jsonify(
                {
                    'status': True,
                    'message': 'New Question added successfully',
                    'data': {
                        'id': question.id,
                        'question': question.question,
                        'answer': question.answer,
                        'category': question.category,
                        'difficulty': question.difficulty
                    }
                }
            )

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()

        search = body.get('search', None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        'status': True,
                        'message': 'Questions fetched Successfully',
                        'data': current_questions,
                    }
                )

            else:
                abort(404)

        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        questions = db.session.query(Question).join(Category, Category.id == Question.category
        ).filter(Question.category == category_id).group_by(Question.id).all()
        data = paginate_questions(request, questions)
        print(data)

        return jsonify({
            'status': True,
            'message': 'Fetched Questions Successfully',
            'data': data
        })

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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({'status': False, 'error': 404, 'message': 'resource not found'}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({'status': False, 'error': 422, 'message': 'unprocessable'}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'status': False, 'error': 400, 'message': 'bad request'}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({'status': False, 'error': 405, 'message': 'method not allowed'}),
            405,
        )

    return app

