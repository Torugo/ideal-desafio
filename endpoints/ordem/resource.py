from datetime import datetime

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

produto_post_parser = reqparse.RequestParser()
produto_post_parser.add_argument(
    "idCliente",
    type=str,
    required=True,
    location=["json"],
    help="O parâmetro idCliente é obrigatório",
)


produto_post_parser.add_argument(
    "idProduto",
    type=str,
    required=True,
    location=["json"],
    help="O parâmetro idProduto é obrigatório",
)

produto_post_parser.add_argument(
    "valorCompra",
    type=float,
    required=True,
    location=["json"],
    help="O parâmetro valorCompra é obrigatório",
)

produto_post_parser.add_argument(
    "qtdCompra",
    type=int,
    required=True,
    location=["json"],
    help="O parâmetro qtdCompra é obrigatório",
)

# produto_post_parser.add_argument(
#     "totalCompra",
#     type=float,
#     required=True,
#     location=["json"],
#     help="O parâmetro totalCompra é obrigatório",
# )


class OrdemResource(Resource):
    def get(self, id=None):
        if id:
            prod = Ordem.query.filter_by(id=id).first()
            return marshal(prod, ordem_fields)

    @marshal_with(ordem_fields)
    def post(self):
        args = produto_post_parser.parse_args()
        args['valorCompra'] = args['valorCompra'] * 100 #avoiding mantissa errors
        args['totalCompra'] = args['valorCompra'] * args['qtdCompra'] #avoiding mantissa errors
        
        
        prod = Ordem(**args)

        db.session.add(prod)
        db.session.commit()

        return prod


        