from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# # MySQL ���� ����
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://KIMMINSE:#$aB354354@localhost/autoQA'
db = SQLAlchemy(app)

@app.route('/') # �����ϴ� url
def dashboard():
    #users = User.query.all()
    return render_template('dashboard.html', users="Kim", data = {'ID':'km99', 'point':360, 'data':20}) 
  # render_template�� ù��°�� html ������, �ι�° �Ű����� ���� ���� �����͸� ���� �� �ִ�.
  # host ���� ���� �����ϰ� �ʹٸ�
  # app.run(host="127.0.0.1", port="5000", debug=True)

#login section
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['ID']
        password = request.form['PASSWORD']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            # �α��� ����
            return "Login successful!"
        else:
            # �α��� ����
            return "Login failed!"
    
    return render_template('login.html')


@app.route('/Test',methods=('GET', 'POST')) # �����ϴ� url
def index():
    if request.method == "POST":
        # user=request.form['user'] # ���޹��� name�� user�� ������
        print(request.form.get('user')) # �����ϰ� ���������� get
        user = request.form.get('user')
        data = {'level': 60, 'point': 360, 'exp': 45000}
        return render_template('index.html', user=user, data=data)
    elif request.method == "GET":
        user = "BAN"
        data = {'level': 60, 'point': 360, 'exp': 45000}
        return render_template('index.html', user=user, data=data)
# GET�� POST ��û�� �ٸ��� �����ϴ� �б� - �α��� �Ƴ� �ȵƳĿ� ���� ���� �б⸦ ���Ҽ��� ������?


if __name__ == '__main__':
    app.run()