FROM python:3.9

WORKDIR /python_app
COPY . .
RUN pip install pipenv
RUN pipenv install sqlalchemy psycopg2-binary flask marshmallow flask-cors openai pyodbc

