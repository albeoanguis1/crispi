from forms import UserLoginForm, UserCreationForm, EditProfileForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserCreationForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            print(email, password)

            user = User(email, username, password = password)

            db.session.add(user)
            db.session.commit()



            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)



@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            print(username,password)

            user = User.query.filter(User.username == username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('You do not have access to this content.', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))