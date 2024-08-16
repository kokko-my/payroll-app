# flaskr/models.py
from flaskr import db, login_manager
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime, timedelta
from uuid import uuid4

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(
        db.String(128),
        default=generate_password_hash('payrollapp')
    )
    is_active = db.Column(db.Boolean, unique=False, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email):
        self.email = email

    @classmethod
    def select_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def select_user_by_id(cls, id):
        return cls.query.get(id)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def save_new_password(self, new_password):
        self.password = generate_password_hash(new_password)
        self.is_active = True

    def create_new_user(self):
        db.session.add(self)


# パスワードリセット時に利用する
class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(
        db.String(64),
        unique=True,
        index=True,
        server_default=str(uuid4)
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expire_at = db.Column(db.DateTime, default=datetime.now)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, token, user_id, expire_at):
        self.token = token
        self.user_id = user_id
        self.expire_at = expire_at

    @classmethod
    def publish_token(cls, user):
        token = str(uuid4())
        new_token = cls(
            token,
            user.id,
            datetime.now() + timedelta(days=1)
        )
        db.session.add(new_token)
        return token

# 勤務先
class UserWorkplace(db.Model):
    __tablename__ = 'user_workplaces'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user = db.relationship('User', backref=db.backref('workplaces', lazy='dynamic'))
    name = db.Column(db.Text)
    deadline = db.Column(db.Integer)
    hourly = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, name, deadline, hourly):
        self.user_id = user_id
        self.name = name
        self.deadline = deadline
        self.hourly = hourly

    def create_new_workplace(self):
        db.session.add(self)

# 勤務日時
class UserWorktime(db.Model):
    __tablename__ = 'user_worktimes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user = db.relationship('User', backref=db.backref('worktime', lazy='dynamic'))
    workplace = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    start_time = db.Column(db.Float)
    end_time = db.Column(db.Float)
    break_start_time = db.Column(db.Float)
    break_end_time = db.Column(db.Float)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, start_date, end_date, start_time, end_time, break_start_time=0.0, break_end_time=0.0):
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.break_start_time = break_start_time
        self.break_end_time = break_end_time

    def create_new_workplace(self):
        db.session.add(self)
