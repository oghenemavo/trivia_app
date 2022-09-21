import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia'
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
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)
        # self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_delete_question(self):
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 23).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], True)
        self.assertEqual(question, None)
        # self.assertEqual(data['deleted'], 2)
        # self.assertTrue(data['total_books'])
        # self.assertTrue(len(data['books']))

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        # self.assertTrue(len(data['questions']))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()