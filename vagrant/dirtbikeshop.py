from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dirtbike_setup import Base, Manufacture, Bikes, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Dirt Bike Shop"

engine = create_engine('sqlite:///dirtbike.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# login page
@app.route('/login')
def loginPage():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# google plus login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user \
        is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['id'] = data['id']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; \
    border-radius: 150px; -webkit-border-radius: 150px;-\
    moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Function
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Google disconnect code
@app.route('/signout')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current usernot connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['credentials']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print result
    if result['status'] == '200':
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(\
        'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# API Endpoint for manufacture(GET Request)
@app.route('/dirtbikes/<int:manufacture_id>/dets/JSON')
def bikeByManufactureJSON(manufacture_id):
    manufacture = session.query(Manufacture).filter_by(id=manufacture_id).one()
    bikes = session.query(Bikes).filter_by(manufacture_id=manufacture_id).all()
    return jsonify(Bikes=[b.serialize for b in bikes])


# API endpoint for a single bike
@app.route('/dirtbikes/dets/<int:bikes_id>/JSON/')
def singleBikeJSON(bikes_id):
    bikes = session.query(Bikes).filter_by(id=bikes_id).one()
    return jsonify(bikes=bikes.serialize)


# home page
@app.route('/')
@app.route('/dirtbikes/')
def manufacturePage():
    manufacture = session.query(Manufacture).all()
    if 'username' not in login_session:
        return render_template('publicmanufacturelist.html',
                               manufacture=manufacture)
    else:
        return render_template('manufacturelist.html', manufacture=manufacture)


# Add a new manufacture
@app.route('/dirtbikes/new/', methods=['GET', 'POST'])
def newManufacture():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newManufacture = Manufacture(name=request.form['name'],
                                     user_id=login_session['user_id'])
        session.add(newManufacture)
        session.commit()
        flash('New Manufacture %s has been added' % newManufacture.name)
        return redirect(url_for('manufacturePage'))
    else:
        return render_template('newmanufacture.html')


# Edit a your manufacture page
@app.route('/dirtbikes/<int:manufacture_id>/edit/', methods=['GET', 'POST'])
def editManufacture(manufacture_id):
    editedManufacture = session.query(Manufacture)\
                                    .filter_by(id=manufacture_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedManufacture.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are\
        not authorized to edit this Manufacture. Please create\
        your own Manufacture to edit.')\
        ;}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedManufacture.name = request.form['name']
            flash('Manufacture Successfully edited %s'
                  % editedManufacture.name)
            return redirect(url_for('manufacturePage'))
    else:
        return render_template('editmanufacture.html',
                               manufacture=editedManufacture)


# Delete your manufacture page
@app.route('/dirtbikes/<int:manufacture_id>/delete/', methods=['GET', 'POST'])
def deleteManufacture(manufacture_id):
    manufactureToDelete = session.query(Manufacture)\
                                       .filter_by(id=manufacture_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if manufactureToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert(' \
        You are not authorized to delete this Manufacture.');}\
        </script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(manufactureToDelete)
        flash('%s You have Successfully Deleted' % manufactureToDelete.name)
        session.commit()
        return redirect(url_for('manufacturePage'))
    else:
        return render_template('deletedmanufacture.html',
                               manufacture=manufactureToDelete)


# Bikes by manufacture page
@app.route('/dirtbikes/<int:manufacture_id>/')
@app.route('/dirtbikes/<int:manufacture_id>/bikes/')
def bikeByManufacturePage(manufacture_id):
    manufacture = session.query(Manufacture).filter_by(id=manufacture_id).one()
    creator = getUserInfo(manufacture.user_id)
    bike = session.query(Bikes).filter_by(manufacture_id=manufacture_id)
    if 'username' not in login_session or \
            creator.id != login_session['user_id']:
        return render_template('publicBikesize.html',
                               bike=bike, manufacture=manufacture,
                               creator=creator)
    else:
        return render_template('bikesize.html',
                               manufacture=manufacture, bike=bike,
                               manufacture_id=manufacture_id, creator=creator)


# Create a new bike page
@app.route('/dirtbikes/<int:manufacture_id>/new/', methods=['GET', 'POST'])
def newDirtbike(manufacture_id):
    if 'username' not in login_session:
        return redirect('/login')
    createdBike = session.query(Manufacture).filter_by(id=manufacture_id).one()
    if login_session['user_id'] != createdBike.user_id:
        return "<script>function myFunction() {alert('You are not \
        authorized to create Bikes for this Manufacture.\
        Please create your own Manufacture to \
        create bikes.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newBike = Bikes(
            name=request.form['name'], size=request.form['size'],
            description=request.form['description'],
            price=request.form['price'],
            manufacture_id=manufacture_id, user_id=login_session['user_id'])
        session.add(newBike)
        session.commit()
        flash("You created a new Dirtbike")
        return redirect(url_for('bikeByManufacturePage',
                        manufacture_id=manufacture_id))
    else:
        return render_template('newdirtbike.html',
                               manufacture_id=manufacture_id)


@app.route('/dirtbikes/<int:manufacture_id>/<int:bikes_id>/edit/',
           methods=['GET', 'POST'])
def editDirtbike(manufacture_id, bikes_id):

    editedBike = session.query(Bikes).filter_by(id=bikes_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedBike.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert(\
        'You are not authorized to edit this Bike. \
        Please create your own bike to edit.\
        ');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedBike.name = request.form['name']
        if request.form['size']:
            editedBike.size = request.form['size']
        if request.form['description']:
            editedBike.size = request.form['description']
        if request.form['price']:
            editedBike.price = request.form['price']
        session.add(editedBike)
        session.commit()
        flash("You edited your Dirtbike")
        return redirect(url_for('bikeByManufacturePage',
                        manufacture_id=manufacture_id))
    else:
        return render_template('editdirtbike.html',
                               manufacture_id=manufacture_id,
                               bikes_id=bikes_id, bikes=editedBike)


@app.route('/dirtbikes/<int:manufacture_id>/<int:bikes_id>/delete/',
           methods=['GET', 'POST'])
def deleteDirtbike(manufacture_id, bikes_id):
    bikeToDelete = session.query(Bikes).filter_by(id=bikes_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if bikeToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not \
        authorized to delete this Bike. Please create your own bike to \
        delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(bikeToDelete)
        session.commit()
        flash("You deleted your Dirtbike")
        return redirect(url_for('bikeByManufacturePage',
                        manufacture_id=manufacture_id))
    else:
        return render_template('deletedirtbike.html', bikes=bikeToDelete)


if __name__ == '__main__':
    app.secret_key = 'Code_Life'
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
