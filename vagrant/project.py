# Import dependencies
from flask import Flask, render_template
from flask import session as login_session
from database_setup import Base, User, Category, CategoryItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



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





# Run the app in the localhost on port 8000
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
