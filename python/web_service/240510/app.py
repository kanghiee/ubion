# flask 프레임 워크 로드
from flask import Flask, render_template, request, redirect
# 웹과 mysql 연동
import pymysql
# pandas 로드
import pandas as pd


# Flask class 생성
app = Flask(__name__)

#mysql sever와의 연결 (server 정보)
# server 정보 : 서버의 주소, 서버의 port, mysql 접속 아이디
# 비밀번호, 데이터베이스명
_db = pymysql.connect(
    host = 'localhost',
    port = 3306, 
    user = 'root',
    password = '2409asdf',
    database = 'ubion'
)

# 가상공간(Cursor) 생성
# 기본값을 이용하여 가상공간 생성 
# -> select문을 상요하여 결과 값을 받아올때 결과의 타입? : tuple
# DictCursor을 이용하여 가상공간 생성
# -> select문을 사용하여 결과 값을 받아올때 결과의 타입 ? : dict
cursor = _db.cursor(pymysql.cursors.DictCursor)

# DB server에 table을 생성하는 sql 쿼리문 작성
# 만약에 table이 존재한다면 table을 생성하지 않는다.
user_table_create = """
    CREATE TABLE
    IF NOT EXISTS
    `user`
    (
        `id` varchar(32) primary key,
        `password` varchar(64) not null,
        `name` varchar(32) not null
    )
"""
# 쿼리문 실행
cursor.execute(user_table_create)
# DB server에 동기화
_db.commit()


# api 생성
@app.route('/')
def index():
    # 특정 페이지(templates 폴더 안에 있는 html 문서)를 리턴
    return render_template('index.html')

# localhost:80/에서 유저가 보낸 데이터를 받아오는 api
@app.route('/login', methods=['post'])
def login():
    # 유저가 보낸 데이터를 변수에 저장
    # 유저가 보낸 데이터 -> request 
    # get 방식으로 보낸 데이터는 request.args
    # post 방식으로 보낸 데이터는 request.form
    # 데이터의 타입은? dict
    # 유저가 보낸 ID 값
    _id = request.form['input_id']
    # 유저가 보낸 password 값
    _pass = request.form['input_pass']
    # 유저가 보낸 데이터를 확인
    print(f"id : {_id}, password : {_pass}")
    # 유저가 보낸 데이터를 DB server에서
    # 특정 table에 id와 password 존재하는가?
    # user table에서 id와 password가 같다 
    # 두개의 조건을 모두 만족하는 데이터의 유무 판단
    # 쿼리문 작성
    login_query = """
        SELECT * FROM
        `user` 
        WHERE
        `id` = %s 
        AND
        `password` = %s
    """
    # 쿼리문을 실행
    cursor.execute(login_query,[_id, _pass])
    # 결과값을 cursor에서 받아온다.
    result = cursor.fetchall()
    # 로그인이 성공 유무 판단을 하는 방법?
    # 성공하는 경우? -> result에 데이터가 존재
    # 실패하는 경우? -> result는 비어있는 데이터
    print(f"login_query result : {result}")
    if result:
        return "로그인 성공"
    else:
        return "로그인 실패"

#회원 가입 페이지를 보여주는 api
@app.route('/signup', methods=['get'])
def signup2():
    return render_template('signup.html')



# 유저가 회원가입을 위한 데이터를 보내주는 api
@app.route('/signup', methods = ['post'])
def signup():
    # 유저가 보낸 데이터를 변수에 저장
    # 유저가 보낸 데이터는? -> request.form
    # 데이터의 형태는? {'input_id' : xxxx, 'input_pass' : xxxx, 'input_name' : xxxx}
    # dict데이터에서 value 값들만 추출하는 방법? values()
    req = request.form.values()
    #print(list(req))
    data = list(req)
    # DB server에 회원 정보를 삽입(insert 구문)
    # insert 쿼리문 작성
    signup_query = """
        insert into `user`
        values
        (%s, %s, %s)
    """
    # 가상공간에 쿼리문을 실행한다
    cursor.execute(signup_query, data)
    # 데이터베이스와 가상공간의 데이터를 동기화
    _db.commit()
    # 로그인 화면으로 되돌아간다. ('/' 주소로 이동)
    return redirect('/')


# 웹서버를 실행
app.run(port=8080, debug = True)
