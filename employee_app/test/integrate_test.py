from django.test import TestCase, Client
from django.contrib.auth.models import User

class IntegrateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test"
        self.password = "password"
        User.objects.create_user(self.username, "test@test.com", self.password).save()

    def test_login_success(self):
        login_success = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login_success)

    def test_post_create_employee_if_user_logged_and_success(self):
        self.client.login(username=self.username, password=self.password)
        employee_create = self.client.post("/employee", data={"name": "test", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_create.status_code, 201)
        employee_list = self.client.get("/employee")
        self.assertEqual(employee_list.status_code, 200)
        self.assertEqual(employee_list.json(), [{'id': 1, 'name': 'test', 'address': 'test', 'manager': True, 'image': None, 'position': None, 'status': None, 'department': None}])

    def test_post_create_employee_if_user_logged_and_not_success(self):
        self.client.login(username=self.username, password=self.password)
        employee_create = self.client.post("/employee", data={}, content_type="application/json")
        self.assertEqual(employee_create.status_code, 400)
        employee_list = self.client.get("/employee")
        self.assertEqual(employee_list.status_code, 200)
        self.assertEqual(employee_list.json(), [])

    def test_get_employee_list_if_not_log_in(self):
        employee_list = self.client.get("/employee")
        self.assertEqual(employee_list.status_code, 302)
    
    def test_get_employee_list_if_use_other_method(self):
        employee_put = self.client.put("/employee")
        self.assertEqual(employee_put.status_code, 405)
        employee_delete = self.client.delete("/employee")
        self.assertEqual(employee_delete.status_code, 405)

    #Department
    def test_post_create_department_if_user_logged_and_success(self):
        self.client.login(username=self.username, password=self.password)
        department_create = self.client.post("/department", data={"department_name": "IT"}, content_type="application/json")
        self.assertEqual(department_create.status_code, 201)
        department_list = self.client.get("/department")
        self.assertEqual(department_list.json(), [{'id': 1, 'department_name': 'IT', 'manager':None}])
        self.assertEqual(department_list.status_code, 200)

    def test_post_create_department_if_user_logged_and_not_success(self):
        self.client.login(username=self.username, password=self.password)
        department_create = self.client.post("/department", data={}, content_type="application/json")
        self.assertEqual(department_create.status_code, 400)
        department_list = self.client.get("/department")
        self.assertEqual(department_list.json(), [])
        self.assertEqual(department_list.status_code, 200)

    def test_department_list_if_not_log_in(self):
        department_list = self.client.get("/department")
        self.assertEqual(department_list.status_code, 302)

    def test_get_department_list_if_use_other_method(self):
        department_put = self.client.put("/department")
        self.assertEqual(department_put.status_code, 405)
        department_delete = self.client.delete("/department")
        self.assertEqual(department_delete.status_code, 405)

    #Position
    def test_post_create_position_if_user_logged_and_success(self):
        self.client.login(username=self.username, password=self.password)
        position_create = self.client.post("/position", data={"position_name":"Python developer", "salary":50000}, content_type="application/json")
        self.assertEqual(position_create.status_code, 201)
        position_list = self.client.get("/position")
        self.assertEqual(position_list.json(), [{"id":1, "position_name":"Python developer", "salary":50000}])
        self.assertEqual(position_list.status_code, 200)

    def test_post_create_position_if_user_logged_and_not_success(self):
        self.client.login(username=self.username, password=self.password)
        position_create = self.client.post("/position", data={"position_name":"Python developer"}, content_type="application/json")
        self.assertEqual(position_create.status_code, 400)
        position_list = self.client.get("/position")
        self.assertEqual(position_list.json(), [])
        self.assertEqual(position_list.status_code, 200)

    def test_position_list_if_not_log_in(self):
        position_list = self.client.get("/position")
        self.assertEqual(position_list.status_code, 302)

    def test_get_position_list_if_use_other_method(self):
        position_put = self.client.put("/position")
        self.assertEqual(position_put.status_code, 405)
        position_delete = self.client.delete("/position")
        self.assertEqual(position_delete.status_code, 405)


    #Employee detail
    def test_get_employee_detail_with_logged_and_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        employee_detail = self.client.get('/employee/2')
        self.assertEqual(employee_detail.status_code, 404)
        employee_detail_put = self.client.put("/employee/1", data={"name": "test2", "address":"test", "manager":True})
        self.assertEqual(employee_detail_put.status_code, 404)
        employee_detail_delete = self.client.delete("/employee/1")
        self.assertEqual(employee_detail_delete.status_code, 404)

    def test_get_employee_detail_with_logged_and_exist(self):
        self.client.login(username=self.username, password=self.password)
        employee_create = self.client.post("/employee", data={"name": "test", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_create.status_code, 201)
        employee_detail = self.client.get('/employee/1')
        self.assertEqual(employee_detail.status_code, 200)
        self.assertEqual(employee_detail.json(), {"id": 1, "name": "test", "address":"test", "manager":True, 'image': None, 'position': None, 'status': None, 'department': None})

    def test_put_employee_detail_with_logged_in_and_success(self):
        self.client.login(username=self.username, password=self.password)
        employee_create = self.client.post("/employee", data={"name": "test", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_create.status_code, 201)
        employee_detail_put = self.client.put("/employee/1", data={"name": "test2", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_detail_put.status_code, 201)
        employee_detail = self.client.get("/employee/1")
        self.assertEqual(employee_detail.status_code, 200)
        self.assertEqual(employee_detail.json(), {"id": 1, "name": "test2", "address":"test", "manager":True, 'image': None, 'position': None, 'status': None, 'department': None})
        
    def test_put_employee_detail_with_logged_in_and_not_success(self):
        self.client.login(username=self.username, password=self.password)
        employee_create = self.client.post("/employee", data={"name": "test", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_create.status_code, 201)
        employee_detail_put = self.client.put("/employee/1", data={}, content_type="application/json")
        self.assertEqual(employee_detail_put.status_code, 400)
        employee_detail = self.client.get("/employee/1")
        self.assertEqual(employee_detail.status_code, 200)
        self.assertEqual(employee_detail.json(), {"id": 1, "name": "test", "address":"test", "manager":True, 'image': None, 'position': None, 'status': None, 'department': None})

    def test_put_employee_detail_but_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        employee_create = self.client.post("/employee", data={"name": "test", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_create.status_code, 201)
        employee_detail_put = self.client.put("/employee/2", data={"name": "test", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_detail_put.status_code, 404)
        employee_detail = self.client.get("/employee/1")
        self.assertEqual(employee_detail.status_code, 200)
        self.assertEqual(employee_detail.json(), {"id": 1, "name": "test", "address":"test", "manager":True, 'image': None, 'position': None, 'status': None, 'department': None})


    def test_delete_employee_detail_and_exist(self):
        self.client.login(username=self.username, password=self.password)
        employee_create = self.client.post("/employee", data={"name": "test", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_create.status_code, 201)
        employee_detail_delete = self.client.delete("/employee/1")
        self.assertEqual(employee_detail_delete.status_code, 204)
        employee_detail = self.client.get("/employee/1")
        self.assertEqual(employee_detail.status_code, 404)


    def test_delete_employee_detail_and_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        employee_create = self.client.post("/employee", data={"name": "test", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_create.status_code, 201)
        employee_detail_delete = self.client.delete("/employee/2")
        self.assertEqual(employee_detail_delete.status_code, 404)
        employee_detail = self.client.get("/employee/1")
        self.assertEqual(employee_detail.status_code, 200)
        self.assertEqual(employee_detail.json(), {"id": 1, "name": "test", "address":"test", "manager":True, 'image': None, 'position': None, 'status': None, 'department': None})


    def test_get_employee_detail_without_log_in(self):
        employee_detail = self.client.get("/employee/2")
        self.assertEqual(employee_detail.status_code, 302)
        employee_detail_put = self.client.put("/employee/2", data={"name": "test2", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_detail_put.status_code, 302)
        employee_detail_delete = self.client.delete("/employee/2")
        self.assertEqual(employee_detail_delete.status_code, 302)

    
    def test_get_employee_detail_post(self):
        self.client.login(username=self.username, password=self.password)
        employee_create = self.client.post("/employee", data={"name": "test", "address":"test", "manager":True}, content_type="application/json")
        self.assertEqual(employee_create.status_code, 201)
        employee_detail = self.client.post("/employee/1")
        self.assertEqual(employee_detail.status_code, 405)

    
    #Position detail
    def test_get_position_detail_with_logged_and_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        position_detail = self.client.get('/position/2')
        self.assertEqual(position_detail.status_code, 404)
        position_detail_put = self.client.put("/position/1", data={"position_name": "Python developer", "salary":50000})
        self.assertEqual(position_detail_put.status_code, 404)
        position_detail_delete = self.client.delete("/position/1", data={"position_name": "Python developer", "salary":50000})
        self.assertEqual(position_detail_delete.status_code, 404)

    def test_get_position_detail_with_logged_and_exist(self):
        self.client.login(username=self.username, password=self.password)
        position_create = self.client.post("/position", data={"position_name": "Python developer", "salary":50000}, content_type="application/json")
        self.assertEqual(position_create.status_code, 201)
        position_detail = self.client.get('/position/1')
        self.assertEqual(position_detail.status_code, 200)
        self.assertEqual(position_detail.json(), {"id": 1, "position_name": "Python developer", "salary":50000})

    def test_put_position_detail_with_logged_in_and_success(self):
        self.client.login(username=self.username, password=self.password)
        position_create = self.client.post("/position", data={"position_name": "Python developer", "salary":50000}, content_type="application/json")
        self.assertEqual(position_create.status_code, 201)
        position_detail_put = self.client.put("/position/1", data={"position_name": "Python developer", "salary":45000}, content_type="application/json")
        self.assertEqual(position_detail_put.status_code, 201)
        position_detail = self.client.get("/position/1")
        self.assertEqual(position_detail.status_code, 200)
        self.assertEqual(position_detail.json(), {"id": 1, "position_name": "Python developer", "salary":45000})
        
    def test_put_position_detail_with_logged_in_and_not_success(self):
        self.client.login(username=self.username, password=self.password)
        position_create = self.client.post("/position", data={"position_name": "Python developer", "salary":50000}, content_type="application/json")
        self.assertEqual(position_create.status_code, 201)
        position_detail_put = self.client.put("/position/1", data={}, content_type="application/json")
        self.assertEqual(position_detail_put.status_code, 400)
        position_detail = self.client.get("/position/1")
        self.assertEqual(position_detail.status_code, 200)
        self.assertEqual(position_detail.json(), {"id": 1, "position_name": "Python developer", "salary":50000})

    def test_put_position_detail_but_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        position_create = self.client.post("/position", data={"position_name": "Python developer", "salary":50000}, content_type="application/json")
        self.assertEqual(position_create.status_code, 201)
        position_detail_put = self.client.put("/position/2", data={"position_name": "Python developer", "salary":45000}, content_type="application/json")
        self.assertEqual(position_detail_put.status_code, 404)
        position_detail = self.client.get("/position/1")
        self.assertEqual(position_detail.status_code, 200)
        self.assertEqual(position_detail.json(), {"id": 1, "position_name": "Python developer", "salary":50000})


    def test_delete_position_detail_and_exist(self):
        self.client.login(username=self.username, password=self.password)
        position_create = self.client.post("/position", data={"position_name": "Python developer", "salary":50000}, content_type="application/json")
        self.assertEqual(position_create.status_code, 201)
        position_detail_delete = self.client.delete("/position/1")
        self.assertEqual(position_detail_delete.status_code, 204)
        position_detail = self.client.get("/position/1")
        self.assertEqual(position_detail.status_code, 404)


    def test_delete_position_detail_and_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        position_create = self.client.post("/position", data={"position_name": "Python developer", "salary":50000}, content_type="application/json")
        self.assertEqual(position_create.status_code, 201)
        position_detail_delete = self.client.delete("/position/2")
        self.assertEqual(position_detail_delete.status_code, 404)
        position_detail = self.client.get("/position/1")
        self.assertEqual(position_detail.status_code, 200)
        self.assertEqual(position_detail.json(), {"id": 1, "position_name": "Python developer", "salary":50000})


    def test_get_position_detail_without_log_in(self):
        position_detail = self.client.get("/position/2")
        self.assertEqual(position_detail.status_code, 302)
        position_detail_put = self.client.put("/position/2", data={"position_name": "Python developer", "salary":50000}, content_type="application/json")
        self.assertEqual(position_detail_put.status_code, 302)
        position_detail_delete = self.client.delete("/position/2")
        self.assertEqual(position_detail_delete.status_code, 302)

    
    def test_get_position_detail_post(self):
        self.client.login(username=self.username, password=self.password)
        position_create = self.client.post("/position", data={"position_name": "Python developer", "salary":50000}, content_type="application/json")
        self.assertEqual(position_create.status_code, 201)
        position_detail = self.client.post("/position/1")
        self.assertEqual(position_detail.status_code, 405)


    #Department detail
    def test_get_department_detail_with_logged_and_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        department_detail = self.client.get('/department/2')
        self.assertEqual(department_detail.status_code, 404)
        department_detail_put = self.client.put("/department/1", data={"department_name": "IT"})
        self.assertEqual(department_detail_put.status_code, 404)
        department_detail_delete = self.client.delete("/department/1")
        self.assertEqual(department_detail_delete.status_code, 404)

    def test_get_department_detail_with_logged_and_exist(self):
        self.client.login(username=self.username, password=self.password)
        department_create = self.client.post("/department", data={"department_name": "IT"}, content_type="application/json")
        self.assertEqual(department_create.status_code, 201)
        department_detail = self.client.get('/department/1')
        self.assertEqual(department_detail.status_code, 200)
        self.assertEqual(department_detail.json(), {"id": 1, "department_name": "IT", 'manager': None})

    def test_put_department_detail_with_logged_in_and_success(self):
        self.client.login(username=self.username, password=self.password)
        department_create = self.client.post("/department", data={"department_name": "IT"}, content_type="application/json")
        self.assertEqual(department_create.status_code, 201)
        department_detail_put = self.client.put("/department/1", data={"department_name": "Odoo"}, content_type="application/json")
        self.assertEqual(department_detail_put.status_code, 201)
        department_detail = self.client.get('/department/1')
        self.assertEqual(department_detail.status_code, 200)
        self.assertEqual(department_detail.json(), {"id": 1, "department_name": "Odoo", 'manager': None})
        
    def test_put_department_detail_with_logged_in_and_not_success(self):
        self.client.login(username=self.username, password=self.password)
        department_create = self.client.post("/department", data={"department_name": "IT"}, content_type="application/json")
        self.assertEqual(department_create.status_code, 201)
        department_detail_put = self.client.put("/department/1", data={}, content_type="application/json")
        self.assertEqual(department_detail_put.status_code, 400)
        department_detail = self.client.get('/department/1')
        self.assertEqual(department_detail.status_code, 200)
        self.assertEqual(department_detail.json(), {"id": 1, "department_name": "IT", 'manager': None})

    def test_put_department_detail_but_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        department_create = self.client.post("/department", data={"department_name": "IT"}, content_type="application/json")
        self.assertEqual(department_create.status_code, 201)
        department_detail_put = self.client.put("/department/2", data={"department_name": "Odoo"}, content_type="application/json")
        self.assertEqual(department_detail_put.status_code, 404)
        department_detail = self.client.get('/department/1')
        self.assertEqual(department_detail.status_code, 200)
        self.assertEqual(department_detail.json(), {"id": 1, "department_name": "IT", 'manager': None})


    def test_delete_department_detail_and_exist(self):
        self.client.login(username=self.username, password=self.password)
        department_create = self.client.post("/department", data={"department_name": "IT"}, content_type="application/json")
        self.assertEqual(department_create.status_code, 201)
        department_detail_delete = self.client.delete("/department/1")
        self.assertEqual(department_detail_delete.status_code, 204)
        department_detail = self.client.get("/department/1")
        self.assertEqual(department_detail.status_code, 404)


    def test_delete_department_detail_and_not_exist(self):
        self.client.login(username=self.username, password=self.password)
        department_create = self.client.post("/department", data={"department_name": "IT"}, content_type="application/json")
        self.assertEqual(department_create.status_code, 201)
        department_detail_delete = self.client.delete("/department/2")
        self.assertEqual(department_detail_delete.status_code, 404)
        department_detail = self.client.get('/department/1')
        self.assertEqual(department_detail.status_code, 200)
        self.assertEqual(department_detail.json(), {"id": 1, "department_name": "IT", 'manager': None})


    def test_get_department_detail_without_log_in(self):
        department_detail = self.client.get("/department/2")
        self.assertEqual(department_detail.status_code, 302)
        department_detail_put = self.client.put("/department/2", data={"department_name": "IT"}, content_type="application/json")
        self.assertEqual(department_detail_put.status_code, 302)
        department_detail_delete = self.client.delete("/department/2")
        self.assertEqual(department_detail_delete.status_code, 302)

    
    def test_get_department_detail_post(self):
        self.client.login(username=self.username, password=self.password)
        department_create = self.client.post("/department", data={"department_name": "IT"}, content_type="application/json")
        self.assertEqual(department_create.status_code, 201)
        department_detail = self.client.post("/department/1")
        self.assertEqual(department_detail.status_code, 405)