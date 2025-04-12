
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from models import db, User, Assignment  # make sure Assignment model is in models.py

# ✅ Initialize Flask app FIRST
app = Flask(__name__)

# ✅ Set Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartcampus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# ✅ Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ✅ Init DB
db.init_app(app)

# ✅ Create DB and add initial users
with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(username='teacher1', password='admin', role='teacher'))
        db.session.add(User(username='student1', password='1234', role='student'))
        db.session.commit()

# 🔒 Login Route
@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            if user.role == 'teacher':
                return redirect('/teacher/dashboard')
            elif user.role == 'student':
                return redirect('/student/dashboard')
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)

# 👨‍🏫 Teacher Section
@app.route('/teacher/dashboard')
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

@app.route('/teacher/assignments')
def assignments():
    return render_template('assignment.html')

@app.route('/teacher/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/teacher/test')
def test():
    return render_template('test.html')

@app.route('/teacher/notice')
def notice():
    return render_template('notice.html')

# 🎓 Student Section
@app.route('/student/dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/student/attendance')
def student_attendance():
    return render_template('Attendancs.html') 

@app.route('/student/Assg', methods=['GET', 'POST'])
def student_assignment():
    if request.method == 'POST':
        topic = request.form['topic']
        notes = request.form.get('notes', '')
        file = request.files['file']
        uploaded_by = 'student1'  # Hardcoded for now

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return render_template('student_assignment.html', success=True)

    return render_template('student_assignment.html', success=False)

@app.route('/student/result')
def student_result():
    return render_template('student_result.html')

@app.route('/student/feedback')
def student_feedback():
    return render_template('student_feedback.html')

@app.route('/student/pyment')
def student_pyment():
    return render_template('student_pyment.html')

@app.route('/student/porfile')
def student_porfile():
    return render_template('student_porfile.html')

@app.route('/student/test')
def student_test():
    return render_template('student_test.html')

@app.route('/student/fee')
def student_fee():
    return render_template('student_fee.html')

@app.route('/student/notice')
def student_notice():
    return render_template('student_notice.html')

# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True)


 



