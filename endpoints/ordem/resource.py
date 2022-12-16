from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import request


from .model import Ordem
from app import db

ordem_fields = {
    "id": fields.Integer,
    "idCliente": fields.Integer,
    "idProduto": fields.Integer,
    "valorCompra": fields.Float,
    "qtdCompra": fields.Integer,
}

ordem_list_fields = {
    'count': fields.Integer,
    'Ordems': fields.List(fields.Nested(ordem_fields)),
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
        """
        Retorna um dado produto quando fornecido seu produto_id 
        ---
        tags:
          - Ordems
        parameters:
          - in: path
            name: id
            required: true
            description: O id da ordem, tente 1
            type: string
        responses:
          200:
            description: Informação da Ordem
            schema:
              id: Ordem
              properties:
                id:
                  type: string
                  default: 1
                idCliente:
                  type: int
                  default: 1
                idProduto:
                    type: int
                    default: 1
                qtdCompra:
                    type: int
                    default: 10
                valorCompra:
                    type: float
                    default: 10.50

          404:
            description: "Ordem não encontrado"  
        """
        if id:
            order = Ordem.query.filter_by(id=id).first()
            if order:
                order.valorCompra = order.valorCompra / 100  # avoiding mantissa errors
                order.totalCompra = order.totalCompra / 100
                return marshal(order, ordem_fields)
            else:
                abort(404, message="Ordem não encontrada")
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            ordem = Ordem.query.filter_by(**args).order_by(Ordem.id)
            if limit:
                ordem = ordem.limit(limit)

            if offset:
                ordem = ordem.offset(offset)

            ordem = ordem.all()

            return marshal({
                'count': len(ordem),
                'ordens': [marshal(o, ordem_fields) for o in ordem]
            }, ordem_list_fields)

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
