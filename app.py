# app.py

import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField, StringField, IntegerField,
    SelectField, RadioField,
)
from wtforms.validators import DataRequired

from payroll import (
    NormalSalary, NightSalary, OvertimeSalary
)

from utils.time_operation import convert_time_to_float

basedir = os.path.abspath(os.path.dirname(__name__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myapp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 勤務先情報登録フォーム
class WorkplaceForm(FlaskForm):
    name = StringField(
        '勤務先の名前: ', validators=[DataRequired()]
    )
    hourly = IntegerField(
        '時給: ', validators=[DataRequired()],
    )
    submit = SubmitField('登録')

# 勤務時間登録フォーム
class WorktimeForm(FlaskForm):
    start_hour = SelectField(
        choices=[h for h in range(0, 24)], coerce=int, validators=[DataRequired()]
    )
    start_minute = SelectField(
        choices=[m for m in range(0, 60)], coerce=int, validators=[DataRequired()]
    )
    end_hour = SelectField(
        choices=[h for h in range(0, 24)], coerce=int, validators=[DataRequired()]
    )
    end_minute = SelectField(
        choices=[m for m in range(0, 60)], coerce=int, validators=[DataRequired()]
    )
    break_start_hour = SelectField(
        choices=[h for h in range(0, 24)], coerce=int, validators=[DataRequired()]
    )
    break_start_minute = SelectField(
        choices=[m for m in range(0, 60)], coerce=int, validators=[DataRequired()]
    )
    break_end_hour = SelectField(
        choices=[h for h in range(0, 24)], coerce=int, validators=[DataRequired()]
    )
    break_end_minute = SelectField(
        choices=[m for m in range(0, 60)], coerce=int, validators=[DataRequired()]
    )
    break_radio = RadioField(
        '休憩: ', choices=[('0', 'なし'), ('1', 'あり')], default='0'
    )
    submit = SubmitField('登録')


@app.route('/', methods=['GET', 'POST'])
def index():
    workplace_form = WorkplaceForm(request.form)
    worktime_form  = WorktimeForm(request.form)
    salary = None
    if request.method == 'POST' and workplace_form.validate() and worktime_form.validate:
        hourly_wage = workplace_form.hourly.data

        start_hour = worktime_form.start_hour.data
        start_minute = worktime_form.start_minute.data
        end_hour = worktime_form.end_hour.data
        end_minute = worktime_form.end_minute.data

        break_start_hour = worktime_form.break_start_hour.data
        break_start_minute = worktime_form.break_start_minute.data
        break_end_hour = worktime_form.break_end_hour.data
        break_end_minute = worktime_form.break_end_minute.data

        start_time = convert_time_to_float(start_hour, start_minute)
        end_time = convert_time_to_float(end_hour, end_minute)
        break_start_time = convert_time_to_float(break_start_hour, break_start_minute)
        break_end_time = convert_time_to_float(break_end_hour, break_end_minute)
        break_time = break_end_time - break_start_time
        if worktime_form.break_radio.data == '0':
            break_start_time = break_end_time = 0
            break_time = 0

        salary = (
            NormalSalary(hourly_wage, start_time, end_time).calc_salary() \
            + NightSalary(hourly_wage, start_time, end_time).calc_salary() \
            + OvertimeSalary(hourly_wage, start_time, end_time).calc_salary(break_time) \
            - (
                NormalSalary(hourly_wage, break_start_time, break_end_time).calc_salary() \
                + NightSalary(hourly_wage, break_start_time, break_end_time).calc_salary()
            )
        )
    return render_template(
        'index.html',
        workplace_form=workplace_form,
        worktime_form=worktime_form,
        salary=salary
    )

if __name__ == '__main__':
    app.run(debug=True)
