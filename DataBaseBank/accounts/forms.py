from django import forms
from .models import UserAccounts
from branch.models import BankBranch
from users.models import BankUser


class UserAccountsForm(forms.ModelForm):
    user = forms.ModelChoiceField(label='客户信息', queryset=BankUser.objects.all(), disabled=True)
    branch = forms.ModelChoiceField(label='所属分行', queryset=BankBranch.objects.all(), disabled=True)
    money = forms.FloatField(label='初始金额', min_value=0.0)

    class Meta:
        model = UserAccounts
        fields = ('user', 'branch', 'money')


class AccountsTransferForm(forms.ModelForm):
    account = forms.ModelChoiceField(label='转出账户', queryset=UserAccounts.objects.all(), disabled=True)
    target_account = forms.ModelChoiceField(label='转入账户', queryset=UserAccounts.objects.all())
    money = forms.FloatField(label='转账金额', min_value=0.0)

    class Meta:
        model = UserAccounts
        fields = ('account', 'target_account', 'money')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        account = kwargs['initial']['account']
        self.fields['target_account'].queryset = UserAccounts.objects.all().exclude(account_id=account.account_id)
