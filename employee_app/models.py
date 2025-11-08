from django.db import models

# Create your models here.
class StatusModel(models.Model):
    status_name = models.CharField(verbose_name="Status", max_length=255, unique=True, blank=False, null=True)
    def __str__(self):
        return self.status_name
    
class PositionModel(models.Model):
    position_name = models.CharField(verbose_name="Position", max_length=255, blank=False, null=False, unique=True)
    salary = models.IntegerField(verbose_name="salary")
    def __str__(self):
        return self.position_name

class EmployeeModel(models.Model):
    name = models.CharField(verbose_name="name", max_length=255, blank=False, null=False, unique=True)
    address = models.TextField(verbose_name="address")
    manager = models.BooleanField(verbose_name="manager", default=False)
    position = models.ForeignKey(verbose_name="position", to='PositionModel', on_delete=models.SET_NULL,  blank=False, null=True)
    status = models.ForeignKey(verbose_name="status", to='StatusModel', on_delete=models.SET_NULL,  blank=False, null=True)
    image = models.ImageField(verbose_name="image", upload_to="image", blank=False, null=True)
    department = models.ForeignKey(verbose_name="department", to='DepartmentModel', on_delete=models.SET_NULL,  blank=False, null=True)
    def __str__(self):
        return self.name

class DepartmentModel(models.Model):
    department_name = models.CharField(verbose_name="Department", max_length=255, blank=False, null=False, unique=True)
    manager = models.OneToOneField(verbose_name="manager", to='EmployeeModel', on_delete=models.SET_NULL,  blank=False, null=True)
    def __str__(self):
        return self.department_name


