from flask import request, jsonify, abort, make_response
from models import Question, Answer
from utilities import abort_func, validate_field


class QuestionController:
    def __init__(self):
        pass
                
    def check_question_exists(self, question):
        if not question:
            abort_func(404, "Question not found", False)
        else:
            return question

    def add_question(self):
        data = request.get_json()
        question = data.get("question")
        teacher_id = data.get("teacher_id")
        validate_field(question, "question")
        validate_field(teacher_id, "teacher_id")
        qn = Question.query.filter_by(question=question).first()
        if qn:
            abort_func(400, 
                    f"Question {qn.question}already exists",
                    False)
        qn_obj = Question(question=question, teacher_id=teacher_id)
        qn_obj.save()
        return jsonify({
            "message": "Question was created successfully",
            "success": True
        }), 201

    def edit_question(self, question_id):
        data = request.get_json()
        question = data.get("question")
        teacher_id = data.get("teacher_id")
        qtn = Question.query.filter_by(id=question_id).first()
        self.check_question_exists(qtn)
        if question:
            setattr(qtn, 'question', question)
            qtn.edit()
        if teacher_id:
            setattr(qtn, 'teacher_id', teacher_id)
            qtn.edit()
        return jsonify({
            "message": "update successful",
            "success": True
            }), 202

    def get_questions(self):
        qtns = Question.query.all()
        if not qtns:
            abort_func(404,
                       "There no questions at the moment",
                       False)
        qtns = [qtn.format() for qtn in qtns]
        return jsonify({
            "data": qtns,
            "success": True
        }), 200
        
    def get_question(self, question_id):
        question = Question.query.filter_by(id=question_id).first()
        self.check_question_exists(question)
        question = question.__dict__
        question.pop('_sa_instance_state')
        data = {
            "data": question,
            "success": True
            }
        return data

    def delete_question(self, question_id):
        question = Question.query.filter_by(id=question_id).first()
        self.check_question_exists(question)
        question.delete()
        return jsonify({
            "message": "Question has been deleted successfuly",
            "success": True
        })


class AnswerController:
    def __init__(self):
        pass
    
    def add_answer(self, question_id):
        data = request.get_json()
        answer = data.get('answer')
        student_id = data.get('student_id')
        qtn = Question.query.filter_by(id=question_id).first()
        if not qtn:
            abort_func(404, "Question not found", False)
        validate_field(answer, 'answer')
        validate_field(student_id, 'student_id')
        answer = Answer(answer=answer, student_id=student_id, question_id=qtn.id)
        answer.save()
        return jsonify({
            "message": "Your answer was recorded",
            "success": True
            }), 201
       
    def get_answers(self, question_id):
        answers = Answer.query.all()
        if not answers:
            abort_func(404,
                       "There no answers at the moment",
                       False)
        answers = [answer.format() for answer in answers]
        return jsonify({
            "data": answers,
            "success": True
        }), 200


    def get_answer(self, answer_id):
        answer = Answer.query.filter_by(id=answer_id).first()
        if not answer:
            abort_func(404, "Answer was not found", False)
        answer = answer.__dict__
        answer.pop('_sa_instance_state')
        data = {
            "data": answer,
            "success": True
            }
        return data
