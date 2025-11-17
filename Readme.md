# Login admin page 
### - User role for development env.
username: `user` <br>
password: `X9HV8n9YP_CH_U4`

### - Admin user for both environment
username: `admin` <br>
password: `admin`

You can use admin role for create new another user from Admin page (`/admin`) > Users

<br>

# How to run
- `git clone https://github.com/dewscan001/employee-test-Changan.git`
- `docker-compose -f docker-compose-prod.yml up --build` << for product environment (use database: `db.sqlite3_prod`) <br>

- `docker-compose -f docker-compose-test.yml up --build` << for development environment (use database: `db.sqlite3_test`) <br>

And then you can access to website by `localhost:8000`

<br>

# API endpoint (login before get it)
- `/employee` (GET/POST) get list of employee
- `/position` (GET/POST) get list of position
- `/department` (GET/POST) get list of department
- `/employee/<int:id>` (GET/PUT/DELETE) get employee detail by id
- `/position/<int:id>` (GET/PUT/DELETE) get position detail by id
- `/department/<int:id>` (GET/PUT/DELETE) get department detail by id

<br>

# Ref. Document
- Django (https://www.djangoproject.com/start/overview/)
- Django Rest Framework (https://www.django-rest-framework.org/) 
- Docker (https://docs.docker.com/manuals/)