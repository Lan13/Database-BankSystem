from django import forms
from .models import AccountBills
from accounts.models import UserAccounts


class AccountBillsForm(forms.ModelForm):
    bill_type = [
        ('收入', '收入'),
        ('支出', '支出'),
    ]
    account = forms.ModelChoiceField(label='账户信息', queryset=UserAccounts.objects.all(), disabled=True)
    changes = forms.FloatField(label='金额')
    type = forms.ChoiceField(label='类型', choices=bill_type)
    remark = forms.CharField(label='备注', required=False)

    class Meta:
        model = AccountBills
        fields = ('account', 'changes', 'type', 'remark')
