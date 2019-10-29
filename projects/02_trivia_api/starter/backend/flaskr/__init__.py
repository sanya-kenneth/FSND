import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        category_list = [cat.format() for cat in categories]
        return jsonify({'categories': category_list}), 200

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the
    bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        """
        Function gets all questions in the game.
        Returned results are paginated
        """
        page = request.args.get('page', 1, type=int)
        questions = Question.query.all()
        categories = Category.query.all()
        categories_returned = [category.format() for category in categories]
        question_list = [question.format() for question in questions]
        start = (page - 1) * 10
        end = start + 10
        return jsonify({
            'questions': question_list[start:end],
            'page': page,
            'total_questions': len(question_list),
            'categories': categories_returned,
            'current_category': ""
          }), 200

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a
    question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/api/questions/<int:question_id>/delete', methods=['DELETE'])
    def delete_question(question_id):
        """
        Function deletes a question
        args: question_id
        """
        question = Question.query.get_or_404(question_id)
        question.delete()
        return jsonify({'success': True,
                        'message': 'question was deleted successfuly'}), 200

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page of the questions list
    in the "List" tab.
    '''
    @app.route('/api/questions', methods=['POST'])
    def add_question():
        """
        Function adds a question to the game
        """
        data = request.get_json()
        question = data['question']
        answer = data['answer']
        difficulty = data['difficulty']
        category = data['category']
        for key, value in data.items():
            if not value:
                return jsonify({'success': False, 'error': 400,
                                'message': f'{key} field is missing a value'
                                }), 400
        new_question = Question(question, answer, category, difficulty)
        new_question.insert()
        return jsonify({'success': True, 'message': 'Question was created',
                        'question': new_question.format()}), 201

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/api/search/questions', methods=['POST'])
    def search_questions():
        """
        Function performs a search against the Question model.
        If a match is found it is then returned as json data
        """
        search = request.args.get('search', '', type=str)
        questions = Question.query.order_by(Question.id)\
            .filter(Question.question.ilike('%{}%'.format(search)))\
            .all()
        results = [question.format() for question in questions]
        return jsonify({'success': True, 'questions': results}), 200

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/api/categories/<category_id>/questions', methods=['GET'])
    def questions_per_category(category_id):
        """
        Function gets questions per category
        """
        questions = Question.query.filter(Question.category == category_id
                                          ).all()
        results = [question.format() for question in questions]
        return jsonify({'success': True, 'questions': results}), 200

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/api/questions/play', methods=['POST'])
    def get_questions_toplay():
        """
        Functions gets the next question to play
        args: previous_question, category
        """
        data = request.get_json()
        category = data.get('category', 'None')
        previous_questions = data.get('previous_questions', None)
        questions = Question.query.filter(Question.category == category).all()
        all_questions = Question.query.all()
        choice = ''
        if category == 'click':
            # Generate random question when user clicks all option
            choice = Question.query\
                        .filter(~Question.question.in_(previous_questions))\
                        .order_by(func.random()).first()
        else:
            # Generate random question based on given category
            choice = Question.query.filter(Question.category == category)\
                        .filter(~Question.question.in_(previous_questions))\
                        .order_by(func.random()).first()
        if choice:
            choice = choice.format()
        else:
            choice = ""
        return jsonify({'success': True, 'question': choice}), 200

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found_404(error):
        """
        Error handler for all 404 not found errors
        """
        return jsonify({
          'success': False,
          'message': 'Resource not found',
          'error': 404
        }), 404

    @app.errorhandler(400)
    def bad_request_400(error):
        """
        Error handler for all 400 bad request errors
        """
        return jsonify({
          'success': False,
          'message': 'Bad request',
          'error': 400
        }), 400

    @app.errorhandler(422)
    def un_processable_422(error):
        """
        Error handler for all 422 un processable errors
        """
        return jsonify({
          'success': False,
          'message': 'request cannot be processed',
          'error': 422
        }), 422
    return app
