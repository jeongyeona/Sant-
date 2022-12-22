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
from sklearn.preprocessing import RobustScaler, MinMaxScaler
import random
import math

current_path = os.path.abspath(__file__) # 경로를 객체화
parent_dir = os.path.dirname(current_path)

# Create your views here.
def main(request):
    user_data = WineUser.objects.all()
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
    if request.method == "GET":
        
        if request.GET.get('filterBtn') and request.GET.get('filterBtn2') and request.GET.get('search_key'):
            print('all')
            search_key = request.GET.get('search_key')
            # print(search_key)
            datas_search = Wine.objects.filter(name_kr__icontains=search_key).order_by('id')
            # print(datas_search)
                
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(datas_search, 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            sk = '&search_key='
                
            list_check = request.GET.get('filterBtn')
            check_filter = Wine.objects.filter(type__icontains=list_check).order_by('id')
                        
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(check_filter, 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
                    
            cb = '&filterBtn='
                    
            list_check2 = request.GET.get('filterBtn2')
            # print(list_check)
            # print(list_check2)
            check_filter2 = Wine.objects.filter(nation__icontains=list_check2).order_by('id')
            # print(check_filter2)
            result = check_filter & check_filter2 & datas_search
            sql_query = str(result.query)
            print(sql_query)
            
            data = sql()
        
            data = data[data['name_kr'].str.contains(search_key)]
            data = data[data['type'].str.contains(list_check)]
            data = data[data['nation'].str.contains(list_check2)]

            # print(data)
                    
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(data.to_dict(orient='records'), 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
                 
            cf = '&filterBtn2='
                    
            count = result.count()
            count = '{:,}'.format(result.count())
                    
            return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'cb':cb, 'list_check':list_check, 'cf':cf, 'list_check2':list_check2, 'sk':sk, 'search_key':search_key})
    
            
        if request.GET.get('filterBtn') and request.GET.get('filterBtn2'):
            print('버튼1 & 버튼2')
            list_check = request.GET.get('filterBtn')
            check_filter = Wine.objects.filter(type__icontains=list_check).order_by('id')
                
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(check_filter, 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            cb = '&filterBtn='
            
            list_check2 = request.GET.get('filterBtn2')
            # print(list_check)
            # print(list_check2)
            check_filter2 = Wine.objects.filter(nation__icontains=list_check2).order_by('id')
            # print(check_filter2)
            result = check_filter & check_filter2 
            print(len(result))
            sql_query = str(result.query)
            print(sql_query)
            
            data = sql()
        
            data = data[data['type'].str.contains(list_check)]
            data = data[data['nation'].str.contains(list_check2)]

            # print(data)
            
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(data.to_dict(orient='records'), 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            cf = '&filterBtn2='
            
            count = result.count()
            count = '{:,}'.format(result.count())
            
            return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'cb':cb, 'list_check':list_check, 'cf':cf, 'list_check2':list_check2})
        
        if request.GET.get('search_key') and request.GET.get('filterBtn'):
            print('서치 & 버튼1')
            search_key = request.GET.get('search_key')
            # print(search_key)
            datas_search = Wine.objects.filter(name_kr__icontains=search_key).order_by('id')
            # print(datas_search)
                
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(datas_search, 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            sk = '&search_key='
                
            list_check = request.GET.get('filterBtn')
            check_filter = Wine.objects.filter(type__icontains=list_check).order_by('id')
                        
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(check_filter, 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
                    
            cb = '&filterBtn='
                    
            result = check_filter & datas_search
            sql_query = str(result.query)
            print(sql_query)
            
            data = sql()
        
            data = data[data['name_kr'].str.contains(search_key)]
            data = data[data['type'].str.contains(list_check)]
                 
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(data.to_dict(orient='records'), 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
                    
            count = result.count()
            count = '{:,}'.format(result.count())
                
            return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'sk':sk, 'search_key':search_key, 'cb':cb, 'list_check':list_check})
        
        if request.GET.get('search_key') and request.GET.get('filterBtn2'):
            print('서치 & 버튼2')
            search_key = request.GET.get('search_key')
            # print(search_key)
            datas_search = Wine.objects.filter(name_kr__icontains=search_key).order_by('id')
            # print(datas_search)
            
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(datas_search, 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            sk = '&search_key='
                    
            list_check2 = request.GET.get('filterBtn2')
            # print(list_check2)
            check_filter2 = Wine.objects.filter(nation__icontains=list_check2).order_by('id')
            # print(check_filter2)
            result = check_filter2 & datas_search
            sql_query = str(result.query)
            print(sql_query)
            
            data = sql()
        
            data = data[data['name_kr'].str.contains(search_key)]
            data = data[data['nation'].str.contains(list_check2)]
            # print(data)    
            
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(data.to_dict(orient='records'), 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
                 
            cf = '&filterBtn2='
                    
            count = result.count()
            count = '{:,}'.format(result.count())
                    
            return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'sk':sk, 'search_key':search_key, 'cf':cf, 'list_check2':list_check2})
        
        if request.GET.get('filterBtn'):
            list_check = request.GET.get('filterBtn')
            check_filter = Wine.objects.filter(type__icontains=list_check).order_by('id')
            
            data = sql()
            
            data = data[data['type'].str.contains(list_check)]
            
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(data.to_dict(orient='records'), 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            cb = '&filterBtn='
            
            count = check_filter.count()
            count = '{:,}'.format(check_filter.count())
            
            return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'cb':cb, 'list_check':list_check})
        
        if request.GET.get('search_key'):
            sk = 'search_key='
            search_key = request.GET.get('search_key')
            # print(search_key)
            datas_search = Wine.objects.filter(name_kr__icontains=search_key).order_by('id')
            # print(datas_search)
            
            data = sql()
            
            data = data[data['name_kr'].str.contains(search_key)]
            # print(data)
            
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(data.to_dict(orient='records'), 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            count = datas_search.count()
            count = '{:,}'.format(datas_search.count())
    
            return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'sk':sk, 'search_key':search_key})
        
        if request.GET.get('filterBtn2'):
            list_check2 = request.GET.get('filterBtn2')
            check_filter2 = Wine.objects.filter(nation__icontains=list_check2).order_by('id')
            # print(check_filter2)
                 
            data = sql()
            
            data = data[data['nation'].str.contains(list_check2)]
    
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(data.to_dict(orient='records'), 10) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            cf = '&filterBtn2='
            
            count = check_filter2.count()
            count = '{:,}'.format(check_filter2.count())
                
            return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'cf':cf, 'list_check2':list_check2})
    
        winedataall=Wine.objects.all().order_by("id")
        
        count = winedataall.count()
        count = '{:,}'.format(winedataall.count())
        
        data = sql()
        
        # distance 함수는 인코딩할 dataframe과 랜덤한 최고평점 와인의 인덱스를 파라미터로 받음 
        if request.session.get('WinePid'):
            ddata=distance(data, request.session.get('WinePid'))
            data=pd.merge(data, ddata)
            data = data.sort_values('distance')
            print('거리순 정렬')
            print(data[['id','distance']].head())
            data=data[1:11]
            
        print(data.head())
    
        page=request.GET.get("page", 1) # 페이지
        paginator=Paginator(data.to_dict(orient='records'), 10) # 페이지당 6개씩 보여주기
        page_obj = paginator.get_page(page)
        
        return render(request, 'winelist.html', {'count':count, 'question_list':page_obj})

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
        
        if WineGrade.userid != wine_user.pid and WineGrade.wineid != wine:
            try:
                conn = MySQLdb.connect(**config)
                cursor = conn.cursor()
                sql = "INSERT INTO wine_grade(userid, wineid, grade) VALUES({},{},{})".format(wine_user.pid, wine, grade)
                count = cursor.execute(sql)
                print(count)
                conn.commit()
                
                winedata = Wine.objects.all()
                winedataid = Wine.objects.get(id=wine)
                
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
                
                winedata = Wine.objects.all()
                winedataid = Wine.objects.get(id=wine)
                
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
    wine_user = WineUser.objects.all()
    wine = Wine.objects.all()
    wine_grade = WineGrade.objects.all()
    id = request.POST.get('myid')
    
    return render(request, 'addinfo.html', {'user':wine_user, 'wine':wine, 'grade':wine_grade})

def winedetail(request):
    if request.method == "GET":
        wineid = request.GET.get('wineid')
        winedataid = Wine.objects.get(id=wineid)
        
        data = []
        if request.session.get('WinePid'):
            diw = request.session['WinePid']
            # print(diw)
            
            data = mysql(diw, wineid)
            data = data[0]
    
    return render(request, 'winedetail.html', {'data':data, 'wineid':wineid,"winedataid":winedataid})

def pwderr(request):
    return render(request, 'pwderr.html')

def iderr(request):
    return render(request, 'iderr.html')

def sql():  
    current_path = os.path.abspath(__file__) # 경로를 객체화
    
    parent_dir = os.path.dirname(current_path)
    
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
    
    # for i, row in enumerate(df):
        # 국가 바꾸기
        # if df['nation'][i] not in nation:
        #     df['nation'][i]='기타국가'
        
        # 품종 바꾸기
        # items = re.findall('\(([^)]+)', df['varieties'][i])   #  첫번째 괄호 안에 있는 문자 추출
        # df['varieties'][i]=items[0]
        # if df['varieties'][i] not in varieties:
        #     df['varieties'][i]='etc'
        
        # type 바꾸기
        # if df['type'][i] not in type:
        #     df['type'][i]='기타'
           
        # 온도 바꾸기
        # if df['abv'][i][0] != '0':
        #     df['abv']=df['abv'].str.replace(pat=r'[^\w]', repl=r'', regex=True)
        # try:
        #     df['abv'][i] = df['abv'][i][0] + (df['abv'][i][1])
        # except:
        #     pass
        #

    def PostNation(values):
        if values not in nation:
            return '기타국가'
        return values
    df['nation'] = df['nation'].apply(PostNation)   
    
    def PostVar(values):
        try:
            values = re.findall('\(([^)]+)', values)   #  첫번째 괄호 안에 있는 문자 추출
            values = values[0]
            if values not in varieties:
                return 'etc'
            return values
        except:
            pass
        
    df['varieties'] = df['varieties'].apply(PostVar)
    
    def PostType(values):
        if values not in type:
            values='기타'
        return values
    df['type'] = df['type'].apply(PostType)
    
    def PostAbv(values):
        if values != '0':
            # values에 ~ 이 있을때 앞에거 0번째
            # ~이 없을때 % 앞에 글자.
            values = re.sub(r'[^\w]', r' ', values)
            values = values.split(sep=' ')[0]
        return values
    df['abv'] = df['abv'].apply(PostAbv)
    df['abv'] = df['abv'].astype(dtype='int')
    bb = round(df['abv'].mean())

    def ZeroAbv(values):
        if values == 0:
            values = bb            
        return values
    df['abv'] = df['abv'].apply(ZeroAbv)    
        
    def PostPrice(values):
        if values == 0:
            values = round(df['price'].mean())
        return values
    df['price'] = df['price'].apply(PostPrice)
    # food    
    # food = "0 chellfish dry fruit noodle chicken pig raisin bibimbap salami salad fish champagne cow asia sheep cheese cake fried pizza walnut"
    # tokenizer = Tokenizer()
    # tokenizer.fit_on_texts([food])
    # # print('단어 집합 :', tokenizer.word_index)
    # # 단어 집합 : {'chellfish': 1, 'dry': 2, 'fruit': 3, 'noodle': 4, 'chicken': 5, 'pig': 6, 'raisin': 7, 'bibimbap': 8, 'salami': 9, 'salad': 10, 'fish': 11, 'champagne': 12, 'cow': 13, 'asia': 14, 'sheep': 15, 'cheese': 16, 'cake': 17, 'fried': 18, 'pizza': 19, 'walnut': 20}
    #
    # for i, row in enumerate(df):
    #     food2 = df['food'][i].replace('food-','')
    #     # print(food2)
    #     encoded = tokenizer.texts_to_sequences([food2])[0]
    #     # print(encoded)
    #     one_hot = to_categorical(encoded)
    #     # print(one_hot)
    #     df['food'][i]=one_hot
    # print(df.nation.head())
    # print(df.varieties.head())
    # print(df.type.head())    
    # print(df.abv.head())
    # print(targetno)
    choice = random.choice(targetno)
    choice = choice[0]
    target = df.index[(df['id']==choice)]

    pd.set_option('display.max_columns', 21)
    pd.set_option('display.max_seq_items', 100)
    feature = df.iloc[:,4:15]
    
    feature.drop(columns=['food','degree'], inplace=True)
    print('feature 요약')
    print(feature.head())
    
    transform = make_column_transformer((OneHotEncoder(), ['nation','varieties','type']), remainder=RobustScaler()) # remainder='passthrough' 원핫 수행 후 다른 모든 칼럼까지 전부 표준화
    transform.fit(feature)
    x_feature = transform.transform(feature)
    # tar=x_feature[target].toarray()
    
    # df['target'] = np.NaN
    # df['feature'] = np.array(x_feature) # (20635, 41)
    # df['target'] = df['target'].fillna(x_feature[target])  # (0, 41)
    def dist(x, y):
        return np.sqrt(np.sum((x-y)**2))
    
    df['distance']= np.NaN
    print(x_feature[0])
    print(x_feature[target])
    for i, row in df.iterrows():
        df['distance'][i]=dist(x_feature[i].toarray(),x_feature[target].toarray())
        
    # def d(values):   # array를 넣어준다
    #     return dist(values, tar)
    # df['distance'] = x_feature.toarray().apply(d)

    # 판다스 시리즈에 적용하는 Haversine 벡터화 구현
    # df['distance'] = dist(df['feature'], df['target'])

    # print(df['distance'])
    print('대상과의 거리 0나와야함')
    print(df['distance'][target])
    print('거리 null값 갯수')
    print(df['distance'].isnull().sum())
    distance=df[['id', 'distance']]
    # print(feature[10:15])
    return distance