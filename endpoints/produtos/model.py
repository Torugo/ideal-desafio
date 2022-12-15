from datetime import datetime

from app import db


class Produto(db.Model):
    _tablename_ = "tbl_produtos"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(), nullable=False, unique=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, nullable=False)

    def _init_(self, id, ativo):
        self.id = id
        self.ativo = ativo

    def _repr_(self):
        return f"id {self.id} nome {self.nome}"
