@app.route('//tfauth', methods=['post','get'])
def authenticate2f():
    if 'secret' not in session:
        flash("please select either one-time pin or google authentication", "reg_error2")
        if session['id']==0:
            return redirect('/authenticate_email')
        else:
            return redirect('/authenticate.html')    
    if not request.form['user_pin']:
        flash("Please enter a valid pin", "reg_error2")
        if session['id']==0:
            return redirect('/authenticate_email')
        else:
            return render_template('authenticate.html')

    user_pin = request.form['user_pin']
    token = Authenticator()
    token.setSecret(session['secret'])
    if 'pin' in session:
        token.setInterval(600)
    else:
        token.setInterval(30)
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
    print(session)
    if session['id']==0:
        return redirect('/authenticate_email')
    else:
        print("SHOULD Hhave")
        return render_template('authenticate.html')