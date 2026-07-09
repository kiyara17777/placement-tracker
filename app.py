from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Company, Topic, CompanyTopicWeight, PracticeLog, User
from datetime import date
from company_data import get_suggestion
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-this-to-something-random-later'  # needed for sessions/flash messages

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirects here if not logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash('Username already taken.')
            return redirect(url_for('signup'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def calculate_coverage_with_decay(topic_id):
    """
    Returns a coverage score (0 to 1) where more recent practice
    counts more than older practice.
    """
    logs = PracticeLog.query.filter_by(topic_id=topic_id, user_id=current_user.id).all()  # <-- filtered
    
    if not logs:
        return 0
    
    total_weight = 0
    solved_weight = 0
    
    for log in logs:
        days_ago = (date.today() - log.date_practiced).days
        recency_weight = math.exp(-days_ago / 30)
        total_weight += recency_weight
        if log.solved:
            solved_weight += recency_weight
    
    return solved_weight / total_weight if total_weight > 0 else 0

def get_recommendation(breakdown):
    """
    Takes the already-built breakdown list and returns a plain-English
    suggestion pointing at the single biggest score gap.
    """
    if not breakdown:
        return "Add topic weights for this company to get a recommendation."

    def gap_score(row):
        return row['weight'] * (1 - row['coverage'] / 100)

    weakest = max(breakdown, key=gap_score)
    gap = gap_score(weakest) * 100

    if gap < 2:
        return "You're solidly covered across all weighted topics. Keep maintaining your practice streak."

    return (f"Focus on {weakest['topic']} — it's weighted {weakest['weight']*100:.0f}% "
            f"for this company and you're only at {weakest['coverage']:.0f}% coverage. "
            f"This is your single biggest score gap (costing you ~{gap:.1f} points).")

@app.route('/')
@login_required
def home():
    companies = Company.query.all()
    return render_template('dashboard.html', companies=companies)

from company_data import get_suggestion

@app.route('/add-company', methods=['GET', 'POST'])
@login_required
def add_company():
    if request.method == 'POST':
        name = request.form['name']
        
        suggestion = get_suggestion(name)
        sector = suggestion['sector'] if suggestion else request.form.get('sector', '')
        
        new_company = Company(name=name, sector=sector)
        db.session.add(new_company)
        db.session.commit()
        
        # Auto-create topic weights if this company is in our curated dataset
        if suggestion:
            for topic_name, weight in suggestion['weights'].items():
                topic = Topic.query.filter_by(name=topic_name).first()
                if not topic:
                    topic = Topic(name=topic_name)
                    db.session.add(topic)
                    db.session.commit()
                
                existing = CompanyTopicWeight.query.filter_by(
                    company_id=new_company.id, topic_id=topic.id
                ).first()
                if not existing:
                    weight_entry = CompanyTopicWeight(
                        company_id=new_company.id, topic_id=topic.id, weight=weight
                    )
                    db.session.add(weight_entry)
            db.session.commit()
            flash(f'{name} added with suggested topic weights from our curated dataset!')
        else:
            flash(f'{name} added. No curated data found — add topic weights manually.')
        
        return redirect(url_for('add_company'))
    
    companies = Company.query.all()
    return render_template('add_company.html', companies=companies)

@app.route('/add-topic', methods=['GET', 'POST'])
@login_required
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
@login_required
def log_practice():
    if request.method == 'POST':
        topic_id = request.form['topic_id']
        question_name = request.form['question_name']
        solved = 'solved' in request.form
        new_log = PracticeLog(
            user_id=current_user.id,        # <-- NEW
            topic_id=topic_id,
            question_name=question_name,
            solved=solved,
            date_practiced=date.today()
        )
        db.session.add(new_log)
        db.session.commit()
        return redirect(url_for('log_practice'))
    
    topics = Topic.query.all()
    logs = PracticeLog.query.filter_by(user_id=current_user.id).order_by(PracticeLog.date_practiced.desc()).all()  # <-- filtered
    return render_template('log_practice.html', topics=topics, logs=logs)

@app.route('/set-weights/<int:company_id>', methods=['GET', 'POST'])
@login_required
def set_weights(company_id):
    company = Company.query.get_or_404(company_id)
    topics = Topic.query.all()
    
    if request.method == 'POST':
        # Clear existing weights for this company first
        CompanyTopicWeight.query.filter_by(company_id=company_id).delete()
        
        for topic in topics:
            weight_str = request.form.get(f'weight_{topic.id}', '0')
            weight = float(weight_str) / 100  # form takes percentage, store as decimal
            if weight > 0:
                new_weight = CompanyTopicWeight(company_id=company_id, topic_id=topic.id, weight=weight)
                db.session.add(new_weight)
        
        db.session.commit()
        flash('Topic weights updated!')
        return redirect(url_for('readiness', company_id=company_id))
    
    existing_weights = {w.topic_id: w.weight for w in CompanyTopicWeight.query.filter_by(company_id=company_id).all()}
    return render_template('set_weights.html', company=company, topics=topics, existing_weights=existing_weights)

@app.route('/summary')
@login_required
def summary():
    topics = Topic.query.all()
    summary_data = []
    for topic in topics:
        total = PracticeLog.query.filter_by(topic_id=topic.id, user_id=current_user.id).count()
        solved = PracticeLog.query.filter_by(topic_id=topic.id, user_id=current_user.id, solved=True).count()
        summary_data.append({'topic': topic.name, 'total': total, 'solved': solved})
    return render_template('summary.html', summary_data=summary_data)

@app.route('/readiness/<int:company_id>')
@login_required
def readiness(company_id):
    company = Company.query.get_or_404(company_id)
    weights = CompanyTopicWeight.query.filter_by(company_id=company_id).all()
    
    total_score = 0
    breakdown = []
    
    for w in weights:
        topic = w.topic
        total = PracticeLog.query.filter_by(topic_id=topic.id).count()
        solved = PracticeLog.query.filter_by(topic_id=topic.id, solved=True).count()
        coverage = calculate_coverage_with_decay(topic.id)
        total_score += w.weight * coverage
        
        breakdown.append({
            'topic': topic.name,
            'weight': w.weight,
            'coverage': round(coverage * 100, 1),
            'solved': solved,
            'total': total
        })
    
    readiness_score = round(total_score * 100, 2)
    recommendation = get_recommendation(breakdown)

    return render_template('readiness.html', company=company,
                            readiness_score=readiness_score,
                            breakdown=breakdown,
                            recommendation=recommendation)

@app.route('/leaderboard/<int:company_id>')
@login_required
def leaderboard(company_id):
    company = Company.query.get_or_404(company_id)
    weights = CompanyTopicWeight.query.filter_by(company_id=company_id).all()
    
    all_users = User.query.all()
    rankings = []
    
    for user in all_users:
        total_score = 0
        for w in weights:
            logs = PracticeLog.query.filter_by(topic_id=w.topic_id, user_id=user.id).all()
            if logs:
                total_weight = 0
                solved_weight = 0
                for log in logs:
                    days_ago = (date.today() - log.date_practiced).days
                    recency_weight = math.exp(-days_ago / 30)
                    total_weight += recency_weight
                    if log.solved:
                        solved_weight += recency_weight
                coverage = solved_weight / total_weight if total_weight > 0 else 0
            else:
                coverage = 0
            total_score += w.weight * coverage
        
        score = round(total_score * 100, 2)
        if score > 0:  # only show users who've logged some relevant practice
            rankings.append({'username': user.username, 'score': score})
    
    rankings.sort(key=lambda x: x['score'], reverse=True)
    
    # find current user's rank even if not in top list
    your_rank = next((i+1 for i, r in enumerate(rankings) if r['username'] == current_user.username), None)
    
    return render_template('leaderboard.html', company=company, rankings=rankings, your_rank=your_rank)

if __name__ == '__main__':
    app.run(debug=True)