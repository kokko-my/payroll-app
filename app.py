# app.py

import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField, StringField, IntegerField,
    SelectField, RadioField,
)
from wtforms.validators import DataRequired
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
        choices=[(h, str(h)) for h in range(0, 24)], coerce=int, validators=[DataRequired()]
    )
    start_minute = SelectField(
        choices=[(m, str(m)) for m in range(0, 60)], coerce=int, validators=[DataRequired()]
    )
    end_hour = SelectField(
        choices=[(h, str(h)) for h in range(0, 24)], coerce=int, validators=[DataRequired()]
    )
    end_minute = SelectField(
        choices=[(m, str(m)) for m in range(0, 60)], coerce=int, validators=[DataRequired()]
    )
    break_start_hour = SelectField(
        choices=[(h, str(h)) for h in range(0, 24)], coerce=int, validators=[DataRequired()]
    )
    break_start_minute = SelectField(
        choices=[(m, str(m)) for m in range(0, 60)], coerce=int, validators=[DataRequired()]
    )
    break_end_hour = SelectField(
        choices=[(h, str(h)) for h in range(0, 24)], coerce=int, validators=[DataRequired()]
    )
    break_end_minute = SelectField(
        choices=[(m, str(m)) for m in range(0, 60)], coerce=int, validators=[DataRequired()]
    )
    break_radio = RadioField(
        '休憩: ', choices=[('0', 'なし'), ('1', 'あり')], default='0'
    )
    submit = SubmitField('登録')


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/workplace', methods=['GET', 'POST'])
def workplace():
    form = WorkplaceForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('workplace.html', form=form)

@app.route('/worktime', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
