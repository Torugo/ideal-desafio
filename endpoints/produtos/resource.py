from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import request

from .model import Produto
from app import db

produto_fields = {
    "id": fields.Integer,
    "nome": fields.String,
    "ativo": fields.Boolean,
    "data_criacao": fields.String,
}

produto_list_fields = {
    'count': fields.Integer,
    'produtos': fields.List(fields.Nested(produto_fields)),
}


produto_post_parser = reqparse.RequestParser()
produto_post_parser.add_argument(
    "nome",
    type=str,
    required=True,
    location=["json"],
    help="O parâmetro nome é obrigatório",
)


class ProdutosResource(Resource):
    def get(self, id=None):
        """
        Retorna um dado produto quando fornecido seu produto_id 
        ---
        tags:
          - Produtos
        parameters:
          - in: path
            name: id
            required: false
            description: O id do produto, tente 1
            type: string
          - in: query
            name: offset
            type: integer
            description: The number of items to skip before starting to collect the result set.
          - in: query
            name: limit
            type: integer
            description: The numbers of items to return.
        responses:
          200:
            description: Informação do Produto
            schema:
              id: Produto
              properties:
                id:
                  type: string
                  default: 1
                nome:
                  type: string
                  default: TRXF11
                ativo:
                    type: Bool
                    default: True
                data_criacao:
                    type: Date
                    default: 16/12/2022 12:56
          404:
            description: "Produto não encontrado"  
        """
        if id:
            prod = Produto.query.filter_by(id=id).first()
            if prod:
                return marshal(prod, produto_fields)
            else:
                abort(404, message="Produto não encontrado")
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            prod = Produto.query.filter_by(**args).order_by(Produto.id)
            if limit:
                prod = prod.limit(limit)

            if offset:
                prod = prod.offset(offset)

            prod = prod.all()

            return marshal({
                'count': len(prod),
                'produtos': [marshal(p, produto_fields) for p in prod]
            }, produto_list_fields)


    @marshal_with(produto_fields)
    def post(self):
        """
        Cadastra um novo produto
        ---
        tags:
          - Produtos
        parameters:
          - in: body
            name: body
            schema:
              id: produto_insert
              properties:
                nome: 
                  type: string
                  default: TRXF11
        responses:
          200:
            description: Informação do produto
            schema:
              id: produto
              properties:
                nome:
                  type: string
                  default: TRXF11
        """
        args = produto_post_parser.parse_args()
        args["ativo"] = True

        nome = args['nome']
        prod = Produto.query.filter_by(nome=nome).first()
        if prod:
            abort(400, message= "Nome do produto já cadastrado")

        prod = Produto(**args)

        db.session.add(prod)
        db.session.commit()

        return prod
