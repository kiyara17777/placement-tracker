from flask import Flask, render_template, request, redirect, url_for
from models import db, Company, Topic, CompanyTopicWeight, PracticeLog
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return "Hello, Placement Tracker is running!"

@app.route('/add-company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        name = request.form['name']
        sector = request.form['sector']
        new_company = Company(name=name, sector=sector)
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for('add_company'))
    
    companies = Company.query.all()
    return render_template('add_company.html', companies=companies)

@app.route('/add-topic', methods=['GET', 'POST'])
def add_topic():
    if request.method == 'POST':
        name = request.form['name']
        new_topic = Topic(name=name)
        db.session.add(new_topic)
        db.session.commit()
        return redirect(url_for('add_topic'))
    
    topics = Topic.query.all()
    return render_template('add_topic.html', topics=topics)

@app.route('/log-practice', methods=['GET', 'POST'])
def log_practice():
    if request.method == 'POST':
        topic_id = request.form['topic_id']
        question_name = request.form['question_name']
        solved = 'solved' in request.form  # checkbox: present if checked
        new_log = PracticeLog(
            topic_id=topic_id,
            question_name=question_name,
            solved=solved,
            date_practiced=date.today()
        )
        db.session.add(new_log)
        db.session.commit()
        return redirect(url_for('log_practice'))
    
    topics = Topic.query.all()
    logs = PracticeLog.query.order_by(PracticeLog.date_practiced.desc()).all()
    return render_template('log_practice.html', topics=topics, logs=logs)

@app.route('/summary')
def summary():
    topics = Topic.query.all()
    summary_data = []
    for topic in topics:
        total = PracticeLog.query.filter_by(topic_id=topic.id).count()
        solved = PracticeLog.query.filter_by(topic_id=topic.id, solved=True).count()
        summary_data.append({
            'topic': topic.name,
            'total': total,
            'solved': solved
        })
    return render_template('summary.html', summary_data=summary_data)

@app.route('/readiness/<int:company_id>')
def readiness(company_id):
    company = Company.query.get_or_404(company_id)
    weights = CompanyTopicWeight.query.filter_by(company_id=company_id).all()
    
    total_score = 0
    breakdown = []
    
    for w in weights:
        topic = w.topic
        total = PracticeLog.query.filter_by(topic_id=topic.id).count()
        solved = PracticeLog.query.filter_by(topic_id=topic.id, solved=True).count()
        coverage = (solved / total) if total > 0 else 0
        total_score += w.weight * coverage
        
        breakdown.append({
            'topic': topic.name,
            'weight': w.weight,
            'coverage': round(coverage * 100, 1),
            'solved': solved,
            'total': total
        })
    
    readiness_score = round(total_score * 100, 2)
    return render_template('readiness.html', company=company, 
                            readiness_score=readiness_score, breakdown=breakdown)

if __name__ == '__main__':
    app.run(debug=True)