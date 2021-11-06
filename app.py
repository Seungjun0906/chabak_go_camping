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

# jwt 시크릿 키
SECRET_KEY = 'SECRET'

API_KEY = 'W7rRGCTEuCgKF9Ml%2FwKJbHCJf0duO218F3SYriSEGGFnjmztdsdfE9CmzyEcW8vma%2FwxwqteC1HIXU4bTgjjOg%3D%3D'
API_URL = f'http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?ServiceKey={API_KEY}&numOfRows=70&pageNo=4&MobileOS=ETC&MobileApp=TestApp&_type=json'


# mongoDB 연결 코드 
# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)

db = client.chabak


# 첫 메인 화면 접속시 로그인 정보따라 화면 이동
@ app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    # 토큰이 있으면 aritcle로
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return redirect("/article")
    
    # 없거나 만료되었다면 login으로
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@app.route('/article')
def show_article():
    try:
        token_receive = request.cookies.get('mytoken')
        # get api data
        res = requests.get(API_URL)
        # parse response JSON data
        data = res.json()
        # access to data that I need
        campsite_list = list(data['response']['body']['items']['item'])
        # helper function which filters data
        def campsite_with_photo(camp_list):
            new_list = []
            for camp in camp_list:
                if 'firstImageUrl' and 'intro' and 'resveUrl' in camp.keys():
                    new_list.append(camp)
            return new_list
        # save returned list to new variable
        filtered_camp = campsite_with_photo(campsite_list)
        # pass the new list as parameter to make jinja templates have access to the list
        return render_template('article.html', campsite_list=filtered_camp)

    except jwt.ExpiredSignatureError:
        # 만료시간이 지났으면 로그인으로
        return redirect(url_for('login',token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        # 로그인 정보가 존재하지 않으면 로그인으로
        return redirect(url_for('login'))
        
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
        # 비밀번호 암호화
        result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
        # 데이터베이스에서 유저 정보가 있는지 검색
        
        # 유저 정보가 있다면 토큰발급
        if result is not None:
            payload = {
                'id': id_receive,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({'result': 'success', 'token': token})
        
        # 찾지못하면    
        else:
            return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@ app.route('/sign-up')
def register():
    return render_template('sign-up.html')


@ app.route('/api/sign-up', methods=['POST'])
def api_sign_up():
    # form 에서 작성된 정보 가져오기
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pwConfirm_receive = request.form['pwConfirm_give']

    # 이미 가입된 id 인지 중첩검사
    check_duplicate_user = db.user.find_one({'id': id_receive})
    # 이미 가입된 정보가 있다면
    if check_duplicate_user is not None:
        if check_duplicate_user['id'] == id_receive:
            return jsonify({'result': 'fail', 'msg': '중복된 아이디가 존재합니다.'})
    # 비밀번호 중첩검사
    if pw_receive != pwConfirm_receive:
        return jsonify({'result': 'fail', 'msg': '비밀번호가 서로 일치하지 않습니다.'})

    # 비밀번호 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    # 데이터베이스에 유저정보 insert
    db.user.insert_one({'id': id_receive, 'pw': pw_hash})

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 방금 insert 한 정보로 바로 로그인이 되도록
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60) # 토큰 유효기간
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '예기치 못한 오류가 발생하였습니다.'})


@app.route('/review')
def review_home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('review.html', diaries = list(db.diary.find({}, {'_id': False}))
)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))

@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))
    return render_template('review.html', diaries=diaries)


@app.route('/diary', methods=['POST'])
def save_diary():
    # 데이터를 review.html 에서 받아옴
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    
    file = request.files["file_give"]
    # 확장자명 만들어줌
    
    extension = file.filename.split('.')[-1]

    # datetime 클래스로 현제 날짜와 시간 만들어줌 -> 현재 시각을 출력하는 now() 메서드
    today = datetime.datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'
    # 파일에 시간붙여서 static 폴더에 filename 으로 저장
    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title': title_receive,
        'content': content_receive,
        'file': f'{filename}.{extension}',
        'time': today.strftime('%Y.%m.%d')
    }
    # diary collection 에 저장 
    db.diary.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
