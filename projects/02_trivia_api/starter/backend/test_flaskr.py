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
        self.database_name = "trivia_test"
        self.data={
             'answer' : 'Red',
             'question' : 'What is my favorite color?',
             'difficulty' : 3,
             'category' : 4
        }
        self.search={
             'searchTerm' : 'favorite'
        }
        self.search_400={
             'searchTerm' : 'gift'
        }
        self.quiz={
             'quiz_category' : {
                 'id' : 0
             },
             'previous_questions' : []
        }
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
        self.assertEqual(res.status_code, 200)

    def test_get_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def test_new_question(self):
        res=self.client().post('/questions', json=self.data)
        self.assertEqual(res.status_code, 200)
    
    def test_search_question(self):
        res=self.client().post('/questions', json=self.search)
        self.assertEqual(res.status_code, 200)

    def test_400_search_question(self):
        res=self.client().post('/questions', json=self.search_400)
        self.assertEqual(res.status_code, 404)
    
    def test_get_questions_invalid_page(self):
        res = self.client().get('/questions?page=200')
        self.assertEqual(res.status_code, 400)
    
    def test_delete_question(self):
        res=self.client().delete('/questions/5')
        self.assertEqual(res.status_code, 200)
    
    def test_delete_invalid_question(self):
        res=self.client().delete('/questions/60')
        self.assertEqual(res.status_code, 422)

    def test_quizzes(self):
        res=self.client().post('/quizzes', json=self.quiz)
        self.assertEqual(res.status_code, 200)


    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        self.assertEqual(res.status_code, 200)
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()