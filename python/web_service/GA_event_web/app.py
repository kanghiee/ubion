from flask import Flask, render_template, request

# class 생성
app = Flask(__name__)

# api 생성
@app.route('/')
def index():
    # return 'Hello World'
    return render_template('index.html')

@app.route('/select')
def select():
    #  유저가 보낸 데이터를 변수에 저장
    # get 방식으로 보낸 데이터는 저장되어있는 곳은? -> request.args
    s1 = request.args['select1']
    s2 = request.args['select2']
    return render_template('select.html', 
                           select1 = s1, 
                           select2 = s2)

app.run(debug=True)