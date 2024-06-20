import pymysql

mydb = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '2409asdf',
    database = 'ubion'
)

cursor = mydb.cursor(pymysql.cursors.DictCursor)

# 테이블 생성
sql = """
        create table 
        IF NOT EXISTS
        items(
        `No` int primary key auto_increment,
        `Name` varchar(64) not null,
        `price` int not null,
        `img_url` text
        )
    """
cursor.execute(sql)
mydb.commit()


# 데이터 삽입
insert_data = """
    insert into
    `items`(`Name`, `price`, `img_url`)
    values
    ('[최저가데이] 하겐다즈 파인트/멀티바 3개 세트 [원산지:프랑스]',
    29900,
    'https://search.pstatic.net/common/?src=http%3A%2F%2Fshopping.phinf.naver.net%2Fmain_3944976%2F39449764234.20230418121632.jpg&type=a340'
    )
    ,(
    '[퍼실 300ml 증정] 헨켈 9중효소 세탁세제 퍼실 딥클린 파워젤 2.7L 2개',
    27900,
    'https://search.pstatic.net/common/?src=https%3A%2F%2Fsearchad-phinf.pstatic.net%2FMjAyNDAxMTZfMjAy%2FMDAxNzA1Mzg5MDc3NjA5.FpYny4QqJgC3K3v4KOEltDFFa9RDorErHw6IXzbUnGEg.M84xPiLN6krzp7vNFxAhMgjYwabVsM1xUcgcE8dbaS4g.PNG%2F1137903-b46d80d0-f93d-4d15-a40d-52aeb4f5c2dd.png&type=f372_372'
    ),
    (
    '[디스커버리] 경량 패커블 남성 바람막이 3종 택1',
    101400,
    'https://search.pstatic.net/common/?src=http%3A%2F%2Fshop1.phinf.naver.net%2F20240405_53%2F1712282641477UAAPU_JPEG%2F343412254996871_829280108.jpg&type=a340'
    )
"""
cursor.execute(insert_data)
mydb.commit()
mydb.close()