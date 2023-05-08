from Model.base import Base, engine, Session
from Model.recordingsDB import Recordings, RecordingSchemaGet, \
    RecordingSchemaPost, Simple, SimpleSchemaPost, SimpleSchemaGet
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

Base.metadata.create_all(engine)


@app.route('/records')
def get_recordings():
    session = Session()

    recording_objects = session.query(Recordings).all()

    schema = RecordingSchemaGet(many=True)

    records = schema.dump(recording_objects)

    session.close()
    print(records)
    return records


@app.route('/records', methods=['POST'])
def add_recording():
    print(request.get_json())
    posted_record = RecordingSchemaPost().load(request.get_json())

    print(posted_record)

    record = Recordings(**posted_record.data)

    session = Session()
    session.add(record)
    session.commit()

    to_json_record = RecordingSchemaPost().dump(record).data
    session.close()
    return jsonify(to_json_record), 201


@app.route('/config_simple')
def config():
    session = Session()
    samples = session.query(Simple).all()
    if len(samples) == 0:
        sample = Simple(5)
        session.add(sample)
        session.commit()
        session.close()

        samples = session.query(Simple).all()
    print(list(samples))

    schema = SimpleSchemaPost(many=True)

    to_json = schema.dump(samples)

    print(to_json)

    return jsonify(to_json)


@app.route('/simple')
def get_simple():
    sess = Session()

    simple_objects = sess.query(Simple).all()

    schema = SimpleSchemaGet(many=True)

    samples = schema.dump(simple_objects)

    print(type(samples))

    return samples


@app.route('/simple', methods=['POST'])
def add_simple():
    print("test")
    posted_simple = SimpleSchemaPost().load(request.get_json())

    print(posted_simple)

    simple = Simple(**posted_simple)

    session = Session()
    session.add(simple)
    session.commit()

    to_json_simple = SimpleSchemaPost().dump(simple)

    print(to_json_simple)
    session.close()

    return jsonify(to_json_simple), 201



