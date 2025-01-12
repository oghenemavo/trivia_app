import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

import random
from random import randint


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.username = 'postgres'
        self.password = 'root'
        self.host_address = 'localhost'
        self.port = '5432'
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(self.username, self.password, self.host_address, self.port, self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who invented writing?',
            'answer': 'The Sumerians',
            'category': '1',
            'difficulty': '2'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    # def test_get_categories_failure(self):
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['status'], False)

    def test_get_category_questions(self):
        category_id = '1'
        res = self.client().get('/categories/' + category_id + '/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions'])) 

    def test_get_category_questions_failure(self):
        category_id = '1'
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions_failure(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        questions_list = Question.query.all()
        fetched_questions = [question.format() for question in questions_list]
        question_id = str(fetched_questions[0]['id'])

        res = self.client().delete('/questions/' + question_id)
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question_id is None:
            self.assertEqual(res.status_code, 422)
        else:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['status'], True)
            self.assertEqual(question, None)

    def test_delete_question_failure(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)

    def test_create_new_question_invalid_ep(self):
        res = self.client().post('/questions/50', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    def test_play_quiz(self):
        payload = {
            'previous_questions': [18, 16, 17],
            'quiz_category': 'Science'
        }
        res = self.client().post('/quizzes', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['status'])
    
    def test_play_quiz_invalid_category(self):
        payload = {
            'previous_questions': [18, 16, 17],
            'quiz_category': 'Geography'
        }
        res = self.client().post('/quizzes', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['status'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()