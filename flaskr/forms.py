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
    get_now_month, get_now_day, convert_time_to_float
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
        choices=[(h, str(f'{h:02}')) for h in range(0, 24)], coerce=int
    )
    start_minute = SelectField(
        choices=[(m, str(f'{m:02}')) for m in range(0, 60)], coerce=int
    )
    end_hour = SelectField(
        choices=[(h, str(f'{h:02}')) for h in range(0, 24)], coerce=int
    )
    end_minute = SelectField(
        choices=[(m, str(f'{m:02}')) for m in range(0, 60)], coerce=int
    )
    break_start_hour = SelectField(
        choices=[(h, str(f'{h:02}')) for h in range(0, 24)], coerce=int
    )
    break_start_minute = SelectField(
        choices=[(m, str(f'{m:02}')) for m in range(0, 60)], coerce=int
    )
    break_end_hour = SelectField(
        choices=[(h, str(f'{h:02}')) for h in range(0, 24)], coerce=int
    )
    break_end_minute = SelectField(
        choices=[(m, str(f'{m:02}')) for m in range(0, 60)], coerce=int
    )
    break_radio = RadioField(
        '休憩: ', choices=[('0', 'なし'), ('1', 'あり')], default='0'
    )
    submit = SubmitField('登録')

    def validate(self):
        if not super().validate():
            return False
        # 時間のバリデーション
        start_time = convert_time_to_float(self.start_hour.data, self.start_minute.data)
        end_time = convert_time_to_float(self.end_hour.data, self.end_minute.data)
        break_start_time = convert_time_to_float(self.break_start_hour.data, self.break_start_minute.data)
        break_end_time = convert_time_to_float(self.break_end_hour.data, self.break_end_minute.data)
        if start_time > end_time:
            end_time += 24
        if self.break_radio.data == '1':
            if start_time > break_start_time:
                break_start_time += 24
            if break_start_time > break_end_time:
                break_end_time += 24
            if break_end_time > end_time:
                return False
        return True
