FROM python:3.6

RUN mkdir /django
WORKDIR /django

COPY requirements.txt ./
RUN apt-get update && apt-get install -y graphviz-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY django .

CMD ["python", "django/manage.py", "runserver", "0.0.0.0:8000"]
