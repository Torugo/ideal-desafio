from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Resource

from .model import Produto
from app import db

produto_fields = {
    "id": fields.Integer,
    "nome": fields.String,
    "ativo": fields.Boolean,
    "data_criacao": fields.DateTime,
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
            required: true
            description: O id do produto, tente 1
            type: string
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
        prod = Produto(**args)

        db.session.add(prod)
        db.session.commit()

        return prod
