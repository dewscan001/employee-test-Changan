FROM python:3.14.0
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic
RUN python manage.py test
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000