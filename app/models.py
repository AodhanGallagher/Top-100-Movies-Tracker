# Importing relevant modules and creating the database schema / template
from app import db
from flask_login import UserMixin

# Association model used to link the movie and user models (as they exist in a many to many relationship)
# An extra column "watched" has been included to indicate if a user has watched a certain movie
class Watched(db.Model):
    __tablename__ = "watchedTable"
    userId = db.Column(db.ForeignKey('userTable.userId'), primary_key=True)
    movieId = db.Column(db.ForeignKey('movieTable.movieId'), primary_key=True)
    watched = db.Column(db.Boolean, nullable=False, default=True)
    movie = db.relationship('Movie', back_populates='parents')
    user = db.relationship('User', back_populates='children')

# User model that is used to store data about each individual user
class User(UserMixin, db.Model):
    __tablename__ = "userTable"
    userId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20))
    surname = db.Column(db.String(25))
    username = db.Column(db.String(20), index=True, unique=True)
    emailAddress = db.Column(db.String(50))
    password = db.Column(db.String(64))
    children = db.relationship('Watched', back_populates='user')

    def get_id(self):
        return (self.userId)

# Movie model that is used to hold data about each movie
class Movie(db.Model):
    __tablename__ = "movieTable"
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True, unique=True)
    description = db.Column(db.String(300))
    duration = db.Column(db.String(8))
    genre = db.Column(db.String(20))
    parents = db.relationship('Watched', back_populates='movie')

    def get_id(self):
        return (self.movieId)
    