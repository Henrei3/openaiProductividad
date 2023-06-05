from backend.Model.DB.base import Base, engine

from flask import Flask
from flask_cors import CORS
from backend.Controller.QualityAssurance import QualityAssurance

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(engine)


@app.route('/records')
def get_recordings():
    print(" ")


@app.route('/records', methods=['POST'])
def add_recording():
    print("")


@app.route("/QA", methods=["POST"])
def execute_qa():
    QualityAssurance.execute()


@app.route("/QA")
def get_all():
    print("Not Yet Implemented")
