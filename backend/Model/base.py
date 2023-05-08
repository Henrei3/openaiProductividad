import sqlalchemy.orm
from sqlalchemy import create_engine
from decouple import config
from sqlalchemy.orm import sessionmaker


db_url = config('pg_url')

db_user = config('pg_user')

db_name = config('pg_name')

db_password = config('pg_psw')


engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = sqlalchemy.orm.declarative_base()
