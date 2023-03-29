from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in Successfully!', category="success")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Try Again!', category="error")
        else:
            flash('Email doesn\'t exist!', category="error")
    return render_template("login.html",user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash('User Already Exists', category='error')
        elif len(email)<5:
            flash('Enter Valid Email!!' ,category='error')
        elif len(first_name) < 3:
            flash('FirstName Should be Greater than 4 Characters! ' ,category='error')
        elif len(password1) < 7:
            flash(' Password must be atleast 7 Characters ' ,category='error')
        elif password1 != password2:
            flash('Passwords don\'t Match!'  ,category='error')
        else :
            new_user = User(email=email, first_name = first_name, password = generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account Created'  ,category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html",user = current_user)