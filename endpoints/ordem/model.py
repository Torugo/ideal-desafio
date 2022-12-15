from datetime import datetime

from app import db


class Ordem(db.Model):
    _tablename_ = "tbl_ordens"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idCliente = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    idProduto = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    valorCompra = db.Column(db.Integer, nullable=False)
    qtdCompra = db.Column(db.Integer, nullable=False)
    totalCompra = db.Column(db.Integer, nullable=False)
    dataOrdem = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def _init_(self, id, idCliente, idProduto, valorCompra, qtdCompra, totalCompra):
        self.id = id
        self.idCliente = idCliente
        self.idProduto = idProduto
        self.valorCompra = valorCompra
        self.qtdCompra = qtdCompra
        self.totalCompra = totalCompra
