from flask_app import app, session
from flask import redirect, render_template, request
from flask_app.models.user import User
from flask_bcrypt import Bcrypt  # password encryption: pipenv install flask-bcrypt
from flask import flash

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    user = None
    print(session)
    if 'id' in session and session['verified'] ==1:
        data = {'id': session['id']}
        user = User.get_user_by_id(data)
        print(user.use_two_factor)
        if user.use_two_factor == 1:
            return render_template('profile.html', user=user)
    
    return render_template('home.html', user=user)


@app.post('/users/create')
def create_user():
    if not User.is_valid_new_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    session['id'] = 0
    session['verified'] = False
    session['email'] = request.form['email']
    session['password'] =pw_hash
    return redirect('/authenticate/setup')

@app.route('/user/add_user')
def add_user():
    
    data = {
        'email': session['email'],
        'password': session['password']
    }

    session['id'] = User.insert_new_user(data)
    session['verified']=True
    return redirect('/')

@app.post('/users/login')
def login():
    if 'id' in session and session['id']>0:
        return redirect('/')
    
    data = {
        'email': request.form['email'],
    }
    user = User.login(data)
    if not user:
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Login/Password", "login")
        return redirect('/')
    session['id'] = user.id
    session['verified'] = user.verified
    session['email'] = user.email
    session['secret'] = user.secret
    
    print(user.secret)
    if user.use_two_factor==1:
        return render_template('authenticate.html')
    return redirect('/')


# @app.route('/welcome')
# def welcome():
#     if 'id' not in session:
#         return redirect('/')
#     data = {'id': session['id']}
#     user = User.get_user_by_id(data)
#     if not int(user.verified):
#         return render_template('verify.html', user=user)
#     return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

