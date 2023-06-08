from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import BankUserLoginForm, BankUserRegisterForm, BankUserEditForm
from .models import BankUser


# Create your views here.
def bank_user_login(request):
    if request.method == 'POST':
        bank_user_login_form = BankUserLoginForm(data=request.POST)
        if bank_user_login_form.is_valid():
            data = bank_user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('frontend:index')
            else:
                return HttpResponse('账号或密码输入错误，请重新输入')
        else:
            return HttpResponse('账号或密码输入不合法，请重新输入')
    elif request.method == 'GET':
        bank_user_login_form = BankUserLoginForm()
        context = {'form': bank_user_login_form}
        return render(request, 'registration/login.html', context)


def bank_user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        register_form = BankUserRegisterForm(data=request.POST)
        if form.is_valid() and register_form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            id = register_form.cleaned_data.get("id")
            # # check if there is id
            # if BankUser.objects.filter(id=id):
            #     messages.error(request, '该身份证号码已被注册')
            #     return render(request, 'frontend/error.html')
            user = User.objects.create_user(username=username, password=password)
            name = register_form.cleaned_data.get("name")
            tel = register_form.cleaned_data.get("tel")
            address = register_form.cleaned_data.get("address")
            branch = register_form.cleaned_data.get("branch")
            bank_user = BankUser.objects.create(user=user, id=id, name=name,
                                                tel=tel, address=address, branch=branch)
            bank_user.save()
            login(request, user)
            return redirect('frontend:index')
        else:
            return HttpResponse('输入不合法或该用户名/身份证号码已注册')
    elif request.method == 'GET':
        form = UserCreationForm()
        register_form = BankUserRegisterForm()
        context = {'form': form, 'register_form': register_form}
        return render(request, 'registration/register.html', context)


@login_required
def change_pwd(request, user_id):
    # judge if the user is the owner
    user = User.objects.get(id=user_id)
    if user != request.user:
        messages.error(request, '无法修改他人密码')
        return render(request, 'frontend/error.html')
    if request.method != 'POST':
        form = PasswordChangeForm(user=request.user)

    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('frontend:index')
    context = {'form': form}
    return render(request, 'registration/change_pwd.html', context)


@login_required
def bank_user_edit(request, user_id):
    user = User.objects.get(id=user_id)
    info = BankUser.objects.get(user_id=user_id)
    if user != request.user and not request.user.is_superuser:
        messages.error(request, '无法修改他人信息')
        return render(request, 'frontend/error.html')

    if request.method != 'POST':
        form = BankUserEditForm(instance=info)
    else:
        form = BankUserEditForm(instance=info, data=request.POST)
        if form.is_valid():
            info.id = form.cleaned_data.get("id")
            info.name = form.cleaned_data.get("name")
            info.tel = form.cleaned_data.get("tel")
            info.address = form.cleaned_data.get("address")
            info.branch = form.cleaned_data.get("branch")
            info.save()
            return redirect('accounts:accounts', user_id=user_id)

    context = {'form': form, 'user_id': user_id}
    return render(request, 'registration/edit.html', context)


@login_required
def get_users(request):
    branch_name = None
    if request.user.is_superuser:
        branch_name = request.user.username
    if branch_name:
        users_lists = BankUser.objects.filter(branch_id=branch_name)
        paginator = Paginator(users_lists, 4)
        page = request.GET.get('page')
        users = paginator.get_page(page)
        context = {'users': users}
        return render(request, 'registration/get_users.html', context)
    else:
        messages.error(request, '无法查看信息')
        return render(request, 'frontend/error.html')
