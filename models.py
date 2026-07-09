from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(50))

    def __repr__(self):
        return f"<Company {self.name}>"


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Topic {self.name}>"


class CompanyTopicWeight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)

    company = db.relationship('Company', backref='topic_weights')
    topic = db.relationship('Topic', backref='company_weights')


class PracticeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    question_name = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(10), default='Medium')  # NEW: Easy / Medium / Hard
    solved = db.Column(db.Boolean, default=False)
    date_practiced = db.Column(db.Date, default=db.func.current_date())

    topic = db.relationship('Topic', backref='practice_logs')
    user = db.relationship('User', backref='practice_logs')