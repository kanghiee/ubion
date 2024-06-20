import pymysql

## DataBase 접속과 query구문을 사용하는 class 선언
class MyDB1:
    # 생성자 함수 생성 -> DB server의 정보를 입력 값으로 받아온다.
    def __init__(
            self, 
            _host = '127.0.0.1', 
            _port = 3306, 
            _user = 'root', 
            _password = '1234', 
            _database = 'ubion'
    ):
        # 객체 변수를 생성
        self.host = _host
        self.port = _port
        self.user = _user
        self.password = _password
        self.database = _database
    
    ## 일반 함수 생성
    def sql_query(self, sql, *values):
        # DB server 연결 -> _db 변수를 생성
        _db = pymysql.connect(
            host = self.host, 
            port = self.port, 
            user = self.user, 
            password = self.password, 
            db = self.database
        )
        # cursor 생성 
        cursor = _db.cursor(pymysql.cursors.DictCursor)

        # sql, values 값을 가지고 execute()
        cursor.execute(sql, values)

        # sql 값이 select문인가?
        if sql.lower().split()[0] == 'select':
            result = cursor.fetchall()
        else:
            _db.commit()
            result = "Query OK"
        
        # DB server와의 연결을 종료
        _db.close()

        # result 되돌려준다.
        return result