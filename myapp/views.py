from django.shortcuts import render, redirect
from myapp.models import WineUser, WineGrade, Wine
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login


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
        
        if not(login_id and login_pwd):
            lo_error['err']="아이디와 비밀번호를 모두 입력해주세요"
        else:
            
            wine_user = WineUser.objects.get(id=login_id)
            # if wine_user == 0:
            #     return render(request, "err.html")
            if check_password(login_pwd, wine_user.pwd): # 비번이 일치하면
                request.session['WineUser'] = wine_user.id
                return redirect('/')
            else:   # 비번이 일치하지 않으면
                lo_error['err'] = "비밀번호를 틀렸습니다."
                
                
                
    return render(request, "err.html")
                
def err(request):
    return render(request, 'err.html')
    
def logout(request):
    request.session.flush()
    return redirect('/')

def winelist(request):
    winedata = Wine.objects.all()
    for w in winedata:
        rs = w.nation.split(sep='-')
        print(rs[0])
    return render(request, 'winelist.html', {'winedata':winedata, 'rs': rs[0]})

def grade(request):
    if request.method == "POST":
        grade = request.POST.get('rating')
        id = request.POST.get('id')
        print(id)
        print(grade)
        userid = WineUser.objects.get(id=id)
        wineid = Wine.objects.get(id=137203)
        WineGrade(
            wu = userid,
            wine = wineid,
            grade = grade
                ).save()
        redirect('/')
    
    return render(request, 'grade.html', {'grade':grade})