from django.shortcuts import render, redirect

# Create your views here.
from frame.error import ErrorCode
from frame.userdb import UsersDB

def home(request):
    return render(request, 'index.html')
def login(request):
    return render(request, 'login.html')
def index(request):
    return render(request, 'index.html')
def elements(request):
    return render(request, 'elements.html')
def generic(request):
    return render(request, 'generic.html')
def register(request):
    return render(request, 'register.html')

# register
def useraddimpl(request):
    # id, pwd, name 을 입력 받아 데이터베이스에 입력 하고
    user_id = request.POST['user_id'];
    pwd = request.POST['pwd'];
    name = request.POST['name'];
    email = request.POST['email'];
    phone = request.POST['phone'];
    try:
        UsersDB().insert(user_id,pwd,name,email,phone);
    except:
        context = { 'msg': ErrorCode.e0001};
        return render(request, 'error.html',context);
    # 조회 화면으로 이동 한다.
    return redirect('index');

# login
def loginimpl(request):
    user_id = request.POST['user_id'];
    pwd = request.POST['pwd'];
    next = 'loginimpl.html';
    try:
        user = UsersDB().selectone(user_id);
        if pwd == user.pwd:
            # 로그 아웃하기 전까지
            request.session['loginuser'] =  {'id':user.user_id,'name':user.name};
            context = None;
        else:
          raise Exception;
    except:
        context = { 'msg':ErrorCode.e0003 };
        next = 'error.html';
    return render(request, next, context);
# logout
def logout(request):
    if request.session['loginuser'] != None:
        del request.session['loginuser'];
    return render(request,'index.html');

# userinfo
def userinfo(request):
    # user_id = request.GET['user_id'];
    # user = UsersDB().selectone(user_id);
    # context = {'u': user};
    # return render(request, 'userinfo.html', context);
    return render(request,'userinfo.html')

def userdelete(request):
    user_id = request.GET['user_id'];
    UsersDB().delete(user_id);
    return redirect('index.html');

def userupdate(request):
    user_id = request.GET['user_id'];
    cust = UsersDB().selectone(user_id);
    context = {'c': cust};
    return render(request, 'userupdate.html', context);
