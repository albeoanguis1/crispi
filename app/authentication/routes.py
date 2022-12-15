from forms import UserLoginForm, UserCreationForm, EditProfileForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import UserMixin, login_user
from flask_login import LoginManager

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserCreationForm()
    if request.method == "POST":
        print("POST request made.")
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()
            print(f'A User has been added to the database.\nEmail: {email}\nUsername: {username}\nPassword: {password}')
            flash('Account registered.', 'success')
            return redirect(url_for('auth.signin'))
        else:
            flash('Validation failed. Please try again.', 'error')
    return render_template('sign_up.html', form=form)



@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            print(f'A user tried to login.\nUsername: {username}\nPassword: {password}')

            user = User.query.filter(User.username == username).first()
            print(f'User.username from DB: {user.username}\nUsername from form: {username}')
            
            if user:
                print(check_password_hash(user.password, password))
                # if check_password_hash(user.password, password):
                login_user(user)
                print(f'{username} has logged in!')
                return redirect(url_for('site.home'))

            else:
                print('You do not have access to this content.', '\nauth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form, current_user=current_user)



@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))