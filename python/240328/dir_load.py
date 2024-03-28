import os
from glob import glob
import pandas as pd

## 파일을 데이터프레임으로 로드하는 함수를 하나 생성
## 매개변수 1개 : 상대경로 | 절대경로, encoding = 'utf-8'
def read_df(_path, _encoding = 'utf-8' ):
    # 입력받은 데이터에서 확장자를 분리해준다.
    head, tail = os.path.splitext(_path)
    #print(tail)
    if tail == '.csv':
        df = pd.read_csv(_path, encoding = _encoding)
    elif tail == '.json':
        df = pd.read_json(_path, encoding = _encoding)
    elif tail == '.xml':
        df = pd.read_xml(_path, encoding = _encoding)
    elif tail in ['.xlsx','.xls']:
        df = pd.read_excel(_path)
    else:
        df = pd.DataFrame()
    return df

## 지정된 경로에 파일들을 하나의 데이터프레임으로 
# 결합하여 되돌려주는 함수 생성
# 매개변수? -> 경로, 확장자명

def data_load(_path, _end = 'csv'):
    file_list = os.listdir(_path)
    # 비어있는 데이터프레임 생성
    result = pd.DataFrame()
    _path = _path + '/'
    for file in file_list:
        # file -> 파일명
        # 파일명의 확장자가 유저가 입력한 확장자와 같다면
        if file.endswith(_end):
            try:
                df = read_df(_path+file)
            except:
                try:
                    df = read_df(_path+file, 'cp949')
                except:
                    df = read_df(_path + file, 'euc-kr')
            # df를 result에 유니언 결합
            result = pd.concat([result, df],
                             axis=0, ignore_index=True)
    return result


## 특정 경로에 있는 파일의 목록들을 각가 파일의 이름으로 전역변수를 생성하여 저장하는 함수 생성
## 매개변수 : 경로
def data_load2(_path):
    # 입력받은 경로를 기준으로 파일의 목록을 모두 로드한다.
    file_list = glob(_path + "/*.*")
    # 반복 실행 file_list를 이용하여
    # 비어있는 딕셔너리 데이터를 생성
    result = dict()
    for file in file_list: 
        # 경로와 파일명을 나눠준다
        folder, name = os.path.split(file)
        # 파일명에서 이름과 확장자를 나눠준다
        head, tail = os.path.splitext(name)
        try:
            df = read_df(file)
        except:
            try:
                df = read_df(file, 'cp949')
            except:
                df = read_df(file, 'euc-kr')

        if len(df) != 0:
            result[f"{head}"] = df.copy()
            #globals()[f"{head}"] = df.copy()
            print(f"{head} 전역변수 저장 완료")
        else:
            print('지원하지 않는 확장자 파일')
    return result







