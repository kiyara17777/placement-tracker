from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    weight = db.Column(db.Float, nullable=False)  # e.g. 0.4 = 40%

    company = db.relationship('Company', backref='topic_weights')
    topic = db.relationship('Topic', backref='company_weights')


class PracticeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    question_name = db.Column(db.String(200), nullable=False)
    solved = db.Column(db.Boolean, default=False)
    date_practiced = db.Column(db.Date, default=db.func.current_date())

    topic = db.relationship('Topic', backref='practice_logs')