FROM python:3.14.0
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
ENV DEBUG=FALSE
RUN python manage.py makemigrations
RUN python manage.py migrate
ENV DEBUG=TRUE
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input
RUN python manage.py test
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000