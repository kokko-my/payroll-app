# flaskr/forms.py
from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField, StringField, IntegerField,
    SelectField, RadioField,
)
from wtforms.validators import DataRequired


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
