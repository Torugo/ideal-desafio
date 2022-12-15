from app import db

class Produto(db.Model):
    _tablename_ = 'tbl_produtos'

    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nome = db.Column(db.String(), nullable=False)
    ativo = db.Column(db.Bool, nullable=False)

    def __init__(self, id, nome, ativo):
        self.id = id
        self.nome = nome
        self.ativo = ativo

    def _repr_(self):
        return f"id {self.id} nome {self.nome}"