# flaskr/forms.py
from flask_wtf import FlaskForm
from wtforms.fields import (
    SubmitField, StringField, IntegerField,
    SelectField, RadioField, PasswordField,
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, ValidationError,
)
from flask_login import current_user
from flaskr.models import User

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
