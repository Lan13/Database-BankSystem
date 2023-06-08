from django.contrib import messages
from django.shortcuts import render
from .models import BranchDepartments
from django.core.paginator import Paginator
from staffs.models import Staff, Manager


# Create your views here.
def departments(request):
    name = None
    if request.user.is_superuser:
        name = request.user.username
    if name:
        departments_lists = BranchDepartments.objects.filter(branch_id=name)
    else:
        departments_lists = BranchDepartments.objects.all()
    paginator = Paginator(departments_lists, 4)
    page = request.GET.get('page')
    departments_list = paginator.get_page(page)
    # get managers
    managers = Manager.objects.all()
    for department in departments_list:
        for manager in managers:
            if department.department_id == manager.department.department_id:
                department.manager = manager.staff
    context = {'departments': departments_list}
    return render(request, 'departments/departments.html', context)


def department_staffs(request, department_id):
    branch_name = None
    if request.user.is_superuser:
        branch_name = request.user.username
    branch = BranchDepartments.objects.get(department_id=department_id).branch_id
    if not (branch_name and branch_name == branch):
        messages.error(request, '你没有权限查看该部门员工')
        return render(request, 'frontend/error.html')
    staffs_lists = Staff.objects.filter(department_id=department_id)
    paginator = Paginator(staffs_lists, 4)
    page = request.GET.get('page')
    staffs_list = paginator.get_page(page)
    context = {'staffs': staffs_list}
    return render(request, 'departments/staffs.html', context)
