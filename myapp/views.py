from django.shortcuts import render, redirect
from myapp.models import WineUser, WineGrade, Wine
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

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
    if request.GET.get('search_key'):
        sk = 'search_key='
        search_key = request.GET.get('search_key')
        print(search_key)
        datas_search = Wine.objects.filter(name_kr__icontains=search_key).order_by('id')
        print(datas_search)
        
        page=request.GET.get("page", 1) # 페이지
        paginator=Paginator(datas_search, 6) # 페이지당 6개씩 보여주기
        page_obj = paginator.get_page(page)
        
        count = datas_search.count()
        count = '{:,}'.format(datas_search.count())

        
        for w in datas_search:
            rs = w.nation.split(sep='-')
            # print(rs[0])
                
        return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'rs': rs[0], 'sk':sk, 'search_key':search_key})
    
    elif request.GET.get('filterBtn'):
        if request.GET.get('filterBtn2'):
            list_check = request.GET.get('filterBtn')
            check_filter = Wine.objects.filter(type__icontains=list_check).order_by('id')
                
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(check_filter, 6) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            cb = '&filterBtn='
            
            for w in check_filter:
                rs = w.nation.split(sep='-')
                # print(rs[0])
            list_check2 = request.GET.get('filterBtn2')
            # print(list_check)
            # print(list_check2)
            check_filter2 = Wine.objects.filter(nation__icontains=list_check2).order_by('id')
            # print(check_filter2)
            result = check_filter & check_filter2 
            print(len(result))
            sql_query = str(result.query)
            print(sql_query)
                
            page=request.GET.get("page", 1) # 페이지
            paginator=Paginator(result, 6) # 페이지당 6개씩 보여주기
            page_obj = paginator.get_page(page)
            
            cf = '&filterBtn2='
            
            count = result.count()
            count = '{:,}'.format(result.count())
            
            for w in result:
                rs = w.nation.split(sep='-')
                # print(rs[0])
            return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'rs': rs[0], 'cb':cb, 'list_check':list_check, 'cf':cf, 'list_check2':list_check2})
    if request.GET.get('filterBtn'):
        list_check = request.GET.get('filterBtn')
        check_filter = Wine.objects.filter(type__icontains=list_check).order_by('id')
        page=request.GET.get("page", 1) # 페이지
        paginator=Paginator(check_filter, 6) # 페이지당 6개씩 보여주기
        page_obj = paginator.get_page(page)
        
        cb = '&filterBtn='
        
        count = check_filter.count()
        count = '{:,}'.format(check_filter.count())
        
        for w in check_filter:
                rs = w.nation.split(sep='-')
                # print(rs[0])
        
        return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'rs': rs, 'cb':cb, 'list_check':list_check})
    elif request.GET.get('filterBtn2'):
        list_check2 = request.GET.get('filterBtn2')
        check_filter2 = Wine.objects.filter(nation__icontains=list_check2).order_by('id')
        # print(check_filter2)

        page=request.GET.get("page", 1) # 페이지
        paginator=Paginator(check_filter2, 6) # 페이지당 6개씩 보여주기
        page_obj = paginator.get_page(page)
        
        cf = '&filterBtn2='
        
        count = check_filter2.count()
        count = '{:,}'.format(check_filter2.count())
        
        for w in check_filter2:
            rs = w.nation.split(sep='-')
            # print(rs[0])
            
        return render(request, 'winelist.html', {'count':count, 'question_list':page_obj, 'rs': rs[0], 'cf':cf, 'list_check2':list_check2})
    
    winedataall=Wine.objects.all().order_by("id")
    page=request.GET.get("page", 1) # 페이지
    paginator=Paginator(winedataall, 6) # 페이지당 6개씩 보여주기
    page_obj = paginator.get_page(page)
    
    count = winedataall.count()
    count = '{:,}'.format(winedataall.count())
    
    list=[]
    
    # for w in winedataall:
    #     for i in winedataall:
    #         rs = i.nation.split(sep='-')
    #         list.append(rs[0])
    #     print(list)
            
        return render(request, 'winelist.html', {'count':count, 'rs': list[0], 'question_list':page_obj})



def grade(request):
    if request.method == "GET":
        wine = request.GET.get('wineid')
        grade = request.GET.get('rating')
        id = request.GET.get('id')
        wine_user = WineUser.objects.get(id=id)
        print(wine_user.pid)
        print(id)
        print(wine)
        print(grade)
                
        import pickle
        import MySQLdb
        import os
        
        current_path = os.path.abspath(__file__) # 경로를 객체화
        
        parent_dir = os.path.dirname(current_path)
        
        print(current_path)
        with open(parent_dir + '/mydb.dat', mode='rb') as obj:
            config = pickle.load(obj)
        
        if WineGrade.iuser != wine_user.pid and WineGrade.iwine != wine:
            try:
                conn = MySQLdb.connect(**config)
                cursor = conn.cursor()
                sql = "INSERT INTO wine_grade(userid, wineid, grade) VALUES({},{},{})".format(wine_user.pid, wine, grade)
                count = cursor.execute(sql)
                print(count)
                conn.commit()
    
                return render(request, 'gradestar.html')
            except:
                sql = "UPDATE wine_grade SET grade={} WHERE wineid={} AND userid={}".format(grade, wine, wine_user.pid)
                count = cursor.execute(sql)
                print(count)
                conn.commit()
    
                return render(request, 'gradestar.html')
            finally:
                cursor.close()
                conn.close()
     
        return render(request, 'err.html')

def gradestar(request):
    return render(request, 'winelist.html')

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
                print(WineUser.objects.filter(nickname=name,
                                             id=id, email=email).exists())
                print('존재하는 회원입니다')
                # if wine_user == 0:
                #     return render(request, "err.html")
                return render(request, "pwdreset.html", {'id':id})
            else:
                print('false')
                lo_error['err'] = "비밀번호를 틀렸습니다."
                return render(request, "err.html")
    

def pwdsuc(request):
    err_data = {}
    id=request.POST.get('id')
    print(id)
    if request.method == "POST":
        new = request.POST.get('new')
        newok = request.POST.get('newok')
    
        if new != newok:
            err_data['error'] = "비밀번호가 틀립니다."
    
        else:
            wine_user = WineUser.objects.get(id=request.POST.get('id'))
            wine_user.pwd=make_password(new)
            wine_user.save()
            print(wine_user)
            return redirect("/")
    return render(request, 'err.html')

def addinfo(request):
    wine_user = WineUser.objects.all()
    wine = Wine.objects.all()
    wine_grade = WineGrade.objects.all()
    return render(request, 'addinfo.html', {'user':wine_user, 'wine':wine, 'grade':wine_grade})

def winedetail(request):
    if request.method == "GET":
        winedata = Wine.objects.all()
        wineid = request.GET.get('wineid')
        winedataid = Wine.objects.get(id=wineid)
    
    return render(request, 'winedetail.html', {'wineid':wineid,"winedataid":winedataid})

def pwderr(request):
    return render(request, 'pwderr.html')

def iderr(request):
    return render(request, 'iderr.html')