from flask import Flask,render_template,request,redirect,url_for,session,flash,Blueprint
from __init__ import config

auth = Blueprint('auth',__name__)
mysql = config()['mysql']


@auth.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND user_password = %s',(email,password,))
        # Fetch one record and return result
        user = cursor.fetchone()
        # If account exists in accounts table in out database
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            # Redirect to home page
            return redirect(url_for('main.home'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('Please check your login details and try again.')
            return render_template('login.html')

    return render_template('login.html')


@auth.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    # Redirect to login page
    return redirect(url_for('main.home'))


@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form \
            and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s',(email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
            return redirect(url_for('auth.register'))

        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO users(username, email, user_password) VALUES (%s, %s, %s)",
                           (username,email,password))
            mysql.connection.commit()

    return redirect(url_for('auth.login'))


