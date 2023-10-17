from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# # MySQL 연결 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://KIMMINSE:#$aB354354@localhost/autoQA'
db = SQLAlchemy(app)

@app.route('/') # 접속하는 url
def dashboard():
    #users = User.query.all()
    return render_template('dashboard.html', users="Kim", data = {'ID':'km99', 'point':360, 'data':20}) 
  # render_template의 첫번째로 html 파일을, 두번째 매개변수 부터 보낼 데이터를 넣을 수 있다.
  # host 등을 직접 지정하고 싶다면
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
            # 로그인 성공
            return "Login successful!"
        else:
            # 로그인 실패
            return "Login failed!"
    
    return render_template('login.html')


@app.route('/Test',methods=('GET', 'POST')) # 접속하는 url
def index():
    if request.method == "POST":
        # user=request.form['user'] # 전달받은 name이 user인 데이터
        print(request.form.get('user')) # 안전하게 가져오려면 get
        user = request.form.get('user')
        data = {'level': 60, 'point': 360, 'exp': 45000}
        return render_template('index.html', user=user, data=data)
    elif request.method == "GET":
        user = "BAN"
        data = {'level': 60, 'point': 360, 'exp': 45000}
        return render_template('index.html', user=user, data=data)
# GET과 POST 요청에 다르게 응답하는 분기 - 로그인 됐냐 안됐냐에 따라 접근 분기를 정할수도 있을듯?


if __name__ == '__main__':
    app.run()