# flaskr/forms.py
from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField, StringField, IntegerField,
    SelectField, RadioField, PasswordField,
)
from wtforms.validators import DataRequired, Email, EqualTo

# ログインフォーム
class LoginForm(FlaskForm):
    email = StringField(
        'メール: ', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'パスワード: ',
        validators=[DataRequired(),
        EqualTo('confirm_password', message='パスワードが一致しません')]
    )
    submit = SubmitField('ログイン')

# アカウント登録フォーム
class RegisterForm(FlaskForm):
    email = StringField(
        'メール: ', validators=[DataRequired(), Email('メールアドレスが誤っています')]
    )
    password = PasswordField(
        'パスワード: ',
        validators=[DataRequired(),
        EqualTo('confirm_password', message='パスワードが一致しません')]
    )
    confirm_password = PasswordField(
        'パスワード再入力: ', validators=[DataRequired()]
    )
    submit = SubmitField('登録')


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
