import pymysql

## mysql server와의 연동을 하는 Class 선언
class MyDB:
    # 생성자 함수
    def __init__(
            self,
            _host = 'localhost',
            _port = 3306,
            _user = 'root',
            _pw = '2409asdf',
            _db = 'ubion'
    ):
        self.host = _host
        self.port = _port
        self.user = _user
        self.pw = _pw
        self.db = _db
    def sql_query(self, _sql, *_values):
        # DB서버와의 연결
        mydb = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.pw,
            db = self.db
        )
        # cursor 생성
        cursor = mydb.cursor(pymysql.cursors.DictCursor)
        # _sql, _values를 이용하여 cursor에 질의를 던진다.
        cursor.execute(_sql, _values)
        # _sql이 select문인가 확인
        if _sql.lower().strip().startswith('select'):
            result = cursor.fetchall()
        else:
            mydb.commit()
            result = 'Query OK'
        # DB 서버와의 연결을 종료
        mydb.close()
        # 결과값을 되돌려준다.
        return result
