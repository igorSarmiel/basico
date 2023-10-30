from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from . import db
from random import randint

class Usuarios(db.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=False, nullable=False)
    email= Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    tokem = Column(String, default=str(randint(1000,9999)) )

    def __repr__(self) -> str:
        return self.nome

    

class Tema(db.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String)



class Materia(db.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String)


class Questao(db.Model):
    id = Column(Integer, primary_key=True)
    ano = Column(Integer)
    enunciado = Column(Text)
    