from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db, User
from formwtf import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/')
def home():
    return redirect(url_for('auth.register'))

@auth.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(name= form.name.data, email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash(f"Welcome, {user.name}!", "success")
            return redirect(url_for("notes.dashboard"))
        flash("Invalid login credentials", "danger")
    return render_template("login.html", form=form)


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out", "info")
    return redirect(url_for('auth.login'))