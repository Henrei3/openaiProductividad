import json
from backend.Model.DB.base import Base, engine
from flask import Flask, request
from flask_cors import CORS
from backend.Controller.ApplicationProcess import QualityAssurance, GestionesDePago
from backend.Controller.PostGreSQLController import PostgreController
from backend.Model.DB.recordingsDB import Embedding
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
def calculate_pattern_price():
    date = dict()
    for date_string in request.form:
        date = json.loads(date_string)
        print(date)

    year = date['year']
    month = date['month']
    day = date['day']
    embeddings_given_date = PostgreController.get_embeddings_given_date(year, month, day)
    if embeddings_given_date:
        row_count = 0
        for embeddings_row in embeddings_given_date:
            embedding: Embedding = embeddings_row[0]
            print("Id : ", embedding.e_id, "Embedding",  embedding.embedding)
            row_count += 1
        if row_count >= 1:
            return 'El calculo de los patrones para esta fecha ya ha sido efectuado'

    result = str(GestionesDePago.audio_price_evaluation(date['year'], date['month'], date['day']))
    print(result)
    return 'El precio de la transformacion a texto de estos audios costara ' + result + ' USD.'


@app.route('/audioTranformationEmbeddingsCalculation', methods=['GET'])
def audio_transformation_embeddings_calculation():
    embedding_price = str(GestionesDePago.audio_transformation_embeddings_evaluation())
    return 'El precio de calculo de embeddings sera de ' + embedding_price + '  USD.'


@app.route('/embeddingsGeneration', methods=['GET'])
def embeddings_calculation():
    embedding_status = GestionesDePago.embeddings_calculation()
    if embedding_status:
        return 'El calculo de Embedings ha sido exitoso ahora puede evaluar ' \
               'la cercania que sus llamadas tienen con las de la base de Datos ahora aumentada'

    return "El calculo de embeddings no se ha podido realizar :'( "
