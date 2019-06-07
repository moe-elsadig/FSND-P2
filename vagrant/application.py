# -*- coding: utf-8 -*-

# Import dependencies
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from database_setup import Base, User, Category, CategoryItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests



app = Flask(__name__)

# Define the name of the application
APPLICATION_NAME = "Catalogue Web App"

# Connect to Database and create a database session
engine = create_engine('sqlite:///catalogue.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalogue/')
@app.route('/categories/')
def showCategories():

    # Obtain a list of the available categories
    categories = session.query(Category).all()

    return render_template('catalogue.html', categories=categories)


@app.route('/catalogue/<int:category_id>/')
def showItems(category_id):

    # Obtain a list of the available categories
    categories = session.query(Category).all()

    # Obtain a list of the selected category's items
    items = session.query(CategoryItem).filter_by(category_id=category_id).all()

    return render_template('catalogue.html', categories=categories, items=items)

@app.route('/catalogue/new/', methods=['POST','GET'])
def newCategory():

    # Check to see if there is a POST request from the interface
    if request.method == 'POST':
        # Create a new category and commit it to the database
        # title: the title entered in the form
        # user_id: use the id of the logged in user
        category = Category(title=request.form['title'], user_id=request.form.get('user_id', 1))
        session.add(category)
        session.commit()

        flash('~*New Category Created')

        return redirect(url_for('showCategories'))

    return render_template('newCategory.html')

@app.route('/catalogue/<int:category_id>/edit/', methods=['POST','GET'])
def editCategory(category_id):

    category = session.query(Category).filter_by(id=category_id).one()

    # Check to see if there is a POST request from the interface
    if request.method == 'POST':
        # Create a new category and commit it to the database
        # title: the title entered in the form
        # user_id: use the id of the logged in user
        category.title = request.form['title']
        session.add(category)
        session.commit()

        flash('~*Category Edited')

        return redirect(url_for('showCategories'))

    return render_template('editCategory.html', category_id=category_id, category=category)



@app.route('/catalogue/<int:category_id>/delete/', methods=['POST','GET'])
def deleteCategory(category_id):

    category = session.query(Category).filter_by(id=category_id).one()

    # Check to see if there is a POST request from the interface
    if request.method == 'POST':
        # Create a new category and commit it to the database
        # title: the title entered in the form
        # user_id: use the id of the logged in user
        session.delete(category)
        session.commit()

        flash('~*Category Deleted')

        return redirect(url_for('showCategories'))

    return render_template('deleteCategory.html', category_id=category_id, category=category)



# Run the app in the localhost on port 8000
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
