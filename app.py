from pymongo import MongoClient
import jwt
from datetime import datetime
from flask import Flask,request,render_template,redirect,flash,url_for
from flask.json import jsonify
from werkzeug.utils import secure_filename
import requests
import hashlib
import datetime
client = MongoClient('localhost', 27017)
db = client.users

app = Flask(__name__)
app.config['SECRET_KEY'] = "ABCD"
SECRET_KEY = 'secret'

API_KEY= 'W7rRGCTEuCgKF9Ml%2FwKJbHCJf0duO218F3SYriSEGGFnjmztdsdfE9CmzyEcW8vma%2FwxwqteC1HIXU4bTgjjOg%3D%3D'
API_URL=f'http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?ServiceKey={API_KEY}&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=TestApp&_type=json'

@app.route('/')
def main():
    token_receive = request.cookies.get('mytoken')
    try:
        # token을 시크릿키로 디코딩
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        
        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        
        return redirect("article")

    except jwt.ExpiredSignatureError:
        # 만료시간이 지났으면 에러가 납니다.
        return redirect(url_for('render_login'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('render_login'))

@app.route('/article')
def show_article() :
    token_receive = request.cookies.get('mytoken')
    
    try :
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        req = requests.get(API_URL)
        res = req.json()
        print(res)
        return render_template('main.html')
    except jwt.ExpiredSignatureError:
        # 만료시간이 지났으면 에러가 납니다.
        return redirect(url_for('render_login'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('render_login'))


@app.route('/login',methods=['GET'])
def render_login():
    if request.method=="GET":
        return render_template("login.html")


# ajax 요청을 받음
@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        user_id = request.form['user_id']
        password = request.form['password']

        pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        user_data = db.users.find_one({'id':user_id,'pw':pw_hash})
        
        if not user_data:
            flash("없는 아이디입니다.")
            return redirect(url_for('render_login'))

        elif pw_hash != user_data['password']:
            flash("비밀번호를 확인해주세요.")
            return url_for("/login")

        if user_data is not None:
            payload = {
                'id': user_id,
                'exp': datetime.utcnow() + datetime.timedelta(hours=1)
            }
            # 뒤에 decode는 byte 속성을 문자열로 바꾸는 역할
            token = jwt.encode(payload,SECRET_KEY,algoristm='HS256').decode('utf-8')
            
            return jsonify({
                'result':'success','token' : token })
        else :
            return jsonify({'result': 'fail','msg':'아이디/비밀번호가 맞지 않습니다.'})


@app.route('/register', methods=['GET'])
def join():
    if request.method == 'GET':
        return render_template('register.html')


    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST' :
        user_id = request.form['user_id']
        fullname = request.form['fullname']
        password = request.form['password']
        check_password = request.form['check_password']

        user_info = db.users.find_one({'id':user_id})
        if user_info is not None:
            flash("이미 가입된 이메일입니다")
            return redirect('/register')

        if password != check_password:
            flash("패스워드를 다시 확인해주세요")
            return redirect('/register')
        pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        db.user.insert_one({'id': user_id, 'pw': pw_hash, 'fullname': fullname})
            
    return render_template('main.html')


if __name__ == '__main__':
    app.debug = True
    app.run()