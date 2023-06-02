from django.shortcuts import render, redirect
from .models import Loans
from users.models import BankUser
from branch.models import BankBranch
from django.contrib import messages
from .forms import LoanForm, PayForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from accounts.models import UserAccounts
from bills.models import AccountBills


# Create your views here.
@login_required
def apply_loan(request, user_id):
    user = BankUser.objects.get(user_id=user_id)
    if request.user.id != user_id:
        messages.error(request, '无法为他人创建账户')
        return render(request, 'frontend/error.html')
    branch = BankBranch.objects.get(name=user.branch_id)
    if request.method != 'POST':
        form = LoanForm(initial={'user': user, 'branch': branch})
    else:
        form = LoanForm(initial={'user': user, 'branch': branch}, data=request.POST)
        if form.is_valid():
            money = form.cleaned_data.get("money")
            loan = Loans.objects.create(user=user, branch=branch, money=money, remain_money=money)
            loan.save()
            # 触发器，自动更新用户的状态
            user.status = False
            user.save()
            return redirect('loans:loans', user_id=user_id)
    context = {'form': form}
    return render(request, 'loans/apply_loan.html', context)


@login_required
def delete_loan(request, loan_id):
    loan = Loans.objects.get(loan_id=loan_id)
    user = BankUser.objects.get(id=loan.user_id)
    # judge if the user is the owner of the account
    if request.user.id != user.user_id:
        messages.error(request, '无法删除他人贷款')
        return render(request, 'frontend/error.html')
    if not loan or loan.status == '未还清':
        messages.error(request, '未还清贷款，无法删除贷款')
        return render(request, 'frontend/error.html')
    loan.delete()
    # if user has no loan, change the status to True
    if not Loans.objects.filter(user_id=user.id):
        user.status = True
        user.save()
    return redirect('loans:loans', user_id=user.user_id)


@login_required
def pay_loan(request, loan_id):
    loan = Loans.objects.get(loan_id=loan_id)
    user = BankUser.objects.get(id=loan.user_id)
    branch = BankBranch.objects.get(name=user.branch_id)
    accounts = UserAccounts.objects.filter(user_id=user.id)
    if request.user.id != user.user_id:
        messages.error(request, '无法为他人还款')
        return render(request, 'frontend/error.html')
    if request.method != 'POST':
        form = PayForm(initial={'loan': loan, 'user': user, 'branch': branch})
    else:
        form = PayForm(initial={'loan': loan, 'user': user, 'branch': branch}, data=request.POST)
        if form.is_valid():
            money = form.cleaned_data.get("money")
            account = form.cleaned_data.get("account")
            # if account has no enough money
            if account.money < money:
                messages.error(request, '账户余额不足')
                return render(request, 'frontend/error.html')
            loan.remain_money -= money
            if loan.remain_money < 0:
                messages.error(request, '还款金额超过贷款金额')
                return render(request, 'frontend/error.html')
            if loan.remain_money == 0:
                loan.status = '已还清'
            loan.save()
            # 修改账户余额
            account.money -= money
            account.save()
            remark = "还款" + str(loan.loan_id) + "号贷款"
            # 添加账单
            bill = AccountBills.objects.create(account=account, changes=-money,
                                               type='支出', remark=remark, money=account.money)
            bill.save()
            return redirect('loans:loans', user_id=user.user_id)
    context = {'form': form, 'loan': loan}
    return render(request, 'loans/pay_loan.html', context)


@login_required
def loans(request, user_id):
    user = BankUser.objects.get(user_id=user_id)
    if request.user.id != user_id:
        messages.error(request, '无法查看他人贷款信息')
        return render(request, 'frontend/error.html')
    loans_lists = Loans.objects.filter(user_id=user.id)
    paginator = Paginator(loans_lists, 4)
    page = request.GET.get('page')
    loans_list = paginator.get_page(page)
    context = {'loans': loans_list, 'loan_user': user}
    return render(request, 'loans/loans.html', context)
