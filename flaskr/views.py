# flaskr/views.py
from flask import (
    Blueprint, render_template, redirect, url_for, flash,
    request
)
from flaskr import db
from flaskr.forms import (
    LoginForm, RegisterForm, WorkplaceForm, WorktimeForm
)
from flaskr.models import (
    User, PasswordResetToken,
)
from flask_login import (
    login_user, logout_user
)
from flaskr.utils.time_operation import convert_time_to_float

bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/', methods=['GET'])
@bp.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@bp.route('logout')
def logout():
    logout_user()
    return redirect(url_for('app.home'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_user_by_email(form.email.data)
        if user and user.is_active:
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next:
                next = url_for('app.home')
            return redirect(next)
        else:
            flash('存在しないユーザです')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            email = form.email.data,
            password = form.password.data,
        )
        user.create_new_user()
        db.session.commit()
        flash('アカウントを登録しました。')
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)

@bp.route('/workplace', methods=['GET', 'POST'])
def workplace():
    form = WorkplaceForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('workplace.html', form=form)

@bp.route('/worktime', methods=['GET', 'POST'])
def worktime():
    form = WorktimeForm(request.form)
    if request.method == 'POST' and form.validate():
        start_hour = form.start_hour.data
        start_minute = form.start_minute.data
        end_hour = form.end_hour.data
        end_minute = form.end_minute.data

        break_start_hour = form.break_start_hour.data
        break_start_minute = form.break_start_minute.data
        break_end_hour = form.break_end_hour.data
        break_end_minute = form.break_end_minute.data

        start_time = convert_time_to_float(start_hour, start_minute)
        end_time = convert_time_to_float(end_hour, end_minute)
        break_start_time = convert_time_to_float(break_start_hour, break_start_minute)
        break_end_time = convert_time_to_float(break_end_hour, break_end_minute)
        break_time = break_end_time - break_start_time
        if form.break_radio.data == '0':
            break_start_time = break_end_time = 0
            break_time = 0
    return render_template('worktime.html', form=form)
