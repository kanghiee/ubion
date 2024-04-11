# 프레임워크 로드
from flask import Flask, request
import pandas as pd
import database
import database_copy



# Flask Class 생성
# __name__ : 현재 파일의 이름
app = Flask(__name__)

## database에 있는 MyDB1 Class 생성
_db = database.MyDB1(
    _host = '172.30.1.22',
    _user = 'ubion',
    _password = '1234',
    _database = 'ubion'
)

# api를 생성
# 127.0.0.1:5000/ 요청 시 아래의 함수를 호출
@app.route('/')
def index():
    # 유저가 보낸 데이터를 확인하고 변수에 저장
    try:
        _id = request.args['input_id']
        _pass = request.args['input_pass']
    except:
        return "parameter error"
    print(_id, _pass)
    query = """
        SELECT * FROM user WHERE id = %s AND password = %s
"""
    result = _db.sql_query(query, _id, _pass)
    if result:
        # 외부의 csv 파일을 로드
        # csv 폴더의 -> 파일 로드
        df = pd.read_csv('../csv/corona.csv', index_col = 0)
        data = df.to_dict()
        return data
    else:
        return "입력 데이터 오류"




## 웹서버를 실행
app.run(debug=True)


