from django.test import TestCase
from ..models import *

class StatusTestCase(TestCase):
    def setUp(self):
        StatusModel.objects.create(status_name="test").save()

    def test_after_add_status_model(self):
        self.assertEqual(StatusModel.objects.last().status_name, "test")

    def test_modify_status_model(self):
        statusModel = StatusModel.objects.last()
        statusModel.status_name = 'test2'
        statusModel.save()
        statusModel.refresh_from_db()
        self.assertEqual(statusModel.status_name, "test2")
    
    def test_delete_status_model(self):
        statusModel = StatusModel.objects.last()
        statusModel.delete()
        self.assertEqual(StatusModel.objects.count(), 0)

class PositionTestCase(TestCase):
    def setUp(self):
        PositionModel.objects.create(position_name="Python developer", salary=45000).save()

    def test_after_add_position_model(self):
        positionModel = PositionModel.objects.last()
        self.assertEqual(positionModel.position_name, "Python developer")
        self.assertEqual(positionModel.salary, 45000)

    def test_modify_salary_position_model(self):
        positionModel = PositionModel.objects.last()
        positionModel.salary = 50000
        positionModel.save()
        positionModel.refresh_from_db()
        self.assertEqual(positionModel.position_name, "Python developer")
        self.assertEqual(positionModel.salary, 50000)

    def test_modify_position_name_position_model(self):
        positionModel = PositionModel.objects.last()
        positionModel.position_name = "Odoo"
        positionModel.save()
        positionModel.refresh_from_db()
        self.assertEqual(positionModel.position_name, "Odoo")
        self.assertEqual(positionModel.salary, 45000)

    def test_delete_position_model(self):
        positionModel = PositionModel.objects.last()
        positionModel.delete()
        self.assertEqual(PositionModel.objects.count(), 0)


class DepartmentTestCase(TestCase):
    def setUp(self):
        employeeModel = EmployeeModel.objects.create(name="test", address="test", manager=True)
        employeeModel.save()
        employeeModel.refresh_from_db()
        DepartmentModel.objects.create(department_name="test", manager_id=employeeModel.pk).save()

    def test_after_add_department_model(self):
        departmentModel = DepartmentModel.objects.last()
        self.assertEqual(departmentModel.department_name, "test")
        self.assertEqual(departmentModel.manager.name, "test")
        self.assertEqual(departmentModel.manager.address, "test")

    def test_modify_department_model(self):
        departmentModel = DepartmentModel.objects.last()
        departmentModel.department_name = 'test2'
        departmentModel.save()
        departmentModel.refresh_from_db()
        self.assertEqual(departmentModel.department_name, "test2")
        self.assertEqual(departmentModel.manager.name, "test")
        self.assertEqual(departmentModel.manager.address, "test")

    def test_modify_manager_department_model(self):
        employeeModel = EmployeeModel.objects.last()
        employeeModel.name = 'test2'
        employeeModel.save()
        departmentModel = DepartmentModel.objects.last()
        self.assertEqual(departmentModel.department_name, "test")
        self.assertEqual(departmentModel.manager.name, "test2")
        self.assertEqual(departmentModel.manager.address, "test")
    
    def test_delete_department_model(self):
        departmentModel = DepartmentModel.objects.last()
        departmentModel.delete()
        self.assertEqual(DepartmentModel.objects.count(), 0)
        self.assertEqual(EmployeeModel.objects.count(), 1)

    def test_delete_employee_model(self):
        employeeModel = EmployeeModel.objects.last()
        departmentModel = DepartmentModel.objects.filter(manager_id = employeeModel.pk).first()
        self.assertEqual(departmentModel.manager.id, employeeModel.pk)
        employeeModel.delete()
        departmentModel.refresh_from_db()
        self.assertEqual(EmployeeModel.objects.count(), 0)
        self.assertEqual(DepartmentModel.objects.count(), 1)
        self.assertEqual(departmentModel.manager, None)


class EmployeeTestCase(TestCase):
    def setUp(self):
        positionModel = PositionModel.objects.create(position_name="Python developer", salary=45000)
        positionModel.save()
        positionModel.refresh_from_db()
        statusModel = StatusModel.objects.create(status_name="onboarding")
        statusModel.save()
        statusModel.refresh_from_db()
        employeeModelManger = EmployeeModel.objects.create(name="manager", address="test manager", manager=True, position_id = positionModel.pk, status_id = statusModel.pk)
        employeeModelManger.save()
        employeeModelManger.refresh_from_db()
        departmentModel = DepartmentModel.objects.create(department_name="IT", manager_id=employeeModelManger.pk)
        departmentModel.save() 
        departmentModel.refresh_from_db()
        employeeModelManger.department_id = departmentModel.pk
        employeeModelManger.save()
        employeeModelEmplpyee = EmployeeModel.objects.create(name="employee", address="test employee", manager=False, position_id = positionModel.pk, status_id = statusModel.pk, department_id = departmentModel.pk)
        employeeModelEmplpyee.save()

    def test_after_create_employee_model(self):
        employeeModel = EmployeeModel.objects.last()
        self.assertEqual(employeeModel.name, "employee")
        self.assertEqual(employeeModel.address, "test employee")
        self.assertEqual(employeeModel.manager, False)
        self.assertEqual(employeeModel.position.position_name, "Python developer")
        self.assertEqual(employeeModel.position.salary, 45000)
        self.assertEqual(employeeModel.status.status_name, "onboarding")
        self.assertEqual(employeeModel.department.department_name, "IT")
        self.assertEqual(employeeModel.department.manager.name, "manager")
        self.assertEqual(employeeModel.department.manager.manager, True)

    # Modify scope
    def test_modify_name_employee_model(self):
        employeeModel = EmployeeModel.objects.last()
        employeeModel.name = 'employee 1'
        employeeModel.save()
        employeeModel.refresh_from_db()
        self.assertEqual(employeeModel.name, 'employee 1')
        self.assertEqual(employeeModel.address, "test employee")
        self.assertEqual(employeeModel.manager, False)
        self.assertEqual(employeeModel.position.position_name, "Python developer")
        self.assertEqual(employeeModel.position.salary, 45000)
        self.assertEqual(employeeModel.status.status_name, "onboarding")
        self.assertEqual(employeeModel.department.department_name, "IT")
        self.assertEqual(employeeModel.department.manager.name, "manager")
        self.assertEqual(employeeModel.department.manager.manager, True)

    def test_modify_position_employee_model(self):
        positionModel = PositionModel.objects.last()
        positionModel.position_name = "Odoo"
        positionModel.save()
        employeeModel = EmployeeModel.objects.last()
        self.assertEqual(employeeModel.name, 'employee')
        self.assertEqual(employeeModel.address, "test employee")
        self.assertEqual(employeeModel.manager, False)
        self.assertEqual(employeeModel.position.position_name, "Odoo")
        self.assertEqual(employeeModel.position.salary, 45000)
        self.assertEqual(employeeModel.status.status_name, "onboarding")
        self.assertEqual(employeeModel.department.department_name, "IT")
        self.assertEqual(employeeModel.department.manager.name, "manager")
        self.assertEqual(employeeModel.department.manager.manager, True)

    
    def test_modify_status_employee_model(self):
        statusModel = StatusModel.objects.last()
        statusModel.status_name = "Doing"
        statusModel.save()
        employeeModel = EmployeeModel.objects.last()
        self.assertEqual(employeeModel.name, 'employee')
        self.assertEqual(employeeModel.address, "test employee")
        self.assertEqual(employeeModel.manager, False)
        self.assertEqual(employeeModel.position.position_name, "Python developer")
        self.assertEqual(employeeModel.position.salary, 45000)
        self.assertEqual(employeeModel.status.status_name, "Doing")
        self.assertEqual(employeeModel.department.department_name, "IT")
        self.assertEqual(employeeModel.department.manager.name, "manager")
        self.assertEqual(employeeModel.department.manager.manager, True)

    
    def test_modify_department_employee_model(self):
        departmentModel = DepartmentModel.objects.last()
        departmentModel.department_name = "Odoo"
        departmentModel.save()
        employeeModel = EmployeeModel.objects.last()
        self.assertEqual(employeeModel.name, 'employee')
        self.assertEqual(employeeModel.address, "test employee")
        self.assertEqual(employeeModel.manager, False)
        self.assertEqual(employeeModel.position.position_name, "Python developer")
        self.assertEqual(employeeModel.position.salary, 45000)
        self.assertEqual(employeeModel.status.status_name, "onboarding")
        self.assertEqual(employeeModel.department.department_name, "Odoo")
        self.assertEqual(employeeModel.department.manager.name, "manager")
        self.assertEqual(employeeModel.department.manager.manager, True)


    #Delete Scope
    def test_delete_employee_model(self):
        self.assertEqual(EmployeeModel.objects.count(), 2)
        employeeModel = EmployeeModel.objects.filter(name="employee")
        employeeModel.delete()
        self.assertEqual(EmployeeModel.objects.count(), 1)
        self.assertEqual(DepartmentModel.objects.count(), 1)
        self.assertEqual(StatusModel.objects.count(), 1)
        self.assertEqual(PositionModel.objects.count(), 1)
        employeeLast = EmployeeModel.objects.last()
        self.assertEqual(employeeLast.department.manager.name, "manager")
        self.assertEqual(employeeLast.department.manager.manager, True)

    
    def test_delete_manager_employee_model(self):
        self.assertEqual(EmployeeModel.objects.count(), 2)
        employeeModel = EmployeeModel.objects.filter(name="manager")
        employeeModel.delete()
        self.assertEqual(EmployeeModel.objects.count(), 1)
        self.assertEqual(DepartmentModel.objects.count(), 1)
        self.assertEqual(StatusModel.objects.count(), 1)
        self.assertEqual(PositionModel.objects.count(), 1)
        employeeModel = EmployeeModel.objects.all()
        employeeModelLast = employeeModel.last()
        employeeModelFirst = employeeModel.first()
        self.assertEqual(employeeModelLast.department.manager, None)
        self.assertEqual(employeeModelFirst.department.manager, None)

    
    def test_delete_position_employee_model(self):
        self.assertEqual(EmployeeModel.objects.count(), 2)
        self.assertEqual(DepartmentModel.objects.count(), 1)
        self.assertEqual(StatusModel.objects.count(), 1)
        PositionModel.objects.filter(position_name="Python developer").delete()
        self.assertEqual(PositionModel.objects.count(), 0)
        employeeModel = EmployeeModel.objects.all()
        employeeModelLast = employeeModel.last()
        employeeModelFirst = employeeModel.first()
        self.assertEqual(employeeModelLast.position, None)
        self.assertEqual(employeeModelFirst.position, None)

    def test_delete_status_employee_model(self):
        self.assertEqual(EmployeeModel.objects.count(), 2)
        self.assertEqual(DepartmentModel.objects.count(), 1)
        self.assertEqual(PositionModel.objects.count(), 1)
        statusModel = StatusModel.objects.filter(status_name = 'onboarding')
        statusModel.delete()
        self.assertEqual(StatusModel.objects.count(), 0)
        employeeModel = EmployeeModel.objects.all()
        employeeModelLast = employeeModel.last()
        employeeModelFirst = employeeModel.first()
        self.assertEqual(employeeModelLast.status, None)
        self.assertEqual(employeeModelFirst.status, None)

    def test_delete_department_employee_model(self):
        self.assertEqual(EmployeeModel.objects.count(), 2)
        self.assertEqual(PositionModel.objects.count(), 1)
        self.assertEqual(StatusModel.objects.count(), 1)
        departmentModel = DepartmentModel.objects.filter(department_name = 'IT')
        departmentModel.delete()
        self.assertEqual(DepartmentModel.objects.count(), 0)
        employeeModel = EmployeeModel.objects.all()
        employeeModelLast = employeeModel.last()
        employeeModelFirst = employeeModel.first()
        self.assertEqual(employeeModelLast.department, None)
        self.assertEqual(employeeModelFirst.department, None)

