import pymysql
class MyDB:
    # 생성자 함수
    def __init__(
            self, _host, _port, _user, _pass, _db
    ):
        # 클래스 내부에서 사용이 되는 독립 변수를 생성
        self.host = _host
        self.port = _port
        self.user = _user
        self.password = _pass
        self.db = _db
    # 클래스 내부에 함수 생성
    # 함수 생성
    # DB server와 연결하고 -> 가상공산 Cursor 생성 ->
    # 매개변수 query문, data값을 이용하여 질의를 보내고 ->
    # 결과 값을 받아오거나 DB서버에 동기화 -> 
    # DB server와의 연결을 종료
    def db_execute(self, query, *data):
        # 데이터베이스와 연결 (server 정보)
        _db = pymysql.connect(
            host = self.host, 
            port = self.port, 
            user = self.user, 
            password = self.password, 
            db = self.db 
        )
        # 가상공간 Cursor 생성
        cursor = _db.cursor(pymysql.cursors.DictCursor)
        # 매개변수 query, data를 이용하여 질의 
        cursor.execute(query, data)
        # query가 select라면 결과값을 변수(result)에 저장 
        if query.strip().lower().startswith('select'):
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
