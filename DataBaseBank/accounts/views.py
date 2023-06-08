from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserAccountsForm, AccountsTransferForm
from .models import UserAccounts
from users.models import BankUser
from branch.models import BankBranch
from bills.models import AccountBills
from django.core.paginator import Paginator


# Create your views here.
@login_required
def create_account(request, user_id):
    user = BankUser.objects.get(user_id=user_id)
    if request.user.id != user_id:
        messages.error(request, '无法为他人创建账户')
        return render(request, 'frontend/error.html')
    branch = BankBranch.objects.get(name=user.branch_id)
    if request.method != 'POST':
        form = UserAccountsForm(initial={'user': user, 'branch': branch})
    else:
        form = UserAccountsForm(initial={'user': user, 'branch': branch}, data=request.POST)
        if form.is_valid():
            money = form.cleaned_data.get("money")
            account = UserAccounts.objects.create(user=user, branch=branch, money=money)
            account.save()
            # 触发器，自动更新用户的账户数
            user.counts = user.counts + 1
            user.save()
            # 账单
            bill = AccountBills.objects.create(account=account, changes=money,
                                               type='收入', remark="创建账户", money=money)
            bill.save()
            return redirect('accounts:accounts', user_id=user_id)
    context = {'form': form}
    return render(request, 'accounts/create_account.html', context)


# delete account
@login_required
def delete_account(request, account_id):
    account = UserAccounts.objects.get(account_id=account_id)
    user = BankUser.objects.get(id=account.user_id)
    # judge if the user is the owner of the account
    if request.user.id != user.user_id:
        messages.error(request, '无法删除他人账户')
        return render(request, 'frontend/error.html')
    if not account or account.money > 0:
        messages.error(request, '无法删除账户')
        return render(request, 'frontend/error.html')
    # 触发器，自动更新用户的账户数
    user.counts = user.counts - 1
    user.save()
    account.delete()
    return redirect('accounts:accounts', user_id=user.user_id)


# show accounts information
@login_required
def accounts(request, user_id):
    # judge if the user is the owner of the account
    if request.user.id != user_id and not request.user.is_superuser:
        messages.error(request, '无法查看他人账户')
        return render(request, 'frontend/error.html')
    account_user = BankUser.objects.get(user_id=user_id)
    accounts_lists = UserAccounts.objects.filter(user_id=account_user.id)
    paginator = Paginator(accounts_lists, 4)
    page = request.GET.get('page')
    accounts_list = paginator.get_page(page)
    context = {'accounts': accounts_list, 'account_user': account_user}
    return render(request, 'accounts/accounts.html', context)


# transfer money
@login_required
def transfer(request, account_id):
    account = UserAccounts.objects.get(account_id=account_id)
    user = BankUser.objects.get(id=account.user_id)
    # judge if the user is the owner of the account
    if request.user.id != user.user_id:
        messages.error(request, '无法使用他人账户')
        return render(request, 'frontend/error.html')
    if request.method != 'POST':
        form = AccountsTransferForm(initial={'account': account})
    else:
        form = AccountsTransferForm(initial={'account': account}, data=request.POST)
        if form.is_valid():
            money = form.cleaned_data.get("money")
            target_account = form.cleaned_data.get("target_account")
            # check if the account has enough money
            if account.money < money:
                messages.error(request, '余额不足')
                return render(request, 'frontend/error.html')
            # check if the target account exists
            if not UserAccounts.objects.filter(account_id=target_account.account_id):
                messages.error(request, '目标账户不存在')
                return render(request, 'frontend/error.html')
            account.money = account.money - money
            account.save()
            # 账单
            remark = "转账给" + target_account.user.name + "的" + str(target_account.account_id) + "账户"
            bill1 = AccountBills.objects.create(account=account, changes=-money,
                                                type='支出', remark=remark, money=account.money)
            bill1.save()

            target_account.money = target_account.money + money
            target_account.save()
            remark = "收到" + account.user.name + "的" + str(account.account_id) + "账户转账"
            bill2 = AccountBills.objects.create(account=target_account, changes=money,
                                                type='收入', remark=remark, money=target_account.money)
            bill2.save()
            return redirect('accounts:accounts', user_id=user.user_id)
    context = {'form': form, 'account': account}
    return render(request, 'accounts/transfer.html', context)
