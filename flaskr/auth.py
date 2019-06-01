#BluePrints and Views:
#View function is code you write to respind to requests to app
#Uses patterns to match incoming URL and view handles the request
#View returns data that Flask turns into an outgoing process

#Flask can also generate a URL based on View 

#Blueprint: Used to organize a group of related views and code
#Blueprint is registered with the application instead of 
#directly coding views within the application

import functools

from flask import(
    Blueprint,flash,g,redirect,render_template,
    request,session,url_for
)

from werkzeug.security import check_password_hash,generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')

#creates blueprint named auth
#__name__ stores where it is defined 
#url_prefix will be associated with all URL's passed into blueprint

#When user visits /auth/register URL, 
#register view will return HTML with a form to fill out
#When form is submitted, validate input and show error or 
#create new user and proceed to login page

@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username required'
        elif not password:
            error = 'Password is required'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?',(username,)
        ).fetchone() is not None:
            error = 'User {} is already registered'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username,password) VALUES (?,?)',
                (username,generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')





