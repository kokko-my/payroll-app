# app.py

import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField, StringField, IntegerField,
    FloatField
)
from wtforms.validators import DataRequired, NumberRange

from payroll import (
    NormalSalary, NightSalary, OvertimeSalary
)

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
        '時給: ', validators=[DataRequired()]
    )
    submit = SubmitField('登録')

# 勤務時間登録フォーム
class WorktimeForm(FlaskForm):
    start_time = FloatField(
        '出勤時刻: ', validators=[DataRequired(), NumberRange(0, 24.0)]
    )
    end_time = FloatField(
        '退勤時刻: ', validators=[DataRequired(), NumberRange(0, 24.0)]
    )
    break_start_time = FloatField(
        '休憩開始時刻: ', validators=[NumberRange(0, 24.0)]
    )
    break_end_time = FloatField(
        '休憩終了時刻: ', validators=[NumberRange(0, 24.0)]
    )
    submit = SubmitField('登録')


@app.route('/', methods=['GET', 'POST'])
def index():
    workplace_form = WorkplaceForm(request.form)
    worktime_form  = WorktimeForm(request.form)
    salary = None
    if request.method == 'POST':
        hourly_wage = workplace_form.hourly.data
        start_time = worktime_form.start_time.data
        end_time = worktime_form.end_time.data
        break_start_time = worktime_form.break_start_time.data
        break_end_time = worktime_form.break_end_time.data
        if break_start_time == None or break_start_time == None:
            break_start_time = break_end_time = 0
        break_time = break_end_time - break_start_time
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
