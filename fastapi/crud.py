from fastapi import FastAPI
from sqlalchemy import create_engine ,Column,Integer,CHAR
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base



app = FastAPI()


engine  = create_engine(url)
session=sessionmaker(bind=engine)
Base=declarative_base()
Base.metada
class employee(Base):
    __tablename__= "employee"
    name = Column()
