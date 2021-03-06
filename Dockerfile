 FROM python:3.6
 ENV PYTHONUNBUFFERED 1
 COPY . .
 RUN pip install -r requirements.txt
 EXPOSE 8000
 RUN python manage.py test
 CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]