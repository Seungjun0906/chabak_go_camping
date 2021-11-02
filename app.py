from flask import Flask,request,render_template,redirect,flash
import requests
import jwt
import hashlib

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.users

app = Flask(__name__)
app.config['SECRET_KEY'] = "ABCD"

API_KEY= 'W7rRGCTEuCgKF9Ml%2FwKJbHCJf0duO218F3SYriSEGGFnjmztdsdfE9CmzyEcW8vma%2FwxwqteC1HIXU4bTgjjOg%3D%3D'
API_URL=f'http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?ServiceKey={API_KEY}&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=TestApp&_type=json'

@app.route('/', methods=['GET'])
def main():
    req = requests.get(API_URL)
    res = req.json()
    print(res)
    return render_template('main.html')



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
        if user_info:
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