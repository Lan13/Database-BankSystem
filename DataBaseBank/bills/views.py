from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AccountBillsForm
from .models import AccountBills
from accounts.models import UserAccounts
from django.core.paginator import Paginator
from django.contrib import messages
from users.models import BankUser


# Create your views here.
@login_required
def create_bill(request, account_id):
    account = UserAccounts.objects.get(account_id=account_id)
    # judge if the user is the owner of the account
    user_id = BankUser.objects.get(id=account.user_id).user_id
    if request.user.id != user_id:
        messages.error(request, '无法为他人账户创建账单')
        return render(request, 'frontend/error.html')
    if request.method != 'POST':
        form = AccountBillsForm(initial={'account': account})
    else:
        form = AccountBillsForm(initial={'account': account}, data=request.POST)
        if form.is_valid():
            old_money = account.money
            changes = form.cleaned_data.get("changes")
            bill_type = form.cleaned_data.get("type")
            remark = form.cleaned_data.get("remark")
            new_money = old_money + changes
            if new_money < 0:
                messages.error(request, '余额不足')
                return render(request, 'frontend/error.html')
            bill = AccountBills.objects.create(account=account, changes=changes,
                                               type=bill_type, remark=remark, money=new_money)
            bill.save()
            # 触发器，自动更新账户余额
            account.money = new_money
            account.save()
            return redirect('bills:bills', account_id=account.account_id)
    context = {'form': form, 'account': account}
    return render(request, 'bills/create_bill.html', context)


@login_required
def bills(request, account_id):
    account = UserAccounts.objects.get(account_id=account_id)
    # judge if the user is the owner of the account
    user_id = BankUser.objects.get(id=account.user_id).user_id
    if request.user.id != user_id:
        messages.error(request, '无法查看他人账单')
        return render(request, 'frontend/error.html')
    bills_lists = AccountBills.objects.filter(account_id=account_id)
    paginator = Paginator(bills_lists, 4)
    page = request.GET.get('page')
    bills_list = paginator.get_page(page)
    context = {'bills': bills_list, 'account': account}
    return render(request, 'bills/bills.html', context)
