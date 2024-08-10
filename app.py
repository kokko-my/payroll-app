# app.py

import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField, StringField, IntegerField, TimeField
)

basedir = os.path.abspath(os.path.dirname(__name__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myapp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 勤務先情報登録フォーム
class WorkplaceForm(FlaskForm):
    name = StringField('勤務先の名前: ')
    hourly = IntegerField('時給: ')
    submit = SubmitField('登録')

# 勤務時間登録フォーム
class WorktimeForm(FlaskForm):
    start_time = TimeField('出勤時刻: ')
    end_time = TimeField('退勤時刻: ')
    submit = SubmitField('登録')


@app.route('/', methods=['GET', 'POST'])
def index():
    workplace_form = WorkplaceForm(request.form)
    worktime_form  = WorktimeForm(request.form)
    return render_template(
        'index.html',
        workplace_form=workplace_form,
        worktime_form=worktime_form
    )

if __name__ == '__main__':
    app.run(debug=True)
