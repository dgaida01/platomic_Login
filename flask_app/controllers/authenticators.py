from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models.authenticator import Authenticator
from flask_app.models.msg import AutoCom
import pyqrcode
import base64
import io


@app.route('/authenticate/setup')
def onetime():
    token = Authenticator()
    token.setInterval(600)
    # token.setSecret()
    token.setTotp()
    session['secret'] = token.secret
    session['pin'] = token.getpin()
    body = f"please use the following pin to access the site {session['pin']}"
    AutoCom.sendMessage('Temporary Pin', session['email'], body)
    return render_template('authenticate_email.html')

@app.route('/authenticate', methods=['post','get'])
def authenticate():
    if 'secret' not in session:
        flash("Sorry there was an issue with the session please log back in", "reg_error2")
        return redirect('/')   
    if not request.form['user_pin']:
        flash("Please enter a valid pin", "reg_error2")
        return render_template('authenticate_email.html')

    user_pin = request.form['user_pin']
    token = Authenticator()
    token.setSecret(session['secret'])
    token.setInterval(600)
    token.setTotp()
    if user_pin == token.getpin():
        print("I AM ADDING A USER WG/at")
        return redirect ('/user/add_user')
    else:
        flash("Pin did not match please try again")
    
    if 'pin' in session:
        if session['pin']!=token.getpin():
            flash ("pin expired please request new pin or use google authentication","reg_error2")
            session.pop('pin')
            session.pop('secret')
    
    return redirect('/')


@app.route('/authenticate/qr')
def newQRcode():
    token = Authenticator()
    token.setSecret()
    token.setInterval(30)
    session['secret'] = token.secret 
    data = {
        'email': session['email'],
        'id':session['id'],
        'secret':session['secret']
    }
    User.update_secret(data)
    myqrcode = pyqrcode.create(
        f"otpauth://totp/platomic:{session['email']}?secret={token.secret}&issuer=platomic")
    buffer = io.BytesIO()
    myqrcode.png(buffer, scale=8)
    myfile = buffer.getvalue()
    myfile = base64.b64encode(myfile)
    myfile = myfile.decode()
    body = '<img src="data:image/png;base64,{}">'.format(myfile)
    AutoCom.sendMessage('2 factor authentication', session['email'], body)
    return render_template('authenticate.html')


@app.route('/tfauth', methods=['post','get'])
def authenticate2f():
    if 'secret' not in session:
        flash("Sorry there was an issue with the session please log back in", "reg_error2")
        return redirect('/')   
    if not request.form['user_pin']:
        flash("Please enter a valid pin", "reg_error2")
        return render_template('authenticate.html')

    user_pin = request.form['user_pin']
    token = Authenticator()
    res= token.setSecret(session['secret'])
    print(res)
    print(session['secret'])
    token.setInterval(30)
   
    token.setTotp()
    
    if user_pin == token.getpin():
        print("YOU all good to go")
        return redirect ('/')
    else:
        flash("Pin did not match please try again")
    
    # if 'pin' in session:
    #     if session['pin']!=token.getpin():
    #         flash ("pin expired please request new pin or use google authentication","reg_error2")
    #         session.pop('pin')
    #         session.pop('secret')
    print(session)
    return render_template('authenticate.html')




# @app.route('/test')
# def test():
#     print(f"SESSION PIN: {session['pin']}")
#     print(f"SESSION SECRET: {session['secret']}")
#     token = Authenticator()
#     token.setInterval(600)
#     token.setSecret(session['secret'])
#     token.setTotp()
#     print(f"new secret {token.secret}")
#     print(f'new pin {token.getpin()}')
#     return render_template('authenticate_email.html')
