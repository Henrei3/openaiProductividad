import json
from backend.Model.DB.base import Base, engine
from flask import Flask, request
from flask_cors import CORS
from backend.Controller.ApplicationProcess import QualityAssurance, GestionesDePago
from backend.Controller.PostGreSQLController import PostgreController

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(engine)


@app.route('/records', methods=["GET"])
def get_recordings():
    print(" Get Signal received ")
    return "Signal Received"


@app.route('/records', methods=['POST'])
def add_recording():
    return QualityAssurance.await_test(request)


@app.route('/patternPrice', methods=['POST'])
def calculatePatternPrice():
    date = dict()
    for date_string in request.form:
        date = json.loads(date_string)
    year = date['year']
    month = date['month']
    day = date['day']
    embeddings_given_date = PostgreController.get_embeddings_given_date(year, month, day)
    if embeddings_given_date and len(embeddings_given_date) > 100:
        return 'El calculo de los patrones para esta fecha ya ha sido efectuado'
    result = str(GestionesDePago.audio_price_evaluation(date['year'], date['month'], date['day']))
    print(result)
    return 'El precio de la transformacion a texto de estos audios costara ' + result + 'USD.'
