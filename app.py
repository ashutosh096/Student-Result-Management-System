from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from models import db, Student
from xhtml2pdf import pisa
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['UPLOAD_FOLDER'] = 'results'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        marks = {
            'Math': int(request.form['math']),
            'Science': int(request.form['science']),
            'English': int(request.form['english'])
        }
        total = sum(marks.values())
        percentage = total / 3

        student = Student(name=name, roll=roll, math=marks['Math'], science=marks['Science'], english=marks['English'], total=total, percentage=percentage)
        db.session.add(student)
        db.session.commit()

        return redirect(f'/result/{student.id}')
    return render_template('index.html')

@app.route('/result/<int:id>')
def result(id):
    student = Student.query.get_or_404(id)
    return render_template('result.html', student=student)

@app.route('/download/<int:id>')
def download(id):
    student = Student.query.get_or_404(id)
    result_html = render_template('result.html', student=student)
    pdf_path = f"results/result_{student.roll}.pdf"
    
    with open(pdf_path, "w+b") as f:
        pisa.CreatePDF(result_html, dest=f)

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('results'):
        os.makedirs('results')
    app.run(debug=True)
