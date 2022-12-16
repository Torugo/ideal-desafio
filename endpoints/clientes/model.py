from datetime import datetime

from app import db


class Cliente(db.Model):
    _tablename_ = "tbl_clientes"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(), nullable=False)
    cpf = db.Column(db.String, nullable=False, unique=True)
    dtNascimento = db.Column(db.DateTime, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, nullable=False)

    def _init_(self, id, nome, cpf, dtNascimento, ativo):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.dtNascimento = dtNascimento
        self.ativo = ativo

    def _repr_(self):
        return f"id {self.id} nome {self.nome} cpf {self.cpf}"
