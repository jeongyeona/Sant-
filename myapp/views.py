from django.shortcuts import render, redirect
from myapp.models import WineUser, WineGrade, Wine
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import pandas as pd
import numpy as np
from django.db.models import Avg
import pickle
import MySQLdb
import os
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical  
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import RobustScaler, MinMaxScaler, StandardScaler
import random
import math
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers.core import Dense, Dropout
import matplotlib.pyplot as plt
import tensorflow as tf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from keras.callbacks import ModelCheckpoint, EarlyStopping

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
current_path = os.path.abspath(__file__) # 경로를 객체화
parent_dir = os.path.dirname(current_path)

# Create your views here.
def main(request):
    user_data = WineUser.objects.all()
    if request.session.get('WinePid'):
        pid=request.session.get('WinePid')
        modeling(pid)
    return render(request, "main.html", {'user':user_data})

def signupok(request):
    if request.method == "POST":
        name = request.POST.get('User_name')
        id = request.POST.get('User_id')
        pwd = request.POST.get('User_pwd')
        pwdok = request.POST.get('User_pwdok')
        email = request.POST.get('User_email')
        
        err_data = {}
        if not(id and name and pwd and pwdok):
            err_data['error'] = "모든 값을 입력해야 합니다."
        elif pwd != pwdok:
            err_data['error'] = "비밀번호가 틀립니다."
        else:
            WineUser(
                id=id,
                nickname=name,
                pwd=make_password(pwd), # make_password() 암호화
                email=email
                ).save()
            return redirect('/') 
    return render(request, 'main.html', err_data) # render -> html화면을 띄어주기


def loginok(request):
    lo_error = {}
    if request.method == "POST":
        login_id = request.POST.get('lo_id')
        login_pwd = request.POST.get('lo_pwd')
        
        if not(login_id):
            lo_error['err']="아이디와 비밀번호를 모두 입력해주세요"
        if(login_id):
            # __________________________________
            try:
                wine_user = WineUser.objects.get(id=login_id)
            except WineUser.DoesNotExist:
                return render(request, 'iderr.html')
            # __________________________________
            # if wine_user == 0:
            # return render(request, "err.html")
            if check_password(login_pwd, wine_user.pwd): # 비번이 일치하면
                request.session['WineUser'] = wine_user.id
                request.session['WinePid'] = wine_user.pid
                request.session['WineNick'] = wine_user.nickname
                return redirect('/')
            else: # 비번이 일치하지 않으면
                return render(request, 'pwderr.html')

    return render(request, "iderr.html")
    
def err(request):
    return render(request, 'err.html')
    
def logout(request):
    request.session.flush()
    return redirect('/')

def winelist(request):
    data = sql()
    df = data.copy()
    postdata=postpro(df)
    df2 = data.copy()
    bb = 0
    if request.session.get('WinePid'):
        pid=request.session.get('WinePid')
        predstardf=deep(postdata, pid)
        
        # 예상 별점 테이블을 로그인시 나오는 data에 붙여야함
        data = pd.concat([data, predstardf], axis=1)
        df2 = data.copy()
        print(data.head())

        # distance 함수는 인코딩할 dataframe과 랜덤한 최고평점 와인의 인덱스를 파라미터로 받음 
        try:
            ddata = distance(postdata, pid)
            if len(ddata)!=0:
                print('시작')
                data = pd.concat([data, ddata], axis=1)
                data = data.sort_values('distance', ascending=True)
                print('거리순 정렬')
                print(data[['id','distance']].head(6))
                aa=data.index[data['distance']==0]
                bb=df['name_kr'][aa].iloc[0]
                
                data=data[1:11]
        except:
            pass
    sk =''
    cb =''
    cf =''
    vt =''
    wf =''
    pr =''
    search_key = ''
    list_check = ''
    list_check2 = ''
    list_check3 = ''
    list_check4 = ''
    m_range2 = ''
    if request.method == "GET":
        if request.GET.get('priceRange'):
            data = df2
            m_range2 = request.GET.get('priceRange')
            if m_range2 == "20":
                m_range=int(m_range2)*500000
            else:
                m_range=int(m_range2)*10000
            # data = data[data['price'].str.contains(m_range)]
            pr = '&priceRange='
            
            # max_range = request.GET.get('priceRange') * 1
            # max_range = request.GET.get('priceRange')
            data=data[data['price'] <= m_range ] # 재활용

            bb = 0
        if request.GET.get('search_key'):
            search_key = request.GET.get('search_key')
            data = data[data['name_kr'].str.contains(search_key)]
            sk = '&search_key='
            
        if request.GET.get('filterBtn'):
            list_check = request.GET.get('filterBtn')
            data = data[data['type'].str.contains(list_check)]
            cb = '&filterBtn='
        if request.GET.get('filterBtn2'):
            list_check2 = request.GET.get('filterBtn2')
            data = data[data['nation'].str.contains(list_check2)]
            cf = '&filterBtn2='
        if request.GET.get('filterBtn3'):
            list_check3 = request.GET.get('filterBtn3')
            data = data[data['food'].str.contains(list_check3)]
            wf = '&filterBtn3='
        if request.GET.get('filterBtn4'):
            list_check4 = request.GET.get('filterBtn4')
            data = data[data['varieties'].str.contains(list_check4)]
            vt = '&filterBtn4='
        count = len(data)
        page=request.GET.get("page", 1) # 페이지
        paginator=Paginator(data.to_dict(orient='records'), 10) # 페이지당 6개씩 보여주기
        page_obj = paginator.get_page(int(page))
        
        return render(request, 'winelist.html', {'favorite':bb, 'count':count, 'question_list':page_obj, 'sk':sk, 'search_key':search_key, 'cb':cb, 'list_check':list_check, 'cf':cf,'list_check2':list_check2, 'vt':vt, 'wf':wf, 'list_check3':list_check3, 'list_check4':list_check4, 'pr':pr, 'm_range':m_range2,'search_key':search_key})

def grade(request):
    if request.method == "GET":
        wine = request.GET.get('wineid')
        grade = request.GET.get('rating')
        id = request.GET.get('id')
        wine_user = WineUser.objects.get(id=id)
        # print(wine_user.pid)
        # print(id)
        # print(wine)
        # print(grade)
        
        print(current_path)
        with open(parent_dir + '/mydb.dat', mode='rb') as obj:
            config = pickle.load(obj)
        
        try:
            conn = MySQLdb.connect(**config)
            cursor = conn.cursor()
            sql = "INSERT INTO wine_grade(userid, wineid, grade) VALUES({},{},{})".format(wine_user.pid, wine, grade)
            count = cursor.execute(sql)
            print(count)
            conn.commit()

            winedataid = Wine.objects.get(id=wine)
            winedataid.nation = winedataid.nation.split(sep='(')[0]
            
            diw = request.session['WinePid']

            data = mysql(diw, wine)
            
            if data:
                data = data[0]
            
            return render(request, 'winedetail.html', {'data':data[0], 'wineid':wine,"winedataid":winedataid})
        except:
            sql = "UPDATE wine_grade SET grade={} WHERE wineid={} AND userid={}".format(grade, wine, wine_user.pid)
            count = cursor.execute(sql)
            # print(count)
            conn.commit()

            winedataid = Wine.objects.get(id=wine)
            winedataid.nation = winedataid.nation.split(sep='(')[0]
            
            diw = request.session['WinePid']
            # print(diw)
            
            data = mysql(diw, wine)
            
            if data:
                data = data[0]

            return render(request, 'winedetail.html', {'data':data, 'wineid':wine,"winedataid":winedataid})
        finally:
            cursor.close()
            conn.close()

    return render(request, 'err.html')

def pwdok(request):
    return render(request, "pwdok.html")

def pwdreset(request):
    lo_error = {}
    if request.method == "POST":
        name = request.POST.get('name')
        id = request.POST.get('id')
        email = request.POST.get('email')
        # if (WineUser.objects.get(id=id)):
        #     lo_error['err']="없는 아이디입니다."
        
        if not(id and name and email):
            lo_error['err']="정보를 모두 입력해주세요"
        else:
            if WineUser.objects.filter(nickname=name,
                                             id=id, email=email).exists():
                # print(WineUser.objects.filter(nickname=name,
                # id=id, email=email).exists())
                # print('존재하는 회원입니다')
                # if wine_user == 0:
                #     return render(request, "err.html")
                return render(request, "pwdreset.html", {'id':id})
            else:
                # print('false')
                lo_error['err'] = "비밀번호를 틀렸습니다."
                return render(request, "err.html")
    
def pwdsuc(request):
    err_data = {}
    id=request.POST.get('id')
    # print(id)
    if request.method == "POST":
        new = request.POST.get('new')
        newok = request.POST.get('newok')
    
        if new != newok:
            err_data['error'] = "비밀번호가 틀립니다."
    
        else:
            wine_user = WineUser.objects.get(id=request.POST.get('id'))
            wine_user.pwd=make_password(new)
            wine_user.save()
            # print(wine_user)
            return redirect("/")
    return render(request, 'err.html')

def addinfo(request):
    wineid = request.session['WineUser']
    diw = request.session['WinePid']
    
    gradedata = mystarcount(diw)
    # print(data)
    
    gdf = pd.DataFrame(gradedata, columns = ['wid', 'mygrade'])
    gdf = gdf.reset_index(drop=True)
    # print(gdf.head(3))
    
    winedata = sql()
    wdf = winedata.copy()
    postdata=postpro(wdf)
    # print(postdata.head(3))
    
    # 선호 국가
    df = pd.concat([wdf, gdf], axis=1)
    # df.info()
    df = df.dropna(axis='index', how='any')
    df['mygrade']=df['mygrade'].astype(int)
    # pd.set_option('display.max_columns', 20)
    # print(df)
    count = df['nation'].value_counts()
    # print('여기')
    nationcount = count.reset_index().rename(columns={'index':'nation', 'nation':'count'})
    # print(nationcount)
    nationcount = nationcount[0:3]
    nationcount = nationcount.to_dict('records')
    # print(nationcount)
    
    # 품종
    varieties = df['varieties'].value_counts()
    varieties = pd.DataFrame(varieties)
    varieties = varieties.reset_index().rename(columns={'index':'varieties', 'varieties':'count'})
    # print(varieties)
    varieties = varieties[0:3]
    varieties = varieties.to_dict('records')
    
    # 내 별점 평균
    # print(df['mygrade'])
    mygrade = pd.DataFrame(df['mygrade'])
    print('여기')
    print(mygrade)
    mygrade = round(mygrade.mean(), 2)
    mygrade = pd.DataFrame(mygrade)
    mygrade = mygrade.rename(columns={'0':'mygrade'})
    mygrade = mygrade.to_dict('records')
    # print('여기')
    # print(mygrade)
    
    # 내 별점 개수
    gradecount = pd.DataFrame(df['mygrade'])
    # print(gradecount)
    gradecount = gradecount.count()
    # print(gradecount)
    
    # 많이 준 별점
    maxgrade = pd.DataFrame(df['mygrade'])
    maxgrade = maxgrade.astype(str)
    print(maxgrade.info())
    fig = px.histogram(maxgrade, x='mygrade', labels={'mygrade':''}, category_orders=dict(mygrade=['1','2','3','4','5']), color_discrete_sequence=['#ff0558'])
    fig.update_layout(go.Layout(plot_bgcolor='white'))
    fig.update_layout(yaxis=dict(visible=False))
    starcount = maxgrade['mygrade'].value_counts()
    
    print(starcount)
    starcount = starcount.reset_index().rename(columns={'index':'star', 'grade':'count'})
    maxgrade = starcount.to_dict('records')
    if maxgrade:
        maxgrade = maxgrade[0]
    else:
        maxgrade = 0
    # print(starcount)
    # maxgrade = starcount.to_dict('records')
    # print(maxgrade)

    # fig = px.bar(starcount, x='star', y="mygrade", facet_col_spacing=1)
    
    return render(request, 'addinfo.html', {'graph':fig.to_json, 'maxgrade':maxgrade, 'gradecount':gradecount, 'mygrade':mygrade, 'nation':nationcount, 'varieties':varieties, 'df':df, 'wineid':wineid})

def winedetail(request):
    if request.method == "GET":
        wineid = request.GET.get('wineid')
        winedataid = Wine.objects.get(id=wineid)
        winedataid.nation = winedataid.nation.split(sep='(')[0]
        
        data = []
        if request.session.get('WinePid'):
            diw = request.session.get('WinePid')
            data = mysql(diw, wineid)
            data = re.sub(r"[^0-9]", "", str(data))
                        
    return render(request, 'winedetail.html', {'data':data, 'wineid':wineid,"winedataid":winedataid})

def pwderr(request):
    return render(request, 'pwderr.html')

def iderr(request):
    return render(request, 'iderr.html')

def sql():  
    # print(current_path)
    with open(parent_dir + '/mydb.dat', mode='rb') as obj:
        config = pickle.load(obj)
    
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
        sql = "select * from wine left join (select wineid, round(avg(grade), 2) as grade from wine_grade group by wineid) as avgstar on wine.id = avgstar.wineid order by id"
        cursor.execute(sql)
        result = cursor.fetchall()

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    
    data = pd.DataFrame(result, columns=['id', 'name_kr', 'name_en', 'producer', 'nation', 'varieties', 'type', 'food', 'abv', 'degree', 'sweet', 'acidity', 'body', 'tannin', 'price', 'year', 'ml', 'url', 'wineid', 'grade'])
    # print(data.head(3))
    
    data[['nation','nation2']] = data['nation'].str.split('(', n=1, expand=True)
    data.drop(columns='nation2', inplace=True)
    
    return data

def mysql(userid, wineid):  
    with open(parent_dir + '/mydb.dat', mode='rb') as obj:
        config = pickle.load(obj)
    
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
        sql = "select grade from wine_grade where userid = {} and wineid = {}".format(userid, wineid)
        cursor.execute(sql)
        result = cursor.fetchone()

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    
    return result

def mystarcount(userid):  
    with open(parent_dir + '/mydb.dat', mode='rb') as obj:
        config = pickle.load(obj)
    
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
        sql = "select wineid, grade from wine_grade where userid = {}".format(userid)
        cursor.execute(sql)
        result = cursor.fetchall()

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    
    return result

def distance(df, userid):
    # print(current_path)
    with open(parent_dir + '/mydb.dat', mode='rb') as obj:
        config = pickle.load(obj)
    
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
        sql = "select wineid from wine_grade where userid=%s and grade=(select max(grade) from wine_grade where userid=%s)"
        cursor.execute(sql, (userid, userid))
        targetno = cursor.fetchall()

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    
    try:
        # 필요 없는 칼럼 지움
        feature = df.iloc[:,4:15]
        feature.drop(columns=['food','degree'], inplace=True)
        
        choice = random.choice(targetno)
        choice = choice[0]
        target = df.index[(df['id']==choice)]
    
        pd.set_option('display.max_columns', 21)
        pd.set_option('display.max_seq_items', 100)
    
        print('feature 요약')
        print(feature.head())
        
        transform = make_column_transformer((OneHotEncoder(), ['nation','varieties','type']), remainder=StandardScaler())
        transform.fit(feature)
        x_feature = transform.transform(feature)
     
        def dist(x, y):
            a = (np.array(x)-np.array(y))**2
            return np.sqrt(a.sum(axis=1))
        
        xf = pd.DataFrame(x_feature.toarray())
        xft = pd.DataFrame(x_feature[target].toarray())
        distdf = dist(xf,xft)
        # print('길이')
        # print(len(c))
    
        # print(df['distance'])
        distance=pd.DataFrame({'distance':distdf})
        print(distance)
        # print(feature[10:15])
        
        return distance
    
    except:
        return 0
    

def postpro(rawdf):
    nation = ['프랑스','이탈리아','미국','칠레','스페인','호주','아르헨티나','독일','뉴질랜드','남아프리카','포르투갈','오스트리아']
    
    # nation 13개
    # France          6643
    # Italy           4133
    # U.S.A           2677
    # Chile           1915
    # Spain           1625
    # Australia       1417
    # Argentina        521
    # Germany          405
    # New Zealand      297
    # South Africa     293
    # Portugal         229
    # Austria          105
    # 기타
    
    varieties = ['Cabernet Sauvignon', 'Pinot Noir', 'Chardonnay', 'Merlot', 'Syrah/Shiraz', 'Sangiovese', 'Sauvignon Blanc', 'Tempranillo',
                 'Blend', 'Grenache', 'Riesling', 'Nebbiolo', 'Moscato', 'Malbec', 'Carmenere', 'Zinfandel']
    
    # variety 17개
    # Cabernet Sauvignon              2777
    # Pinot Noir                      2548
    # Chardonnay                      2517
    # Merlot                          1575
    # Syrah/Shiraz                    1378
    # Sangiovese                       849
    # Sauvignon Blanc                  728
    # Tempranillo                      588
    # Blend                            538
    # Grenache                         530
    # Riesling                         462
    # Nebbiolo                         430
    # Moscato                          337
    # Malbec                           301
    # Carmenere                        239
    # Zinfandel                        185
    # 기타품종
    
    type = ['레드','화이트','스파클링','로제','주정강화','고도주']
    
    # type 7개
    # 레드        13197
    # 화이트        5267
    # 스파클링       1561
    # 로제          324
    # 주정강화        152
    # 고도주          76
    # 기타           57
    
    # 총 43개
                
    def postnation(values):
        if values not in nation:
            return '기타국가'
        return values
    rawdf['nation'] = rawdf['nation'].apply(postnation)   
    
    def postvar(values):
        try:
            values = re.findall('\(([^)]+)', values)   #  첫번째 괄호 안에 있는 문자 추출
            values = values[0]
            if values not in varieties:
                return 'etc'
            return values
        except:
            pass
        
    rawdf['varieties'] = rawdf['varieties'].apply(postvar)
    
    def posttype(values):
        if values not in type:
            values='기타'
        return values
    rawdf['type'] = rawdf['type'].apply(posttype)
    
    def postabv(values):
        if values != '0':
            # values에 ~ 이 있을때 앞에거 0번째
            # ~이 없을때 % 앞에 글자.
            values = re.sub(r'[^\w]', r' ', values)
            values = values.split(sep=' ')[0]
        return values
    rawdf['abv'] = rawdf['abv'].apply(postabv)
    rawdf['abv'] = rawdf['abv'].astype(dtype='int')
    
    abvmean = round(rawdf['abv'].mean())
    def zeroabv(values):
        if values == 0:
            values = abvmean            
        return values
    rawdf['abv'] = rawdf['abv'].apply(zeroabv)    
        
    def postprice(values):
        if values == 0:
            values = round(rawdf['price'].mean())
        return values
    rawdf['price'] = rawdf['price'].apply(postprice)
    
    return rawdf

# 딥러닝 예상별점 코드
def deep(postdata, pid):
          
    df=postdata[['id','varieties','type','nation','abv','sweet','acidity','body','tannin']]
    star = df.drop(columns=['id'])
    star = star.fillna('etc')
    # print(star.info())
    transform = make_column_transformer((OneHotEncoder(handle_unknown = 'ignore'), ['nation','varieties','type']), remainder=MinMaxScaler()) # remainder='passthrough'는 
    transform.fit(star)
    x_feature = transform.transform(star)
    # print(x_feature.shape)
    try:
        model = tf.keras.models.load_model(parent_dir +'\model'+str(pid)+'.h5')
    
        predstar = model.predict(x_feature)
        predstardf = pd.DataFrame(predstar, columns=['predstar'])
        # print('예측값 :', predstar.ravel())
        
        return predstardf
    except:
        pass

def modeling(pid):
    data = sql()
    postdata = postpro(data)
    mydata =  pd.DataFrame(mystarcount(pid), columns=['wineid', 'grade'])
    
    postdata=postdata[['id','varieties','nation','type','abv','sweet','acidity','body','tannin']]
    postdata = postdata.fillna('etc')
    df_LEFT_JOIN = pd.merge(postdata, mydata, left_on='id', right_on='wineid', how='right')
    star = df_LEFT_JOIN.dropna()
    
    star = star.drop(columns=['wineid'])
    postdata = postdata.drop(columns=['id'])
    
    feature = star.iloc[:,1:-1]
    # print('모델링feature', feature.info())
    label = star.iloc[:,-1].values
    try:
        # 원핫인코딩
        transform = make_column_transformer((OneHotEncoder(), ['nation','varieties','type']), remainder=MinMaxScaler())
        transform.fit(postdata)
        x_feature = transform.transform(feature)
        
        # print(x_feature.shape)
        # print('Sequential api 구성')
        model = Sequential()
        model.add(Dense(units=48, activation='linear', input_shape=x_feature.shape[1:]))
        model.add(Dropout(0.2)) # 드롭아웃 추가. 비율은 20%
        model.add(Dense(units=24, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(units=12, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(units=1, activation='linear'))
        
        model.compile(optimizer='adam', loss='mse', metrics=['mse'])
    
        history = model.fit(x=x_feature, y=label, epochs=300, batch_size=1, verbose=2)
        model.save(parent_dir +'/model'+str(pid)+'.h5')
    except:
        pass