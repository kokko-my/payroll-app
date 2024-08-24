# flaskr/forms.py
from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField, StringField, IntegerField,
    SelectField, RadioField, PasswordField,
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, ValidationError
)
from flask_login import current_user
from flaskr.models import User

from flaskr.utils.datetime_operation import (
    get_now_month, get_now_day
)

# ログインフォーム
class LoginForm(FlaskForm):
    email = StringField(
        'メール: ', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'パスワード: ',
        validators=[DataRequired()]
    )
    submit = SubmitField('ログイン')

# アカウント登録フォーム
class RegisterForm(FlaskForm):
    email = StringField(
        'メール: ', validators=[DataRequired(), Email('メールアドレスが誤っています')]
    )
    password = PasswordField(
        'パスワード: ', validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'パスワード再入力: ',
        validators=[DataRequired(), EqualTo('password', message='パスワードが一致しません')]
    )
    submit = SubmitField('登録')

    def validate_email(self, field):
        if User.select_user_by_email(field.data):
            raise ValidationError('このメールアドレスはすでに登録されています')

    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは8文字以上です')

# 勤務先情報登録フォーム
class WorkplaceForm(FlaskForm):
    name = StringField(
        '勤務先の名前: ', validators=[DataRequired()]
    )
    hourly = IntegerField(
        '時給: ', validators=[DataRequired()]
    )
    deadline = SelectField(
        '締日: ', choices=[(d, str(d) + '日') for d in range(1, 31)] + [(31, '月末')],
        coerce=int, validators=[DataRequired()]
    )
    submit = SubmitField('登録')

# 勤務時間登録フォーム
class WorktimeForm(FlaskForm):
    workplace = SelectField(
        '勤務先: ', choices=[]
    )
    work_month = SelectField(
        choices=[(m, str(m)) for m in range(1, 13)], coerce=int, default=get_now_month()
    )
    work_day = SelectField(
        choices=[(d, str(d)) for d in range(1, 31)], coerce=int, default=get_now_day()
    )
    start_hour = SelectField(
        choices=[(h, str(h)) for h in range(0, 24)], coerce=int
    )
    start_minute = SelectField(
        choices=[(m, str(m)) for m in range(0, 60)], coerce=int
    )
    end_hour = SelectField(
        choices=[(h, str(h)) for h in range(0, 24)], coerce=int
    )
    end_minute = SelectField(
        choices=[(m, str(m)) for m in range(0, 60)], coerce=int
    )
    break_start_hour = SelectField(
        choices=[(h, str(h)) for h in range(0, 24)], coerce=int
    )
    break_start_minute = SelectField(
        choices=[(m, str(m)) for m in range(0, 60)], coerce=int
    )
    break_end_hour = SelectField(
        choices=[(h, str(h)) for h in range(0, 24)], coerce=int
    )
    break_end_minute = SelectField(
        choices=[(m, str(m)) for m in range(0, 60)], coerce=int
    )
    break_radio = RadioField(
        '休憩: ', choices=[('0', 'なし'), ('1', 'あり')], default='0'
    )
    submit = SubmitField('登録')
