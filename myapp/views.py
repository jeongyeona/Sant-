from django.shortcuts import render, redirect
from myapp.models import WineUser, WineGrade, Wine
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import pandas as pd
from django.db.models import Avg
import pickle
import MySQLdb
import os

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
            wine_user = WineUser.objects.get(id=login_id)
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
        
        current_path = os.path.abspath(__file__) # 경로를 객체화
        
        parent_dir = os.path.dirname(current_path)
        
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
                print(diw)
                
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
        winedata = Wine.objects.all()
        wineid = request.GET.get('wineid')
        winedataid = Wine.objects.get(id=wineid)
        
        diw = request.session['WinePid']
        # print(diw)
        
        data = mysql(diw, wineid)
        if data:
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
    
    data[['nation','nation2']] = data['nation'].str.split(' -', n=1, expand=True)
    data.drop(columns='nation2')
    
    return data

def mysql(userid, wineid):  
    current_path = os.path.abspath(__file__) # 경로를 객체화
    
    parent_dir = os.path.dirname(current_path)
    
    print(current_path)
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