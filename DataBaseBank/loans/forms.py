from django import forms
from .models import Loans
from branch.models import BankBranch
from users.models import BankUser
from accounts.models import UserAccounts


class LoanForm(forms.ModelForm):
    user = forms.ModelChoiceField(label='客户信息', queryset=BankUser.objects.all(), disabled=True)
    branch = forms.ModelChoiceField(label='所属分行', queryset=BankBranch.objects.all(), disabled=True)
    money = forms.FloatField(label='借贷金额', min_value=0.0)

    class Meta:
        model = Loans
        fields = ('user', 'branch', 'money')


class PayForm(forms.ModelForm):
    loan = forms.ModelChoiceField(label='贷款信息', queryset=Loans.objects.all(), disabled=True)
    user = forms.ModelChoiceField(label='客户信息', queryset=BankUser.objects.all(), disabled=True)
    branch = forms.ModelChoiceField(label='所属分行', queryset=BankBranch.objects.all(), disabled=True)
    account = forms.ModelChoiceField(label='账户信息', queryset=UserAccounts.objects.none())
    money = forms.FloatField(label='还款金额', min_value=0.0)

    class Meta:
        model = Loans
        fields = ('loan', 'user', 'branch', 'account', 'money')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs['initial']['user']
        self.fields['account'].queryset = UserAccounts.objects.filter(user_id=user.id)
