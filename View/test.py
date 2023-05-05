from Model.base import Base, engine, Session
from Model.recordingsDB import Recordings


Base.metadata.create_all(engine)

session = Session()

records = session.query(Recordings).all()

if len(records) == 0:

    json0 = {"test": 0}
    json1 = {"test": 1}
    json2 = {"test": 2}
    json3 = {"test": 3}

    recording = Recordings(json0, json1, json2, json3)

    session.add(recording)
    session.commit()
    session.close()

    records = session.query().all()

print('### Recordings:')
for exam in records:
    print(f'({exam.id}) {exam.title} - {exam.description}')


