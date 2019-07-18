# -*- coding: utf-8 -*-

# Import dependencies
from flask import Flask, render_template, request, redirect, url_for, flash,\
    jsonify
from flask import session as login_session
from flask import make_response
from database_setup import Base, User, Category, CategoryItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets, GoogleCredentials,\
    OAuth2Credentials
from oauth2client.client import FlowExchangeError
import requests
import random
import string
import httplib2
import json
import requests
from functools import wraps

app = Flask(__name__)

# Define the name of the application
APPLICATION_NAME = "Catalogue Web App"

# Load the client ID from the downloaded google client secret json file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create a database session
engine = create_engine('sqlite:///catalogue.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Check if the user is already logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function

DEBUG_MODE = True

@app.route('/')
@app.route('/catalogue/')
@app.route('/categories/')
def showCategories():

    if DEBUG_MODE:
        login_session['google_user_id'] = "debugging google_user_id"
        login_session['username'] = "debugging username"
        login_session['user_id'] = 1
        login_session['picture'] = None
        login_session['email'] = "m.da7th@gmail.com"
    # try to see if a user is currently logged in and assign a value
    # this will help toggle the login/logout buttons on a page
    if login_session.get('google_user_id'):
        log_user = login_session['google_user_id']
        print("User: " + str(log_user))
    else:
        print("No user is logged in")

    # Obtain a list of the available categories
    categories = session.query(Category).all()

    all_items = session.query(CategoryItem).all()
    all_items = all_items[::-1]
    latest_items = all_items[:18]

    # Check to see if a user is currently logged in to access the correct page
    if 'username' not in login_session:
        return render_template('publicCatalogue.html', categories=categories,
                               latest_items=latest_items)
    else:
        return render_template('catalogue.html', categories=categories,
                               log_in_stat=1, latest_items=latest_items)


# Route to: JSON list of the categories available to the app
@app.route('/categories/JSON')
@app.route('/catalogue/JSON')
def showCategoriesJSON():

    # Obtain a list of the categories available to the app
    categories = session.query(Category).all()

    # Return a JSON version of the list of categories available
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/category/<int:category_id>/')
def showItems(category_id):

    # Obtain a list of the available categories
    categories = session.query(Category).all()

    category = session.query(Category).filter_by(id=category_id).one_or_none()

    # Obtain a list of the selected category's items
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()

    # Check to see if a user is currently logged in to access the page
    if 'username' not in login_session:
        return render_template('publicItems.html', category=category,
                               selected_id=category_id,
                               categories=categories, items=items)
    else:
        return render_template('items.html',
                               category=category,
                               selected_id=category_id,
                               categories=categories, items=items)


# Route to: JSON list of the categories available to the app
@app.route('/category/<int:category_id>/JSON')
def showItemsJSON(category_id):

    # Obtain a list of the categories available to the app
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()

    # Return a JSON version of the list of the items available to a category
    return jsonify(categories=[item.serialize for item in items])


@app.route('/category/new/', methods=['POST', 'GET'])
@login_required
def newCategory():

    # Check to see if there is a POST request from the interface
    if request.method == 'POST':
        # Create a new category and commit it to the database
        # title: the title entered in the form
        # user_id: use the id of the logged in user
        if request.form['title'] != '':

            category = Category(
                title=request.form['title'], user_id=login_session['user_id'])
            session.add(category)
            session.commit()

            # Notify the user
            flash('~*New Category Created')

            return redirect(url_for('showCategories'))
        else:
            flash('a valid input has not been made')
            return render_template('newCategory.html')

    return render_template('newCategory.html')


@app.route('/category/<int:category_id>/edit/', methods=['POST', 'GET'])
@login_required
def editCategory(category_id):

    category = session.query(Category).filter_by(id=category_id).one_or_none()
    creator_id = category.user_id

    # Check if the user is the owner of the category
    if login_session['user_id'] != creator_id:
        # If a wrong user is logged in inform them
        flash("You don't have the permission to do that.")
        return redirect(url_for('showCategories'))

    # Check to see if there is a POST request from the interface
    if request.method == 'POST':
        # Create a new category and commit it to the database
        # title: the title entered in the form
        # user_id: use the id of the logged in user
        category.title = request.form['title']
        session.add(category)
        session.commit()

        # Notfiy the user
        flash('~*Category Edited')

        return redirect(url_for('showCategories'))

    return render_template('editCategory.html', category_id=category_id,
                           category=category)


@app.route('/category/<int:category_id>/delete/', methods=['POST', 'GET'])
@login_required
def deleteCategory(category_id):

    category = session.query(Category).filter_by(id=category_id).one_or_none()
    creator_id = category.user_id

    # Check if the user is the owner of the category
    if login_session['user_id'] != creator_id:
        # If a wrong user is logged in inform them
        flash("You don't have the permission to do that.")
        return redirect(url_for('showCategories'))

    # Check to see if there is a POST request from the interface
    if request.method == 'POST':
        # Create a new category and commit it to the database
        # title: the title entered in the form
        # user_id: use the id of the logged in user
        session.delete(category)
        session.commit()

        # Notify the user
        flash('~*Category Deleted')

        return redirect(url_for('showCategories'))

    return render_template('deleteCategory.html',
                           category_id=category_id, category=category)


@app.route('/category/<int:category_id>/item/<int:item_id>/',
           methods=['POST', 'GET'])
def showItem(category_id, item_id):

    category = session.query(Category).filter_by(id=category_id).one_or_none()

    # Obtain a list of the available categories
    categories = session.query(Category).all()

    # Obtain a list of the selected category's items
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()

    item = session.query(CategoryItem).filter_by(
        id=item_id, category_id=category_id).one_or_none()

    # Check to see if a user is currently logged in to access the page
    if 'username' not in login_session:
        return render_template('publicItem.html', selected_item=category_id,
                               item_id=item_id, category=category, item=item, 
                               categories=categories, items=items)
    else:
        return render_template('item.html', selected_id=category_id,
                               item_id=item_id, category=category, item=item)


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON',
           methods=['POST', 'GET'])
def showItemJSON(category_id, item_id):

    # Obtain a list of the categories available to the app
    item = session.query(CategoryItem).filter_by(
        id=item_id, category_id=category_id).one_or_none()

    # Return a JSON version of the list of categories available
    return jsonify(Item=[item.serialize])


@app.route('/category/<int:category_id>/item/new/', methods=['POST', 'GET'])
@login_required
def newItem(category_id):

    category = session.query(Category).filter_by(id=category_id).one_or_none()
    creator_id = category.user_id

    # Check if the user is the owner of the category
    if login_session['user_id'] != creator_id:
        # If a wrong user is logged in inform them
        flash("You don't have the permission to do that.")
        return redirect(url_for('showCategories'))

    # Check to see if there is a POST request from the interface
    if request.method == 'POST':
        # Create a new item and commit it to the database
        # title: the title entered in the form
        # user_id: use the id of the logged in user
        if request.form['title'] != '' and request.form['description'] != '':

            item = CategoryItem(title=request.form['title'],
                                user_id=login_session['user_id'],
                                category_id=category_id,
                                description=request.form['description'])
            session.add(item)
            session.commit()

            # Notify the user
            flash('~*New Item Created')

            return redirect(url_for('showItems', category_id=category_id))
        else:
            flash('your input was invalid, please try again')
            return render_template('newItem.html', category_id=category_id)

    return render_template('newItem.html', category_id=category_id)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['POST', 'GET'])
@login_required
def editItem(category_id, item_id):

    category = session.query(Category).filter_by(id=category_id).one_or_none()
    item = session.query(CategoryItem).filter_by(
        id=item_id, category_id=category_id).one_or_none()
    creator_id = category.user_id

    # Check if the user is the owner of the category
    if login_session['user_id'] != creator_id:
        # If a wrong user is logged in inform them
        flash("You don't have the permission to do that.")
        return redirect(url_for('showCategories'))

    # Check to see if there is a POST request from the interface
    if request.method == 'POST':
        # Create a new category and commit it to the database
        # title: the title entered in the form
        # user_id: use the id of the logged in user
        if request.form['title']:
            item.title = request.form['title']
        if request.form['description']:
            item.title = request.form['description']

        session.add(category)
        session.commit()

        # Notify the user
        flash('~*Item Edited')

        return redirect(url_for('showItems', category_id=category_id))

    return render_template('editItem.html', category_id=category_id,
                           item_id=item_id, category=category, item=item)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['POST', 'GET'])
@login_required
def deleteItem(category_id, item_id):

    category = session.query(Category).filter_by(id=category_id).one_or_none()
    item = session.query(CategoryItem).\
        filter_by(id=item_id, category_id=category_id).one_or_none()
    creator_id = category.user_id

    # Check if the user is the owner of the category
    if login_session['user_id'] != creator_id:
        # If a wrong user is logged in inform them
        flash("You don't have the permission to do that.")
        return redirect(url_for('showCategories'))

    # Check to see if there is a POST request from the interface
    if request.method == 'POST':

        session.delete(item)
        session.commit()

        # Notify the user
        flash('~*Item Deleted')

        return redirect(url_for('showItems', category_id=category_id))

    return render_template('deleteItem.html', category_id=category_id,
                           item_id=item_id, category=category, item=item)


# Route to: Application login page
@app.route('/login')
def showLogin():

    # Create a local state token to implement an anti-session-forgery check
    # randomise an alphanumeric code to represent the current session
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))

    # assign the state token to the state param of login_session variable
    login_session['state'] = state

    # Render the login Page
    # state: the state token for the current session
    # CLIENT_ID: the client id of the application available in the client\
    # secrets file
    return render_template('login.html', STATE=state, client_ID=CLIENT_ID)


# Route to: CONNECT - for 3rd party login with Google
@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token received from Google against the available token
    if request.args.get('state') != login_session['state']:

        # Create and return a 401 error to the user that the tokens are not\
        # the same
        response = make_response(json.dumps('Invalid state token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # If this request does not have `X-Requested-With` header, this could be\
    # a CSRF
    if not request.headers.get('X-Requested-With'):
        abort(403)

    # Obtain the authorization code received from Google
    code = request.data

    # Try to obtain a credentials object from the authorization code received\
    # from Google
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    # notify the user that a credentials object could not be obtained from\
    # the authorization code provided by the server
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid by using it to make a call to Google
    access_token = credentials.access_token

    # Assemble the url, call Google's servers, and save the result
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Check the resul of the call, if there was an error in the access token\
    # info, abort.
    if result.get('error') is not None:

        # Notify the user of the Google Server error, 500
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # obtain the user id within the credentials object used to make the\
    # connection request
    google_user_id = credentials.id_token['sub']

    # Verify that the access token is used by the intended user
    if result['user_id'] != google_user_id:

        # notify the user that the user id of the request maker and of the\
        # information received don't match
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:

        # notify the user that the id of the client does not match the\
        # application's
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify if there's a stored access token and whether the user id is\
    # already stored, this means the user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_google_user_id = login_session.get('google_user_id')
    if stored_access_token is not None and google_user_id ==\
            stored_google_user_id:

        # notify the user that they're already logged in
        response = make_response(json.dumps('Current user is already \
            connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_user_id'] = google_user_id

    # Assemble the request, Get the user info data
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # Assign the user info data received to the login session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # the return variable containing the final connection/login information\
    # the user will see
    output = ''

    # get the user id associated with email from the database
    user_id = getUserID(login_session['email'])

    # if the user is not in the database
    if not user_id:

        # create a new user and obtain the id
        user_id = createUser(login_session)

        # notify the user that a new account has been created for them
        output += '<h2>A new user account has been created for you with the\
             following information: %s </h2> </br></br></br></br>' % \
            getUserInfo(user_id)

    # update/set the user id of the login session
    login_session['user_id'] = user_id

    # print the login info to the user
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
        -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    # flash a message to the user in the landing page to confirm the login
    flash("you are now logged in as %s" % login_session['username'])

    # return the html code to the login.html page for rendering
    return output


# Route to: DISCONNECT - Revoke a current user's token and reset their\
# login-session with google
@app.route('/gdisconnect/')
def gdisconnect():

    # Obtain the current access token of the login session
    access_token = login_session.get('access_token')

    # If there's no token notify the user that no one is currently connected
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'

        # Redirect the user to the list of categories
        return redirect(url_for('showCategories'))

    # Verify the current login session access token with the Google\
    # server and revoke it
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %\
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # if the token is Successfully revoked, remove the associated local\
    # information
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['google_user_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # build a Successfully disconnected response and code
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'

        # Redirect the user to the list of categories page
        return redirect(url_for('showCategories'))

    # if the token is not succes revoked, inform the user
    else:
        response = make_response(json.dumps('Failed to revoke token for\
             given user.', 400))
        response.headers['Content-Type'] = 'application/json'

        # Redirect the user to the list of categories page
        return redirect(url_for('showCategories'))


# This function is used to create a new user and commit them to the database
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    return newUser.id


# This function is used to get the info of a user from the database
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


# This function is used to get the id of a user if it exists in the database
def getUserID(email):

    if session.query(User).filter_by(email=email).one_or_none():
        user = session.query(User).filter_by(email=email).one_or_none()
        print("User ID is already available")
        return user.id
    else:
        print("User ID is not available")
        return None


# This is currently a debugging function to delete users
def deleteUser(email):
    users = session.query(User).filter_by(email=email).all()
    print (users)
    for user in users:

        session.delete(user)
        session.commit()

    users = session.query(User).filter_by(email=email).all()
    print (users)


# Run the app in the localhost on port 8000
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
