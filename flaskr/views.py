# flaskr/views.py
from flask import (
    Blueprint, render_template, redirect, url_for, flash,
    request, abort
)
from flaskr import db
from flaskr.forms import (
    LoginForm, RegisterForm, WorkplaceForm, WorktimeForm
)
from flaskr.models import (
    User, PasswordResetToken, UserWorkplace, UserWorktime
)
from flask_login import (
    login_user, logout_user, current_user,
)
from datetime import date
from flaskr.utils.datetime_operation import *

bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/', methods=['GET'])
@bp.route('/home', methods=['GET'])
def home():
    print(dir(current_user))
    worktimes = current_user.worktime.all()
    return render_template('home.html', worktimes=worktimes)

@bp.route('logout')
def logout():
    logout_user()
    return redirect(url_for('app.home'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_user_by_email(form.email.data)
        if user and user.is_active and user.validate_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next:
                next = url_for('app.home')
            return redirect(next)
        elif not user:
            flash('存在しないユーザです')
        elif not user.is_active:
            flash('無効なユーザです。パスワードを再設定してください')
        elif not user.validate_password(form.password.data):
            flash('メールアドレスとパスワードの組み合わせが誤っています')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.email.data)
        user.save_new_password(form.password.data)
        user.create_new_user()
        db.session.commit()
        flash('アカウントを登録しました。')
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)

@bp.route('/workplace', methods=['GET', 'POST'])
def workplace():
    workplaces = current_user.workplaces.all()
    return render_template('workplace.html', workplaces=workplaces)

@bp.route('/regist_workplace', methods=['GET', 'POST'])
def regist_workplace():
    form = WorkplaceForm(request.form)
    if request.method == 'POST' and form.validate():
        workplace = UserWorkplace(
            user_id = current_user.get_id(),
            name = form.name.data,
            deadline = form.deadline.data,
            hourly = form.hourly.data
        )
        workplace.create_new_workplace()
        db.session.commit()
        flash('勤務先を登録しました')
        return redirect(url_for('app.workplace'))
    return render_template('regist_workplace.html', form=form)

@bp.route('/deleat_workplace/<int:workplace_id>', methods=['GET'])
def deleat_workplace(workplace_id):
    workplace = UserWorkplace.query.get_or_404(workplace_id)
    if workplace.user != current_user:
        abort(403)
    db.session.delete(workplace)
    db.session.commit()
    return redirect(url_for('app.workplace'))

@bp.route('/worktime', methods=['GET', 'POST'])
def worktime():
    form = WorktimeForm(request.form)
    form.workplace.choices = [(wp.name, wp.name) for wp in current_user.workplaces.all()]
    if request.method == 'POST' and form.validate():
        start_month = form.start_month.data
        end_month = form.end_month.data
        start_day = form.start_day.data
        end_day = form.end_day.data
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

        # 時間のバリデーション
        if start_time > end_time:
            end_time += 24
        if end_time - start_time > 24:
            flash(f'時間に誤りがあります。（{start_time}->{end_time}）')
            return render_template('worktime.html', form=form)
        if form.break_radio.data == '1':
            if start_time > break_start_time:
                break_start_time += 24
            if break_start_time > break_end_time:
                break_end_time += 24
            if break_end_time > end_time:
                flash(f'時間に誤りがあります。（{start_time}->{end_time}）')
                return render_template('worktime.html', form=form)

        # 日付のバリデーション
        end_time = convert_time_to_float(end_hour, end_minute)
        if start_month > end_month:
            if not (start_month == 12 and end_month == 1):
                flash('日付に誤りがあります。')
                return render_template('worktime.html', form=form)
        if start_day > end_day:
            if not (start_day == get_days_in_month(start_month) and end_day == 1):
                flash('日付に誤りがあります。')
                return render_template('worktime.html', form=form)
        elif end_day - start_day > 1:
            flash('日付に誤りがあります。')
            return render_template('workplace.html', form=form)
        elif start_day == end_day:
            if start_time > end_time:
                flash('時間に誤りがあります。')
                return render_template('worktime.html', form=form)
        else:
            if start_time < end_day:
                flash('時間に誤りがあります。')
                return render_template('worktime.html', form=form)

        end_time = convert_time_to_float(end_hour, end_minute)
        worktime = UserWorktime(
            user_id = current_user.get_id(),
            workplace = form.workplace.data,
            start_date = date(get_now_year(), start_month, start_day),
            end_date = date(get_now_year(), end_month, end_day),
            start_time = start_time,
            end_time = end_time,
            break_start_time = break_start_time,
            break_end_time = break_end_time
        )
        worktime.create_new_worktime()
        db.session.commit()
        flash('勤務時間を登録しました')
        return redirect(url_for('app.home'))
    return render_template('worktime.html', form=form)
