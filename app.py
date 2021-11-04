from datetime import datetime
from bson.objectid import ObjectId
import base64
import datetime 
import jwt
import hashlib
import json
import requests
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)
SECRET_KEY = 'SECRET'
API_KEY= 'W7rRGCTEuCgKF9Ml%2FwKJbHCJf0duO218F3SYriSEGGFnjmztdsdfE9CmzyEcW8vma%2FwxwqteC1HIXU4bTgjjOg%3D%3D'
API_URL=f'http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?ServiceKey={API_KEY}&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=TestApp&_type=json'

client = MongoClient('localhost', 27017)
db = client.chabak

@ app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return redirect("/article")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))

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
        # 로그인 정보가 존재하지 않음.

@ app.route('/login')
def login():
    token_expired = request.args.get("token_expired")
    return render_template('login.html', token_expired=token_expired)


@ app.route('/api/login', methods=['POST'])
def api_login():
    if request.method == 'POST':
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']

        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
        result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

        if result is not None:
            payload = {
                'id': id_receive,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({'result': 'success', 'token': token})
        else:
            return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@ app.route('/sign-up')
def register():
    return render_template('sign-up.html')


@ app.route('/api/sign-up', methods=['POST'])
def api_sign_up():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pwConfirm_receive = request.form['pwConfirm_give']

    check_duplicate_user = db.user.find_one({'id': id_receive})

    if check_duplicate_user is not None:
        if check_duplicate_user['id'] == id_receive:
            return jsonify({'result': 'fail', 'msg': '중복된 아이디가 존재합니다.'})

    if pw_receive != pwConfirm_receive:
        return jsonify({'result': 'fail', 'msg': '비밀번호가 서로 일치하지 않습니다.'})

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash })

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
    
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '예기치 못한 오류가 발생하였습니다.'})

        

@app.route('/review')
def review_home():
    return render_template('review.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))
    return jsonify({'all_diary': diaries})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title':title_receive,
        'content':content_receive,
        'file': f'{filename}.{extension}',
        'time': today.strftime('%Y.%m.%d')
    }

    db.diary.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5021, debug=True)
