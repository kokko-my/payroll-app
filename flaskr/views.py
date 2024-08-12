# flaskr/views.py
from flask import (
    Blueprint, render_template, request
)
from flaskr.forms import (
    WorkplaceForm, WorktimeForm
)
from flaskr.utils.time_operation import convert_time_to_float

bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

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
