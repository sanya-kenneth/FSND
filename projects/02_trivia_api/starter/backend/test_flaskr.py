import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}"\
                             .format('postgres', 'psql',
                                     'localhost:5432',
                                     self.database_name)
        setup_db(self.app, self.database_path)

        category = Category(type="sports")
        category.insert()

    def tearDown(self):
        """Executed after reach test"""
        questions = Question.query.all()
        categories = Category.query.all()
        for qtn in questions:
            qtn.delete()
        for category in categories:
            category.delete()

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """
    def test_api_creates_a_question(self):
        data = {
                "question": "what is soccer?",
                "answer": "it is football",
                "category": 1,
                "difficulty": 1
                }
        data = json.dumps(data)
        res = self.client.post('/api/questions', data=data,
                               content_type="application/json")
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(str(res_data['message']), "Question was created")
        self.assertTrue(res_data['success'])
        self.assertEqual(res_data['question']['question'], "what is soccer?")

    def test_api_returns_error_if_a_field_is_missing_on_create_question(self):
        data = {
                "question": "",
                "answer": "it is football",
                "category": 1,
                "difficulty": 1
                }
        data = json.dumps(data)
        res = self.client.post('/api/questions', data=data,
                               content_type="application/json")
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data['message'],
                         "question field is missing a value")
        self.assertFalse(res_data['success'])

    def test_api_gets_questions(self):
        data = {
                "question": "what is soccer?",
                "answer": "it is football",
                "category": 1,
                "difficulty": 1
                }
        data = json.dumps(data)
        self.client.post('/api/questions', data=data,
                         content_type="application/json")
        res = self.client.get('/api/questions')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res_data['questions'], list)
        self.assertEqual(res_data['page'], 1)
        self.assertEqual(res_data['questions'][0]['question'],
                         "what is soccer?")

    def test_api_deletes_questions(self):
        question = Question("what is music?", "Its good sounds", 1, 1)
        question.insert()
        url = '/api/questions/{}/delete'.format(question.id)
        res = self.client.delete(url)
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['message'],
                         "question was deleted successfuly")
        self.assertTrue(res_data['success'])

    def test_api_gets_questions_by_search_term(self):
        data = {
            "question": "what is soccer?",
            "answer": "it is football",
            "category": 1,
            "difficulty": 1
            }
        data = json.dumps(data)
        self.client.post('/api/questions', data=data,
                         content_type="application/json")
        res = self.client.post('/api/search/questions?search=soccer')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['questions'][0]['question'],
                         "what is soccer?")

    def test_api_gets_questions_by_category(self):
        category = Category(type="sports")
        category.insert()
        fetch_url = '/api/categories/{}/questions'.format(category.id)
        data = {
            "question": "what is soccer?",
            "answer": "it is football",
            "category": category.id,
            "difficulty": 1
        }
        data = json.dumps(data)
        self.client.post('/api/questions', data=data,
                         content_type="application/json")
        res = self.client.get(fetch_url)
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(category.id,
                         int(res_data['questions'][0]['category']))
        self.assertEqual(res_data['questions'][0]['question'],
                         "what is soccer?")

    def test_api_gets_question_to_play(self):
        category = Category("entertainment")
        category.insert()
        question = Question("what is music?", "Its good sounds",
                            category.id, 1)
        question.insert()
        question2 = Question("what is a movie?", "It looks good",
                             category.id, 1)
        question2.insert()
        question3 = Question("what is music?", "Its good sounds",
                             category.id, 1)
        question3.insert()
        question4 = Question("what is a game?", "It looks real",
                             category.id, 1)
        question4.insert()

        play_data = {
            "category": str(category.id),
            "previous_questions": [str(question3.question)]
        }
        data = json.dumps(play_data)
        res = self.client.post('/api/questions/play', data=data,
                               content_type="application/json")
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
