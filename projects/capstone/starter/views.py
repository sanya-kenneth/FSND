from flask import Blueprint, request
from auth import requires_auth
from controllers import QuestionController, AnswerController
from flask import current_app as app


question = QuestionController()
answer = AnswerController()


# setup blueprint for app
app_bp = Blueprint('app_bp', __name__)


@app_bp.route('/questions', methods=['POST'])
@requires_auth('add:question')
def add_question():
    return question.add_question()


@app_bp.route('/questions', methods=['GET'])
@requires_auth('read:questions')
def fetch_questions():
    return question.get_questions()


@app_bp.route('/questions/<question_id>', methods=['GET'])
@requires_auth('read:question')
def fetch_question(question_id):
    return question.get_question(question_id)


@app_bp.route('/questions/<question_id>', methods=['PATCH'])
@requires_auth('edit:question')
def patch_question(question_id):
    return question.edit_question(question_id)


@app_bp.route('/questions/<question_id>', methods=['DELETE'])
@requires_auth('delete:question')
def remove_question(question_id):
    return question.delete_question(question_id)


@app_bp.route('/question/<question_id>/answers', methods=['POST'])
@requires_auth('add:answer')
def post_answer(question_id):
    return answer.add_answer(question_id)


@app_bp.route('/question/<question_id>/answers', methods=['GET'])
@requires_auth('read:answers')
def fetch_answers(question_id):
    return answer.get_answers(question_id)


@app_bp.route('/answer/<answer_id>', methods=['GET'])
@requires_auth('read:answer')
def fetch_answer(answer_id):
    return answer.get_answer(answer_id)
