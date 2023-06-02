from django.db import models
from department.models import BranchDepartments


# Create your models here.
class Staff(models.Model):
    objects = models.Manager()
    staff_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(BranchDepartments, on_delete=models.CASCADE, related_name='DepartmentStaff')
    name = models.CharField(max_length=20)
    tel = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/%Y%m%d/', default='photos/20230601/default.png')

    def __str__(self):
        return f"{self.staff_id}-{self.name}"


class Manager(models.Model):
    objects = models.Manager()
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='StaffManager', primary_key=True)
    department = models.ForeignKey(BranchDepartments, on_delete=models.CASCADE, related_name='DepartmentManager')

    def __str__(self):
        return f"{self.staff.name}-{self.department.name}"
