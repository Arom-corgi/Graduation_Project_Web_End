from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from index.forms import *


# Create your views here.
def index(request):
    return render(request, 'index.html')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # 用户录入数据库
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # 登陆验证
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{username}账号创建成功，已自动登录跳转至主页')
                return redirect('index')
            else:
                # 不太可能发生的情况,用户刚才被创建
                messages.error(request, '自动登录失败，请手动登录')
                return redirect('user_login')
        else:
            # 表单数据无效的情况
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = UserRegisterForm()
    return render(request, 'user_register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 登陆验证
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '登陆成功，已自动登录跳转至主页')
                return redirect('index')
        else:
            # 表单数据无效的情况
            messages.error(request, '用户名或密码不正确')
    else:
        form = UserLoginForm()
    return render(request, 'user_login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, '您已成功登出')
    redirect('index')
