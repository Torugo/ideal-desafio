from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Resource

from .model import Ordem
from app import db

ordem_fields = {
    "id": fields.Integer,
    "idCliente": fields.Integer,
    "idProduto": fields.Integer,
    "valorCompra": fields.Float,
    "qtdCompra": fields.Integer,
    "totalCompra": fields.Float,
}

order_post_parser = reqparse.RequestParser()
order_post_parser.add_argument(
    "idCliente",
    type=str,
    required=True,
    location=["json"],
    help="O parâmetro idCliente é obrigatório",
)


order_post_parser.add_argument(
    "idProduto",
    type=str,
    required=True,
    location=["json"],
    help="O parâmetro idProduto é obrigatório",
)

order_post_parser.add_argument(
    "valorCompra",
    type=float,
    required=True,
    location=["json"],
    help="O parâmetro valorCompra é obrigatório",
)

order_post_parser.add_argument(
    "qtdCompra",
    type=int,
    required=True,
    location=["json"],
    help="O parâmetro qtdCompra é obrigatório",
)


class OrdemResource(Resource):
    def get(self, id=None):
        if id:
            order = Ordem.query.filter_by(id=id).first()
            if order:
                order.valorCompra = order.valorCompra / 100  # avoiding mantissa errors
                order.totalCompra = order.totalCompra / 100
                return marshal(order, ordem_fields)
            else:
                abort(404)

    @marshal_with(ordem_fields)
    def post(self):
        args = order_post_parser.parse_args()
        args["valorCompra"] = args["valorCompra"] * 100  # avoiding mantissa errors
        args["totalCompra"] = args["valorCompra"] * args["qtdCompra"]
        order = Ordem(**args)

        db.session.add(order)
        db.session.commit()

        order.valorCompra = order.valorCompra / 100  # avoiding mantissa errors
        order.totalCompra = order.totalCompra / 100

        return order
