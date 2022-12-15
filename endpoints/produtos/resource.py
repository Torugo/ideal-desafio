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
        if id:
            prod = Produto.query.filter_by(id=id).first()
            if prod:
                return marshal(prod, produto_fields)
            else:
                abort(404)

    @marshal_with(produto_fields)
    def post(self):
        args = produto_post_parser.parse_args()
        args["ativo"] = True
        prod = Produto(**args)

        db.session.add(prod)
        db.session.commit()

        return prod
