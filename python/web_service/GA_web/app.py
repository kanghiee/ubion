# flask 프레임 워크 안에 특정 기능들을 로드
from flask import Flask, render_template, request, redirect, url_for
# mysql과 연동을 하는 라이브러리 로드
import pymysql


# Flask라는 Class 생성
app = Flask(__name__)

# 함수생성
# DB server와 연결하고 -> 가상공간 Cursor 생성 ->
# 매개변수 query문, data값을 이용하여 질의를 보내고 -> 
# 결과 값을 받아오거나 DB서버에 동기화 _>
# DB server와의 연결을 종료.
def db_execute(query,*data):
    # 데이터베이스와 연결
    _db = pymysql.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = '2409asdf',
        database = 'ubion'
    )
    # 가상공간 Cursor 생성
    cursor = _db.cursor(pymysql.cursors.DictCursor)
    # 매개변수 query, data를 이용하여 질의
    cursor.execute(query, data)
    # query가 select라면 결과값을 변수(result)에 저장
    if query.lower().strip().startswith('select'):
        result = cursor.fetchall()
    # query가 select가 아니라면 DB server와 동기화하고
    # 변수(result)는 Query OK 문자를 대입
    else:
        _db.commit()
        result = 'Query OK'
    # 데이터베이스 서버와의 연결을 종료
    _db.close()
    # 결과(result)를 되돌려준다.
    return result

# 메인페이지 api 생성
# 로그인 화면
@app.route("/")
def index():
    # 요청이 들어왔을 때 state라는 데이터가 존재하면
    try:
        # 로그인이 실패한 경우
        _state = request.args['state']
    except:
        # 처음 로그인 화면을 로드한 경우
        _state = 1
    # login.html 되돌려준다.
    return render_template('login.html', state = _state)

# 로그인 화면에서 id, password 데이터를 보내는 api 생성
@app.route("/main", methods=['post'])
def main():
    # 유저가 보낸 데이터: ID, PASSWORD
    # 유저가 보낸 id값의 key -> input_id
    # 유저가 보낸 password값의 key -> inputs_pass
    _id = request.form['input_id']
    _pass = request.form['input_pass']
    # 받아온 데이터를 확인
    print(f"/main[post] -> 유저 id : {_id}, password : {_pass}")
    # 유저가 보낸 데이터를 DB server에 table data와 비교
    login_query = """
        select *
        from `user`
        where `id` = %s and `password` = %s
    """
    # 함수 호출
    db_result = db_execute(login_query, _id, _pass)
    # 로그인의 성공 여부 (조건식??) 
    if db_result:
        # 로그인이 성공하는 경우 -> main.html을 되돌려준다
        return render_template('main.html')
        #return "login ok"
    else:
        # 로그인이 실패하는 경우 -> 로그인화면('/')으로 되돌아간다.
        return redirect('/?state=2')
        #return 'login fail'


# 회원가입 화면을 보여주는 api 생성
@app.route('/signup')
def signup():
    return render_template('signup.html')

# id 사용 유무를 판단하는 api
@app.route('/check_id', methods=['post'])
def check_id():
    # 프로트에서 비동기 통신으로 보내는 id 값을 변수에 저장
    _id = request.form['input_id']
    # 유저에게 받은 데이터 확인
    print(f"/check_id[post] -> 유저 id : {_id}")
    # 유저가 보낸 id값이 사용이 가능한가?
    # 조건? -> 해당 아이디와 동일한 아이디가 table에 존재하는가?
    check_id_query = """
        select * from `user`
        where `id` = %s
    """
    # 함수 호출
    db_result = db_execute(check_id_query, _id)
    # id가 사용가능한 경우: db_result는 존재하지 않는다.
    if db_result:
        result = '0'
    else:
        result = '1'
    return result

# 회원 정보를 받아와서 데이터베이스에 삽입을 하는 api
@app.route('/signup2', methods=['post'])
def signup2():
    # 유저가 보낸 데이터를 변수에 저장
    _id = request.form['input_id']
    _pass = request.form['input_pass']
    _name = request.form['input_name']
    print(f"/signup2[post] -> 유저 ID : {_id}, password : {_pass}, name : {_name}")
    # 쿼리문 작성(위에 3개 데이터베이스에 삽입하기위한)
    insert_user_query = """
        insert into `user`
        values(%s, %s, %s)
    """
    # 함수 호출 (에러가 발생하는 경우가 있으니 try 생성)
    try:
        db_result = db_execute(insert_user_query, _id, _pass, _name)
        print(db_result)
    except:
        db_result = 3
    # 로그인 화면으로 되돌아간다.
    if db_result ==3:
        return redirect(f'/?state={db_result}')
    else:
        return redirect('/')
# 웹 서버를 실행
app.run(port = 8080,debug=True)