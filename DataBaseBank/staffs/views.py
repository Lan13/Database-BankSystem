from django.shortcuts import render, redirect
from .models import Staff, Manager
from django.core.paginator import Paginator
from .forms import StaffEditForm, StaffCreateForm
from department.models import BranchDepartments
from django.contrib import messages


# Create your views here.
def staffs(request):
    staffs_lists = Staff.objects.all()
    paginator = Paginator(staffs_lists, 4)
    page = request.GET.get('page')
    staffs_list = paginator.get_page(page)
    context = {'staffs': staffs_list}
    return render(request, 'staffs/staffs.html', context)


def create_staff(request, department_id):
    # judge if user is superuser
    if not request.user.is_superuser:
        messages.error(request, '你没有权限创建员工')
        return render(request, 'frontend/error.html')
    department = BranchDepartments.objects.get(department_id=department_id)
    if request.method != 'POST':
        form = StaffCreateForm(initial={'department': department})
    else:
        form = StaffCreateForm(initial={'department': department}, data=request.POST, files=request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            tel = form.cleaned_data.get("tel")
            address = form.cleaned_data.get("address")
            staff = Staff.objects.create(department=department, name=name, tel=tel, address=address)
            if 'photo' in request.FILES:
                staff.photo = form.cleaned_data.get("photo")
            staff.save()
            return redirect('staffs:staffs')
    context = {'form': form, 'department': department}
    return render(request, 'staffs/create_staff.html', context)


def edit_staff(request, staff_id):
    # judge if user is superuser
    if not request.user.is_superuser:
        messages.error(request, '你没有权限修改员工信息')
        return render(request, 'frontend/error.html')
    staff = Staff.objects.get(staff_id=staff_id)
    old_department = staff.department
    if request.method != 'POST':
        form = StaffEditForm(instance=staff)
    else:
        form = StaffEditForm(instance=staff, data=request.POST, files=request.FILES)
        if form.is_valid():
            staff.department = form.cleaned_data.get("department")
            # if staff is the old department manager
            # and old department is not the new department, delete the manager
            if old_department != staff.department and Manager.objects.filter(department=old_department):
                manager = Manager.objects.get(staff=staff, department=old_department)
                manager.delete()
            staff.name = form.cleaned_data.get("name")
            staff.tel = form.cleaned_data.get("tel")
            staff.address = form.cleaned_data.get("address")
            if 'photo' in request.FILES:
                # if old photo is not default photo, then delete old photo
                if staff.photo and staff.photo.name != 'photos/20230601/default.png':
                    staff.photo.delete()
                staff.photo = form.cleaned_data.get("photo")
            staff.save()
            return redirect('staffs:staffs')
    context = {'form': form, 'staff': staff}
    return render(request, 'staffs/edit_staff.html', context)


def delete_staff(request, staff_id):
    # judge if user is superuser
    if not request.user.is_superuser:
        messages.error(request, '你没有权限删除员工')
        return render(request, 'frontend/error.html')
    staff = Staff.objects.get(staff_id=staff_id)
    # if staff is a manager, delete it
    if Manager.objects.filter(staff=staff):
        manager = Manager.objects.get(staff=staff)
        manager.delete()
    # if staff photo is not the default photo, delete staff photo
    if staff.photo and staff.photo.name != 'photos/20230601/default.png':
        staff.photo.delete()
    staff.delete()
    return redirect('staffs:staffs')


def set_manager(request, staff_id, department_id):
    # judge if user is superuser
    if not request.user.is_superuser:
        messages.error(request, '你没有权限设置经理')
        return render(request, 'frontend/error.html')
    staff = Staff.objects.get(staff_id=staff_id)
    department = BranchDepartments.objects.get(department_id=department_id)
    # if there is a manager in this department, delete it
    if Manager.objects.filter(department=department):
        manager = Manager.objects.get(department=department)
        manager.delete()
    # create a new manager
    manager = Manager.objects.create(department=department, staff=staff)
    manager.save()
    return redirect('departments:departments')


def delete_manager(request, department_id):
    # judge if user is superuser
    if not request.user.is_superuser:
        messages.error(request, '你没有权限删除经理')
        return render(request, 'frontend/error.html')
    department = BranchDepartments.objects.get(department_id=department_id)
    # if there is a manager in this department, delete it
    if Manager.objects.filter(department=department):
        manager = Manager.objects.get(department=department)
        manager.delete()
    return redirect('departments:departments')
