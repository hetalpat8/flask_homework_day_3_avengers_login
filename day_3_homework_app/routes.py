# Import the app variable from the init 
from day_3_homework_app import app, db 

# Import specific packages from flask
from flask import render_template,request, redirect, url_for

# Import Our Form(s)**
from day_3_homework_app.forms import UserInfoForm, LoginForm

# Import of Our Model(s) for the Database***
from day_3_homework_app.models import User, Post, check_password_hash

# Import for Flask Login functions - login_required***
#login_user, current_user, logout_user
from flask_login import login_required, login_user, current_user, logout_user

# Default Home Route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fav')
def favRoute():
    avengers = ['Iron Man','Captain America','Hulk','Thor','Spider Man']
    return render_template('fav.html',list_avengers = avengers)

# GET == Gathering Info**
# POST == Sending Info**
@app.route('/register', methods = ['GET', 'POST'])
def register():
    # Init our form**
    form = UserInfoForm()
    # Validation of our form**
    if request.method == 'POST' and form.validate():
        #Get Information from the form**
        name = form.name.data
        phone_number = form.phone_number.data
        email = form.email.data
        password = form.password.data
        #Print the data to the server that comes from the form**
        print(name,phone_number,email,password)

        # Creation/Init of our User Class (aka Model)
        user = User(name,phone_number,email,password)

        # Open a connection to the database
        db.session.add(user)

        # Commit all data to the database
        db.session.commit()
    
    return render_template('register.html',user_form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        # Saving the logged in user to a variable
        logged_user = User.query.filter(User.email == email).first()
        # check the password of the newly found user
        # and validate the password against the hash value
        # inside of the database
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            # TODO Redirected User
            return redirect(url_for('home'))
        else:
            # TODO Redirected User to login route
            return redirect(url_for('login'))
    return render_template('login.html', login_form = form)