from flask import Flask, render_template, request
import database_copy 
app=Flask(__name__)

# MyDB class 생성
mydb = database_copy.MyDB()

@app.route("/")
def index():
    return render_template('index.html')

# 데이터베이스에 저장된 아이템의 목록을 보여주는 api생성
@app.route('/shop')
def shop():
    # items table에 있는 모든 정보를 로드
    items_select = """
        select * from items
    """
    # mydb를 이용하여 쿼리문을 실행
    db_result = mydb.sql_query(items_select)
    print(db_result)
    # html문서와 db_result변수를 결합하여 유저에게 되돌려준다.
    return render_template('item_list.html', 
                           db_data = db_result)



# 상품의 정보를 출력하는 api를 생성
@app.route('/item_info')
def item_info():
    # 유저가 보낸 데이터가 존재
    # get 방식으로 보낸 데이터를 추출
    item_id = request.args['no']
    # 상품의 정보를 추출하는 쿼리문을 작성
    selected_item_info = """
        select * from `items` where `No` = %s
    """

    db_result = mydb.sql_query(selected_item_info, item_id)
    print(db_result)
    return render_template('item_info.html', info = db_result)

app.run(debug=True)