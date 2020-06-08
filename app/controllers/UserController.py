from flask import Blueprint, redirect, url_for, render_template, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.models.Job import Job
from app.models.User import User
from app.forms.LoginForm import LoginForm
from app.forms.RegisterForm import RegisterForm
from app.forms.NewPredictionForm import NewPredictionForm

bp = Blueprint('index', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_one(by={'name': form.name.data})
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index.login'))
        login_user(user, remember=True)
        flash(f"Welcome {user.name}")
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@bp.route('/dashboard')
@login_required
def dashboard():
    jobs = Job.find(by={'user_id': current_user.id})
    form = NewPredictionForm()
    return render_template('dashboard.html', title='Dashboard', jobs=jobs, form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.create(name=form.name.data, password=form.password.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index.login'))
    return render_template('register.html', title='Register', form=form)
