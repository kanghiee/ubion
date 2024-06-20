# flask 웹 프레임워크를 로드
# render_template() -> html문서를 유저에게 되돌려주기 위한 함수
#   templates 폴더 안에 있는 html 문서를 되돌려준다
#   html문서를 parsing 작업을 통해 유저에게 되돌려주는 형태
#   html 문서에서 {{변수명}}, {% python code %}를 사용 가능
#   f-string과 비슷한 기능
from flask import Flask, render_template, request
import pandas as pd

# Flask class 생성
# 생성자 함수에 필수 인자 값 : 1개
#   파일의 이름(app.py -> __name__)
app = Flask(__name__)

# api 생성
# router : 네이게이터 함수 
# route()함수 안에 인자값과 루트주소와 
# 연결된 주소 값으로 요청 시 아래의 함수를 호출
# ex) @app.route('/view_info') --> localhost:8080/view_info 주소로 요청시
@app.route('/')
def index():
    return '<h1>Hello World</h1>'

# 새로운 api 생성 
# page1.html을 되돌려주는 api
@app.route('/first')
def first():
    # templates 폴더 안에 있는 page1.html 파일을 로드하여 
    # parsing
    # render_template() 함수에 변수를 지정 -> 서버가 유저에게 데이터를 보내는 부분
    print(render_template('page1.html', name = 'test'))
    print(type(render_template('page1.html', name = 'test')))
    return render_template('page1.html', name = 'test') 

# 유저가 서버에게 데이터를 보내는 페이지 api
@app.route('/second')
def second():
    return render_template('page2.html')

# /second 페이지에서 유저가 보낸 데이터를 받아오는 api
@app.route('/data')
def data():
    # 유저가 보낸 데이터를 변수에 저장 
    # {'q' : 'data'} --> request 메시지에 저장
    print(request.args['q'])
    search_data = request.args['q']
    return search_data

# chart html 문서를 보내는 api 
@app.route('/chart')
def chart():
    # select키로 들어오는 데이터에 따라서 로드하는 csv 파일을 변경
    # type키는 라인, 바를 선택
    input_select = request.args['select']
    input_type = request.args['type']
    # pandas 안에 있는 read_csv()함수를 이용하여 데이터를 로드 
    df = pd.read_csv(f"../csv/{input_select}.csv")
    df = df.tail(10)
    # x축 데이터 -> df에서 Date 컬럼의 값
    input_x = list(df['Date'])
    # y축 데이터 -> df에서 Close 컬럼의 값
    input_y = df['Close'].to_list()
    return render_template('chart.html', _x = input_x, 
                           _y = input_y, _type = input_type)


# 웹 서버를 실행
# run() 함수는 매개변수 port의 기본값은 5000
app.run(port = 8080, debug=True)