from backend.Model.DB.base import Base, engine

from flask import Flask, request
from flask_cors import CORS
from backend.Controller.ApplicationProcess import QualityAssurance

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(engine)


@app.route('/records', methods=["GET"])
def get_recordings():
    print(" Get Signal received ")
    return "Signal Received"


@app.route('/records', methods=['POST'])
def add_recording():
    for val in request.values:
        print(val)

    return QualityAssurance.await_test()


@app.route("/QA", methods=["POST"])
def execute_qa():
    QualityAssurance.execute()


@app.route("/QA")
def get_all():
    print("Not Yet Implemented")
