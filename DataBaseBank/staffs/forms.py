from django import forms
from .models import Staff
from department.models import BranchDepartments


class StaffCreateForm(forms.ModelForm):
    department = forms.ModelChoiceField(label='所属部门', queryset=BranchDepartments.objects.all(), disabled=True)
    name = forms.CharField(label='姓名', max_length=20)
    tel = forms.CharField(label='电话', max_length=11)
    address = forms.CharField(label='地址', max_length=100)
    photo = forms.ImageField(label='照片', required=False)

    class Meta:
        model = Staff
        fields = ('department', 'name', 'tel', 'address', 'photo')


class StaffEditForm(forms.ModelForm):
    staff_id = forms.IntegerField(label='工号', disabled=True)
    department = forms.ModelChoiceField(label='所属部门', queryset=BranchDepartments.objects.all())
    name = forms.CharField(label='姓名', max_length=20)
    tel = forms.CharField(label='电话', max_length=11)
    address = forms.CharField(label='地址', max_length=100)
    photo = forms.ImageField(label='照片', required=False)

    class Meta:
        model = Staff
        fields = ('staff_id', 'department', 'name', 'tel', 'address')
