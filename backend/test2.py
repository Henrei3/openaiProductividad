import requests
from Model.base import engine, Session
from Model.recordingsDB import Base, Gestion, PatronesExito, Audios
from sqlalchemy import text


def make_post_simple():
    url = "http://127.0.0.1:5000/records"

    audio_text = {"content": "Alo ?"}
    score = {"QA": "Dos tablas "}

    simple_post_object = Gestion(10, 10, 10, 10)


session = Session()

Base.metadata.create_all(engine)
gestion = session.query(Gestion).all()
patrones_exito = session.query(PatronesExito).all()
audios = session.query(Audios).all()

if len(gestion) == 0:
    score = '{"test" = "expected ?"}'
    gestion_obj = Gestion(score)

    session.add(gestion_obj)
    session.commit()

    gestion = session.query(Gestion).all()

if len(patrones_exito) == 0:
    patterns = '{"test": "Very well though Pattern"}'

    gestion_p = PatronesExito(patterns)

    session.add(gestion_p)
    session.commit()

    patrones_exito = session.query(PatronesExito).all()

if len(audios) == 0:
    gpt_answer = '{"content": "My name is Elon Musk"}'
    audio_text = ' {"content": "Buenas Tardes le saludamos del banco del pacifico"} '
    gestion_a = session.query(Gestion).one()
    audi = Audios(audio_text, gpt_answer, gestion_a.g_id)

    session.add(audi)
    session.commit()

session.close()

print("## PatronesExito")
for patrones in patrones_exito:
    print(f"{patrones.pe_id}: {patrones.patterns}")

print("## Gestion")
for calidad in gestion:
    print(f"{calidad.g_id}:  {calidad.score}")

audios = session.query(Audios).all()
print("## Audios")
for audio in audios:
    print(f"{audio.audio_id} : {audio.audio_text} - {audio.gpt_answer} - {audio.gestion_id}")
