FROM mcr.microsoft.com/windows:ltsc2019 as windows
COPY . .

FROM python:3.9
COPY --from=windows . .

WORKDIR /python_app
EXPOSE 5000

RUN pip install sqlalchemy psycopg2-binary flask marshmallow flask-cors openai pyodbc tiktoken makeobj pydub decouple
ENV FLASK_RUN_HOST=0.0.0.0
RUN flask --app ./View/flaskView.py run

