# Importing relevant modules
from flask import Flask, render_template, flash, request, redirect, url_for, session
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from .forms import RegistrationForm, LoginForm
from .models import Watched, User, Movie
import pandas as pd
import time
import logging

# Adding each of the models to the admin view (for debugging and database management purposes)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Movie, db.session))
admin.add_view(ModelView(Watched, db.session))

# The route for the movies overview page (main page of the application)
@app.route('/', methods=['GET', 'POST'])
def moviesOverview():
    logging.info('moviesOverview accessed')

    # CODE USED TO READ IN THE MOVIES CSV FILE AND ADD THE DATA TO THE MOVIES DATABASE
    # UNCOMMENT TO ADD OR RESET THE DATA IN THE MOVIES TABLE IF ANYTHING GOES WRONG
    # with open("app/static/top100movies.csv", 'r') as file:
    #     data_df = pd.read_csv(file)
    # data_df.to_sql('movieTable', con=create_engine('sqlite:///app.db'), index=True, index_label='movieId', if_exists='replace')
    # db.session.commit()
    # logging.debug('Movies successfully read from CSV file and added to database')

    # Getting all the records from the movie table to be displayed in the html table
    cursor = db.engine.execute('SELECT * FROM movieTable')
    items = cursor.fetchall()
    logging.info('Movies table successfully loaded')

    return render_template('moviesOverview.html', title='Top Movies Tracker', items=items)

# The route for the unwatched movies page
@app.route('/unwatchedMovies', methods=['GET', 'POST'])
@login_required
def unwatchedMovies():
    logging.info('unwatchedMovies accessed')

    # Query used to get the movies that have not been marked as seen
    cursor = db.engine.execute('SELECT mt.movieId, mt.title, mt.description, mt.duration, mt.genre FROM movieTable mt LEFT JOIN watchedTable wt ON wt.movieId = mt.movieId WHERE wt.movieId IS NULL')
    items = cursor.fetchall()
    logging.info('Unwatched table successfully loaded')

    # Sleep function used to wait 1 second to allow time for the 'watched' buttons to update upon being clicked
    time.sleep(1)
    logging.info('Successfully waited for button state change')

    return render_template('unwatchedMovies.html', title='Unwatched Movies', items=items)

# The route for the watched movies page
@app.route('/watchedMovies', methods=['GET', 'POST'])
@login_required
def watchedMovies():
    logging.info('watchedMovies accessed')

    # Query used to get the movies that have been marked as seen
    cursor = db.engine.execute('SELECT mt.movieId, mt.title, mt.description, mt.duration, mt.genre FROM movieTable mt LEFT JOIN watchedTable wt ON wt.movieId = mt.movieId WHERE wt.movieId = mt.movieId')
    items = cursor.fetchall()
    logging.info('Watched table successfully loaded')
    
    return render_template('watchedMovies.html', title='Watched Movies', items=items)

# The route to handle marking movies as seen. It adds a record to the 'watchedTable' and updates the 'watched' field to '1' to reflect this.
@app.route('/flip', methods=['POST'])
@login_required
def flip():
    w = Watched()

    # Getting the movie id and the current user's id
    currentMovieId = request.form["flip"]
    currentUserId = current_user.get_id()

    # Adding a new record / updating the values in the record
    w.userId = currentUserId
    w.movieId = currentMovieId
    w.watched = 1

    # Adding and committing the changes to the database
    db.session.add(w)
    db.session.commit()
    logging.info('Movie successfully marked as viewed')

    return redirect(url_for('unwatchedMovies'))

# The route for the login page
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

# The route for handling post requests on the login page
@app.route('/login', methods=['POST'])
def loginPost():
    form = LoginForm()

    # Getting values from the form
    username = form.loginUsername.data
    password = form.loginPassword.data
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first() # Getting the user specified in the username field

    # If the user doesn't exist or the password is wrong, give a warning
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        logging.warning('User could not login - wrong details')
        return redirect(url_for('login'))

    # Using flask-login to login and remember the user
    login_user(user, remember=remember)
    logging.info('User successfully logged in')

    return redirect(url_for('account'))

# The route for the registration page
@app.route('/registration')
def registration():
    form = RegistrationForm()
    return render_template('registration.html', title='Sign Up', form=form)

# The route for handling post requests on the registration page
@app.route('/registration', methods=['POST'])
def registrationPost():
    form = RegistrationForm()

    # Assigning form data to variables
    firstName = form.forename.data
    surname = form.surname.data
    username = form.username.data
    email = form.email.data
    password = form.password.data

    # Getting the user specified in the form
    user = User.query.filter_by(username=username).first()

    # If the user exists already, display a warning
    if user:
        flash('This username already exists')
        logging.warning('User could not register - Username taken')
        return redirect(url_for('registration'))

    # Assign the data to the User database, with encryption for the password
    newUser = User(firstName=firstName, surname=surname, username=username, emailAddress=email,
                    password=generate_password_hash(password, method='sha256'))

    # Add and commit chnages to the database
    db.session.add(newUser)
    db.session.commit()
    logging.info('User successfully registered')

    return redirect(url_for('login'))

# The route for the account page
@app.route('/account')
@login_required
def account():
    logging.info('account page accessed')
    return render_template('account.html', title='Account',
                            firstName=current_user.firstName,
                            surname=current_user.surname,
                            username=current_user.username,
                            email=current_user.emailAddress)

# The route for logging a user out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    logging.info('User logged out')
    return redirect(url_for('moviesOverview'))

# The route for the page to change the user's password
@app.route('/changePassword')
@login_required
def changePassword():
    form = RegistrationForm()
    return render_template('changePassword.html', title='Change Password', form=form)

# The route for handling post requests on the change password page
@app.route('/changePassword', methods=['POST'])
@login_required
def changePasswordPost():
    form = RegistrationForm()

    # Getting the current user's id and getting the record for that user
    currentUserId = current_user.get_id()
    q = User.query.filter_by(userId=currentUserId).first_or_404()

    # Getting the new password from the form data and encrypting it
    newPassword = form.password.data
    hashedPassword = generate_password_hash(newPassword, method='sha256')
    
    # Updating the password
    q.password = hashedPassword

    # Adding and committing the changes to the database
    db.session.add(q)
    db.session.commit()
    logging.info('User successfully changed password')

    # Logging the user out (so they need to login again with the new password)
    logout_user()
    logging.info('User logged out')

    return redirect(url_for('login'))