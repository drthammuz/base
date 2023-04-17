from flask import render_template, request, redirect, url_for, flash
from app import app, db, login_manager
from models import User
from forms import LoginForm, RegistrationForm
from flask_login import login_user, login_required, logout_user, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))

        flash('Invalid username or password. Please try again.')

    return render_template('login.html')

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/konto', methods=['GET', 'POST'])
def konto():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already taken, please choose another one.')
        else:
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful')
            return redirect(url_for('konto'))
        
    return render_template('konto.html', form=form)