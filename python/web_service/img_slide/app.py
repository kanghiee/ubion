# flask 웹 프레임워크 로드
from flask import Flask, request, render_template
# database 안에 있는 MyDB class 로드
from static.python.database import MyDB
# Flask class 생성
app=Flask(__name__)
# MyDB class 생성
mydb = MyDB(
    '127.0.0.1',
    3306,
    'root',
    '2409asdf',
    'ubion'   
)

# localhost:5000/ api을 생성하여 img_slide.html를 되돌려주는 함수 생성
@app.route('/')
def slide():     
    # DB server에 있는 company_list table의 정보를 로드
    select_query = """
        select *
        from company_list
    """
    # calss 생성 mydb안에 내장된 함수를 호출
    db_data = mydb.db_execute(select_query)
    # db_data의 타입은? [{name : xxxx, link_url : xxxx, img_url : xxxx}]
    # db_data에서 img_url만 따로 추출
    imgs = []
    links = []
    for data in db_data:
        imgs.append(data['img_url'])
        links.append(data['link_url'])
    print(imgs)
    print(links)
    return render_template('img_slide.html',
                           imgs = imgs,
                           links = links,
                           cnt = len(imgs))

# 웹서버를 실행
app.run(port = 8080,debug=True)