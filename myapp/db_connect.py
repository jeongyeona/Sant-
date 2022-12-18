# MariaDB 연결정보를 객체로 저장
# 보이면 안되기 때문에 보이지 않게 별도의 파일에 보관해야 된다.


config = {
    'host':'61.74.225.3',
    'user':'root',
    'password':'kor123',
    'database':'1team',
    'port':3306,
    'charset':'utf8',
    'use_unicode':True
}

import pickle

with open('mydb.dat', mode='wb') as obj:
    pickle.dump(config, obj)