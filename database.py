from sqlalchemy.orm import declarative_base,create_session
from sqlalchemy import create_engine


Base=declarative_base()
session=create_session()

engine=create_engine("postgresql://postgres:ramiz@localhost/delivery_heros",echo=True)

