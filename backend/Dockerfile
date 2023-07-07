FROM python:3.9

WORKDIR /python_app

ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
COPY . .
RUN pip install sqlalchemy psycopg2-binary flask marshmallow flask-cors openai pyodbc tiktoken makeobj pydub decouple
RUN flask --app .\View\flaskView.py run 

