import os
import unittest
import json
from models import db
from app import create_app


class CapstoneTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('Testing')
        db.create_all(app=self.app)
        self.client = self.app.test_client()
        self.teacher_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qRXlRVUpDUVRsQ09UQkVNVEZDTWtWR01VWXdPVGRETlVVMk5UQTRRMFZGTlVNMVJqQkROdyJ9.eyJpc3MiOiJodHRwczovL2Rldi16NTdxMGcyYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkwMzcyMjc2Mzg5NTg3MTMzMTEiLCJhdWQiOlsiaHR0cDovLzAuMC4wLjA6ODA4MC8iLCJodHRwczovL2Rldi16NTdxMGcyYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc5Njg4MDEzLCJleHAiOjE1Nzk2OTUyMTMsImF6cCI6IjJnNzc3b2txSlg0QVRucjZvclNKc2NQdmpyU2RPRlpJIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImFkZDpxdWVzdGlvbiIsImRlbGV0ZTpxdWVzdGlvbiIsImVkaXQ6cXVlc3Rpb24iLCJyZWFkOmFuc3dlciIsInJlYWQ6YW5zd2VycyIsInJlYWQ6cXVlc3Rpb24iLCJyZWFkOnF1ZXN0aW9ucyJdfQ.RNX2KgmhalPcZApU5e8ht7gQalArtdU4hT694fdn6UTXFyatHEkkHCVx2Pz6THMSm2TnCwxJkkLC_RKmg91-zvUmqkijIVZsPOCZQiDkRbhNh9whOBkPYdM8ebIGMudZn_yfZCjkHxRyW7FrIT1bp9tjTTkusTqnzBDNvjC4BLV8yko1y8ka36Ubf-bGLXLtkqORjfU2nQP6nW_ncbMvpinkSANKFIqMvTZjXYpPEUgCZoUXkjkrlbmP6vvj2vpegGtFsttYsY3IZZz9KlWox1S4DEDye6lMcNwyoVcQf24koSWv-evI2Lk44D5x_X2fh_k41kZs4jcR8MhDq9Vi2Q'
        self.question = {
                'question': 'What is python?',
                'teacher_id': '12'
            }


    def tearDown(self):
        db.drop_all(app=self.app)
        
    
    def test_api_can_add_question(self):
        response = self.client.post('/questions',
                                      json=self.question,
                                      headers={"Authorization":"Bearer {}".format(self.teacher_token)})
        self.assertEqual(response.status_code, 201)


    def test_api_can_get_questions(self):
        self.client.post('/questions',
                            json=self.question,
                            headers={"Authorization":"Bearer {}".format(self.teacher_token)})
        response = self.client.get('/questions',
                                   headers={"Authorization": "Bearer {}".format(self.teacher_token)})
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"][0]["question"], "What is python?")
        
    
    def test_api_gets_one_question(self):
        self.client.post('/questions',
                            json=self.question,
                            headers={"Authorization":"Bearer {}".format(self.teacher_token)})
        response = self.client.get('/questions/1',
                                   headers={"Authorization": "Bearer {}".format(self.teacher_token)})
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["question"], "What is python?")


    def test_api_can_delete_question(self):
        headers = {"Authorization":"Bearer {}".format(self.teacher_token)}
        self.client.post('/questions', json=self.question, headers=headers)
        r = self.client.delete('/questions/1', headers=headers)
        data = json.loads(r.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Question has been deleted successfuly")
        
        
    def test_returns_error_if_teacher_tries_to_add_an_answer(self):
        headers = {"Authorization":"Bearer {}".format(self.teacher_token)}
        r = self.client.post('/question/1/answers', headers=headers)
        data = json.loads(r.data)
        print(data)
        self.assertEqual(data["error"], "Permission not found.")
