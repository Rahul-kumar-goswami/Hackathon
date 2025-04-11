
from flask import Flask, render_template, request, redirect, session, url_for
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/erp_database'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'teacher'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


def require_login():
    allowed_routes = ['login']
    if 'user_id' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))


@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'role' not in session:
#         return redirect('/login')
#     if session['role'] == 'teacher':
#         return render_template('teacher_dashboard.html')
#     elif session['role'] == 'student':
#         attendance = Attendance.query.filter_by(student_id=session['user_id']).all()
#         return render_template('student_dashboard.html', attendance=attendance)
#     return redirect('/login')
@app.route('/dashboard')
def dashboard():
    role = session.get('role')
    if role == 'student':
        return render_template('student_dashboard.html')
    elif role == 'teacher':
        return render_template('teacher_dashboard.html')
    else:
        return "Unauthorized", 403


@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if session.get('role') != 'teacher':
        return 'Unauthorized', 403
    student_id = request.form['student_id']
    new_attendance = Attendance(student_id=student_id)
    db.session.add(new_attendance)
    db.session.commit()
    return redirect('/dashboard')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/login')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/assignments')
def assignments():
    return render_template('assignment.html')
@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    # yahan backend logic aayega - filhaal hum log sirf form ka data capture karenge
    class_name = request.form['class_name']
    date = request.form['date']
    student_name = request.form['student_name']
    status = request.form['status']
    
    # yeh sab print ho raha hai console me, future me DB me save kar sakte ho
    print(f"📌 Attendance: {class_name} | {date} | {student_name} - {status}")
    
    return redirect(url_for('attendance'))
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/submit_test', methods=['POST'])
def submit_test():
    title = request.form['title']
    subject = request.form['subject']
    class_name = request.form['class_name']
    date = request.form['date']
    file = request.files['file']

    # Temporary handling (you can save it as needed)
    print(f"[TEST] {title} | {subject} | {class_name} | {date} | File: {file.filename}")

    return redirect(url_for('test'))
@app.route('/notice')
def notice():
    return render_template('notice.html')

@app.route('/submit_notice', methods=['POST'])
def submit_notice():
    recipient = request.form['recipient']
    subject = request.form['subject']
    message = request.form['message']

    print(f"[NOTICE] To: {recipient} | Subject: {subject}\nMessage: {message}")

    return redirect(url_for('notice'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
