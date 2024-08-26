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
    User, UserWorkplace, UserWorktime
)
from flask_login import (
    login_user, logout_user, current_user,
)
from datetime import date

from flaskr.payroll import *
from flaskr.utils.datetime_operation import *

bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/', methods=['GET'])
@bp.route('/home', methods=['GET'])
def home():
    if not current_user.is_authenticated:
        return render_template('home.html')
    worktimes = current_user.worktime.all()
    total_salary = 0
    for worktime in worktimes:
        workplace = UserWorkplace.select_workplace_by_name(worktime.workplace)
        if workplace is None:
            continue
        salary = calc_total_salary(
            workplace.hourly,
            worktime.start_time,
            worktime.end_time,
            worktime.break_start_time,
            worktime.break_end_time
        )
        total_salary += salary
    return render_template('home.html', worktimes=worktimes, total_salary=total_salary)

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
        work_year = form.work_year.data
        work_month = form.work_month.data
        work_day = form.work_day.data
        start_hour = form.start_hour.data
        start_minute = form.start_minute.data
        end_hour = form.end_hour.data
        end_minute = form.end_minute.data
        break_start_hour = form.break_start_hour.data
        break_start_minute = form.break_start_minute.data
        break_end_hour = form.break_end_hour.data
        break_end_minute = form.break_end_minute.data
        if form.break_radio == '1':
            break_start_hour = break_start_minute = 0
            break_end_hour = break_end_minute = 0

        worktime = UserWorktime(
            user_id = current_user.get_id(),
            workplace = form.workplace.data,
            work_date = date(work_year, work_month, work_day),
            start_time = convert_time_to_float(start_hour, start_minute),
            end_time = convert_time_to_float(end_hour, end_minute),
            break_start_time = convert_time_to_float(break_start_hour, break_start_minute),
            break_end_time = convert_time_to_float(break_end_hour, break_end_minute)
        )
        worktime.create_new_worktime()
        db.session.commit()
        flash('勤務時間を登録しました')
        return redirect(url_for('app.home'))
    elif request.method == 'POST':
        flash('入力に誤りがあります')
    return render_template('worktime.html', form=form)

@bp.route('/deleat_worktime/<int:worktime_id>', methods=['GET'])
def deleat_worktime(worktime_id):
    worktime = UserWorktime.query.get_or_404(worktime_id)
    if worktime.user != current_user:
        abort(403)
    worktime.delete_worktime()
    db.session.commit()
    return redirect(url_for('app.home'))

@bp.route('/edit_worktime/<int:worktime_id>', methods=['GET', 'POST'])
def edit_worktime(worktime_id):
    prev_worktime = UserWorktime.query.get_or_404(worktime_id)
    if prev_worktime.user != current_user:
        abort(403)

    form = WorktimeForm(request.form)
    form.workplace.choices = [(wp.name, wp.name) for wp in current_user.workplaces.all()]
    if request.method == 'GET':
        form.workplace.data = prev_worktime.workplace
        form.work_year.data, form.work_month.data, form.work_day.data = map(int, (prev_worktime.work_date).split('-'))
        form.start_hour.data, form.start_minute.data = convert_float_to_time(prev_worktime.start_time)
        form.end_hour.data,   form.end_minute.data   = convert_float_to_time(prev_worktime.end_time)
        form.break_start_hour.data, form.break_start_minute.data = convert_float_to_time(prev_worktime.break_start_time)
        form.break_end_hour.data,   form.break_end_minute.data   = convert_float_to_time(prev_worktime.break_end_time)
        if prev_worktime.break_start_time == 0 and prev_worktime.break_end_time == 0:
            form.break_radio.data = '0'
        else:
            form.break_radio.data = '1'
    elif request.method == 'POST' and form.validate():
        work_year = form.work_year.data
        work_month = form.work_month.data
        work_day = form.work_day.data
        start_hour = form.start_hour.data
        start_minute = form.start_minute.data
        end_hour = form.end_hour.data
        end_minute = form.end_minute.data
        break_start_hour = form.break_start_hour.data
        break_start_minute = form.break_start_minute.data
        break_end_hour = form.break_end_hour.data
        break_end_minute = form.break_end_minute.data
        if form.break_radio.data == '0':
            break_start_hour = break_start_minute = 0
            break_end_hour = break_end_minute = 0

        new_worktime = UserWorktime(
            user_id = current_user.get_id(),
            workplace = form.workplace.data,
            work_date = date(work_year, work_month, work_day),
            start_time = convert_time_to_float(start_hour, start_minute),
            end_time = convert_time_to_float(end_hour, end_minute),
            break_start_time = convert_time_to_float(break_start_hour, break_start_minute),
            break_end_time = convert_time_to_float(break_end_hour, break_end_minute)
        )
        prev_worktime.delete_worktime()
        new_worktime.create_new_worktime()
        db.session.commit()
        flash('勤務時間の編集が完了しました')
        return redirect(url_for('app.home'))
    elif request.method == 'POST':
        flash('入力に誤りがあります')
    return render_template('edit_worktime.html', form=form, worktime=prev_worktime)
