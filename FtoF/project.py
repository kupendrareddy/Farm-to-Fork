from flask import Flask, url_for, render_template
from flask import request, redirect, jsonify, flash
from flask import session as login_session
import random, string, os, requests
from flask import send_from_directory, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Crop, Voulent, Farmer, Customer


from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "FarmtoFork.Application"


app =  Flask(__name__)

engine = create_engine('sqlite:///farmerdatabase.db', connect_args ={'check_same_thread':False}, echo = True )

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()

def getvolid(phone):
	try:
		vol_id = session.query(Voulent).filter_by(email = email).first().id
		return cus_id
	except BaseException:
		return None
def getcusid(email):
	try:
		cus_id = session.query(Customer).filter_by(email = email).first().id
		return cus_id
	except BaseException:
		return None

@app.route('/')
@app.route('/home')
def Role():
	flag = 0
	try:
		if login_session['email']:	
			return render_template('home.html', flag = 1)
	except:
		return render_template('home.html')



# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits +
            string.ascii_lowercase) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)




@app.route('/customer/signup', methods=['POST','GET'])
def cus_signup():
	if request.method == 'POST':		
		nam = request.form['fname']+request.form['lname']
		emai = login_session['email']
		phon = request.form['phone']
		aadhaa = request.form['aadhaar']
		addres = request.form['dno']+request.form['city']+request.form['state']
		pincod = request.form['zipcode']
		vol_mobile = request.form['email']
		vol_id = session.query(Voulent).filter_by(email = emai).one().id

		new_vol = Customer(name=nam,email=emai,phone=phon,aadhaar=aadhaa,address=addres,password='1234',
			customer_pic=login_session['picture'],voulenter_id = vol_id, vol_phone = vol_mobile, pincode=pincod)
		session.add(new_vol)
		session.commit()
		flash('New Customer {} has been created'.format(nam))
		return render_template('cus_home.html', cus_id = getcusid(phon))
		# return redirect(url_for('showLogin'))
	else:
		return render_template('cus_signup.html')

# @app.route('/cus/home')
# def cus_home():
	# if login_session['email']:	
	# 	session.commit()
	# 	return render_template('home.html', user_id = getcusid(login_session['email']))
	# else:
	# 	return render_template('home.html')


@app.route('/customer/login', methods=['POST',"GET"])
def cus_login():
	if request.method == 'POST':
		phone = request.form['phone']
		password = request.form['password']
		pwd = session.query(Customer).filter_by(phone = phone).one()
		if pwd.password == password:
			return render_template('cus_home.html',cus_id = getcusid(phone))
		else:
			return render_template('cus_login.html', msg = 'invalid username and password')
	else:
		return render_template('cus_login.html')


@app.route('/voulenter/create', methods=['POST','GET'])
def vol_signup():
	if request.method == 'POST':	
		nam = request.form['fname']+request.form['lname']
		emai = request.form['email']
		phon = request.form['phone']
		passwor = request.form['password']
		aadhaa = request.form['aadhaar']
		addres = request.form['dno']+request.form['city']+request.form['state']
		pincod = request.form['zipcode']
		pic = 'pic'

		new_vol = Voulent(name=nam,email=emai,phone=phon,password=passwor,aadhaar=aadhaa,address=addres,pincode=pincod)
		session.add(new_vol)
		session.commit()
		flash('New Customer {} has been created'.format(nam))
		flash("New Voulenter {} has been created".format(nam))
		return render_template('vol_home.html', v_id= getvolid(phon))
	else:
		return render_template('vol_sign.html')


@app.route('/voulenter/login', methods=['GET','POST'])
def vol_login():
	if request.method == 'POST':
		phone = request.form['phone']
		password = request.form['password']
		print(phone,password)
		pwd = session.query(Voulent).filter_by(phone = phone).one()
		print(pwd)
		if pwd.password == password:
			return render_template('vol_home.html')
		else:
			return render_template('vol_login.html',message = 'invalid username and password')
	else:
		return render_template('vol_login.html')



# # Your Account Sid and Auth Token from twilio.com/console
# # DANGER! This is insecure. See http://twil.io/secure
# account_sid = 'AC25ed0732eac432bd87092497227a4e5c'
# auth_token = 'your_auth_token'
# client = Client(account_sid, auth_token)

# message = client.messages \
#                 .create(
#                      body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                      from_='+15017122661',
#                      to='+15558675310'
#                  )

# print(message.sid)



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
    print('error in g connect is', result.get('error'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        print('in result.get("error")')
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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'
    # see if user exists, if it doesn't make a new one
    user_id = getcusid(login_session['email'])
    # if not user_id:
    # 	output="New User"
    # 	print(output)
    # 	return output

    # login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    b = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % b
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for given user.',400))
        response.headers['Content-Type'] = 'application/json'
        return response



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
