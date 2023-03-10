# Importing relevant modules
import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models
from app.models import User, Movie
from sqlalchemy import create_engine
import pandas as pd

class TestCase(unittest.TestCase):
    # Setting up the database and variables necessary for testing
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    # tearDown method to clean up the databse after the tests
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    # A function to test if certain users are added and exist within the User table
    def test_user_exists(self):
        # Adding users to the user table
        alice = User(firstName="Alice", surname="Wonderland", username="AliceInWonderland", emailAddress="alice@example.com", password="RandomPassword")
        bob = User(firstName="Bob", surname="Builder", username="BobTheBuilder", emailAddress="bob@example.com", password="ExtraRandomPassword")
        charlie = User(firstName="Charlie", surname="Chaplin", username="CharlieTheChap", emailAddress="charlie@example.com", password="CrazyPassword")
        db.session.add_all([alice, bob, charlie])
        db.session.commit()

        # Testing if the users exist in the user table
        self.assertTrue(User.query.filter_by(username="AliceInWonderland").first())
        self.assertTrue(User.query.filter_by(username="BobTheBuilder").first())
        self.assertTrue(User.query.filter_by(username="CharlieTheChap").first())
        self.assertFalse(User.query.filter_by(username="DaveTheDude").first())

    # A function to test if the top 100 movies are all exist in the movie table
    def test_entry_count(self):
        # CODE USED TO READ IN THE MOVIES CSV FILE AND ADD THE DATA TO THE MOVIES DATABASE
        with open("app/static/top100movies.csv", 'r') as file:
            data_df = pd.read_csv(file)
        data_df.to_sql('movieTable', con=create_engine('sqlite:///test.db'), index=True, index_label='movieId', if_exists='replace')
        db.session.commit()

        # Query to count the number of entries in the movie table and a check to see if there are 100 entries
        count = Movie.query.count()
        self.assertEqual(count, 100)

if __name__ == '__main__':
    unittest.main()