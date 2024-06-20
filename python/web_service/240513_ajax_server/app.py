from flask import Flask, request, render_template
import random
app = Flask(__name__)

# index.html를 보여주는 api생성
@app.route('/')
def index():
    return render_template('index.html')

# form 태그를 이용하여 보낸 데이터를 받는 api
@app.route('/data')
def data():
    # get방식으로 들어온 데이터를 확인
    req = request.args
    print("form 태그를 이용한 요청 메시지 :",req)
    return ""

# ajax를 이용하여 보낸 데이터를 받는 api
@app.route('/ajax_data')
def ajax_data():
    # get방식으로 들어온 데이터를 확인
    req = request.args
    print("ajax를 이용한 요청 메시지 :", req)
    return ""

# /game api 생성
@app.route('/game')
def game():
    return render_template('game.html')


#/game_result [post] api 생성
@app.route('/game_result', methods = ['post'])
def game_result():
    # 유저가 보낸 데이터를 변수에 저장
    _user = request.form['user']
    print("유저가 선택한 손동작 : ",_user)
    # 서버도 가위, 바위, 보 셋 중 하나를 랜덤하게 선택
    _list = ['가위','바위','보']
    _server = random.choice(_list)
    print("서버가 선택한 손동작 : ", _server)
    # 승부의 결과를 조건문으로 생성
    # _user와 _server가 같은 경우(무승부)
    if _user == _server :
        result = "무승부"
    else:
        # 두 개의 데이터가 다른 경우
        if _user == '가위':
            if _server == '바위':
                result = "바보 같은 놈"
            else:
                result == '축하방구'
        elif _user == '바위':
            if _server == '보':
                result = "바보 같은 놈"
            else:
                result = "축하방구"
        else:
            if _server == '가위':
                result = "바보 같은 놈"
            else:
                result = "축하방구"
    print(result)
    # ajax 통신에서 결과값의 타입? -> json
    # return 데이터를 dict 형태로 되돌려준다.
    return_data = {
        'user' : _user,
        'server' : _server,
        'result' : result
    }
    return return_data


# game_result2 api 생성
@app.route('/game_result2')
def game_result2():
    _user = request.args['g2']
    _list = ['가위','바위','보']
    _server = random.choice(_list)
    print("내가 선택한 손동작 : ", _user)
    print("서버가 선택한 손동작 : ", _server)
    # game_table 생성
    game_table = {
        '가위' : {
            '가위':'무승부',
            '바위':'바보 같은 놈',
            '보':'기특한 놈'
        },
        '바위':{
            '바위':'무승부',
            '보':'바보 같은 놈',
            '가위':'기특한 놈'
        },
        '보':{
            '보':'무승부',
            '가위':'바보 같은 놈',
            '바위':'기특한 놈'
        }
    }
    
    result = game_table[_user][_server]
    print('결과 : ', result)
    return result

app.run(debug=True)