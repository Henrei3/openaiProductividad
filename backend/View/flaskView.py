import json
from backend.Model.DB.base import Base, engine
from flask import Flask, request
from flask_cors import CORS
from backend.Controller.ApplicationProcess import QualityAssurance, GestionesDePago
from backend.Controller.PostGreSQLController import PostgreController
from backend.Model.DB.recordingsDB import Embedding, Scores
from backend.Controller.pathFinder import JSONFinder
app = Flask(__name__)
CORS(app)

Base.metadata.create_all(engine)


@app.route('/records', methods=['POST'])
def add_recording():
    date = dict()
    for date_string in request.form:
        date = json.loads(date_string)
        print(date)
    year = date['year']
    month = date['month']
    day = date['day']

    scores_given_date = PostgreController.get_scores_given_date(year, month, day)
    if scores_given_date:
        row_count = 0
        for scores_row in scores_given_date:
            row_count += 1
            score: Scores = scores_row[0]
            print('FlaskView : addRecording -> Found score id: ', score.s_id, 'Score score: ', score.score)
        if row_count >= 10:
            return ['El calculo de calificacion para esta fecha ya ha sido efectuado', False]
        else:
            audio_calculation_price = QualityAssurance.audio_price_evaluation(year, month, day)
            print(audio_calculation_price)
            return ['La transformación de Audios a Texto costará : ' + str(audio_calculation_price) + ' USD. ', True]


@app.route('/scoresFetch', methods=['GET'])
def get_calculated_scores_set_date():
    json_finder = JSONFinder('../analysed_records/')
    date = json_finder.find('date.json')
    print(date['y'], date['m'], date['d'])
    chunked_iterator_results = PostgreController.get_scores_given_date(date['y'], date['m'], date['d'])

    scores = dict()
    print(chunked_iterator_results)
    for row_result in chunked_iterator_results:
        print("Test")
        score: Scores = row_result[0]
        name = row_result[1]
        audio_text = row_result[2]
        scores[name] = [score.score, audio_text]
        print("FlaskView -> Get Calculated Scores Set Date Score.id = ", score.s_id,
              " Score.score = ", score.score)
    print("Scores : ", scores)
    if len(scores) > 0:
        return [scores, True]
    return ['No Scores To See', False]


@app.route('/records', methods=["GET"])
def get_recordings():

    function_status = QualityAssurance.audio_transformation_score_calculation()
    if function_status:
        return 'El calculo de las grabaciones ha sido efectuado'
    return 'El calculo de las grabaciones no se ha podido efectuar'


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
            return ["El calculo de los patrones para esta fecha ya ha sido efectuado", True]

    result = str(GestionesDePago.audio_price_evaluation(date['year'], date['month'], date['day']))
    print(result)
    return ['El precio de la transformacion a texto de estos audios costara ' + result + ' USD.', False]


@app.route('/audioTranformationEmbeddingsCalculation', methods=['GET'])
def audio_transformation_embeddings_calculation():
    embedding_price = str(GestionesDePago.audio_transformation_embeddings_evaluation())
    return 'El precio de calculo de embeddings sera de ' + embedding_price + '  USD.'


@app.route('/embeddingsGeneration', methods=['GET'])
def embeddings_calculation():
    embedding_status = GestionesDePago.embeddings_calculation()
    if embedding_status:
        return 'El calculo de Embedings ha sido exitoso, ahora puede evaluar un audio'

    return "El calculo de embeddings no se ha podido realizar :'( "
