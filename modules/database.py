from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    transcript = Column(String)
    analysis = Column(JSON)

def get_db():
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///empathy_analyzer.db')
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def save_result(db, filename, transcript, analysis):
    result = Result(filename=filename, transcript=transcript, analysis=analysis)
    db.add(result)
    db.commit()
    return result.id

def get_result(db, result_id):
    return db.query(Result).filter(Result.id == result_id).first()