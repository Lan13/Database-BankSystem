from django.shortcuts import render
from .models import BranchDepartments
from django.core.paginator import Paginator
from staffs.models import Staff, Manager


# Create your views here.
def departments(request):
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
    staffs_lists = Staff.objects.filter(department_id=department_id)
    paginator = Paginator(staffs_lists, 4)
    page = request.GET.get('page')
    staffs_list = paginator.get_page(page)
    context = {'staffs': staffs_list}
    return render(request, 'departments/staffs.html', context)
