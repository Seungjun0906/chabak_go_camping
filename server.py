from flask import Flask,request,render_template
import requests
app = Flask(__name__)

API_KEY= 'W7rRGCTEuCgKF9Ml%2FwKJbHCJf0duO218F3SYriSEGGFnjmztdsdfE9CmzyEcW8vma%2FwxwqteC1HIXU4bTgjjOg%3D%3D'
API_URL=f'http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?ServiceKey={API_KEY}&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=TestApp&_type=json'

@app.route('/', methods=['GET'])
def main():
    req = requests.get(API_URL)
    res = req.json()
    print(res)
    return render_template('main.html')



