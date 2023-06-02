from django import forms
from django.contrib.auth.models import User
from .models import BankUser
from branch.models import BankBranch


class BankUserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')


class BankUserRegisterForm(forms.ModelForm):
    id = forms.CharField(label='身份证号', strip=True, error_messages={'required': '身份证号不能为空。'})
    name = forms.CharField(label='姓名', strip=True, error_messages={'required': '姓名不能为空。'})
    tel = forms.CharField(label='电话号码', strip=True, error_messages={'required': '电话号码不能为空。'})
    address = forms.CharField(label='地址', strip=True, error_messages={'required': '地址不能为空。'})
    branch = forms.ModelChoiceField(label='所属分行', queryset=BankBranch.objects.all())

    class Meta:
        model = BankUser
        fields = ('id', 'name', 'tel', 'address', 'branch')


class BankUserEditForm(forms.ModelForm):
    id = forms.CharField(label='身份证号', strip=True, disabled=True)
    name = forms.CharField(label='姓名', strip=True, error_messages={'required': '姓名不能为空。'})
    tel = forms.CharField(label='电话号码', strip=True, error_messages={'required': '电话号码不能为空。'})
    address = forms.CharField(label='地址', strip=True, error_messages={'required': '地址不能为空。'})
    branch = forms.ModelChoiceField(label='所属分行', queryset=BankBranch.objects.all(), disabled=True)

    class Meta:
        model = BankUser
        fields = ('id', 'name', 'tel', 'address', 'branch')
