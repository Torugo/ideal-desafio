from datetime import datetime

from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Resource

from .model import Cliente
from app import db

user_fields = {
    "id": fields.Integer,
    "nome": fields.String,
    "cpf": fields.String,
    "dtNascimento": fields.DateTime,
}


user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument(
    "nome",
    type=str,
    required=True,
    location=["json"],
    help="O parâmetro nome é obrigatório",
)
user_post_parser.add_argument(
    "cpf",
    type=int,
    required=True,
    location=["json"],
    help="O parâmetro CPF é obrigatório",
)
user_post_parser.add_argument(
    "dtNascimento",
    type=str,
    required=True,
    location=["json"],
    help="O parâmetro dtNascimento é obrigatório",
)


class ClientsResource(Resource):
    def get(self, id=None):
        if id:
            user = Cliente.query.filter_by(id=id).first()
            if user:
                return marshal(user, user_fields)
            else:
                abort(404)

    @marshal_with(user_fields)
    def post(self):
        args = user_post_parser.parse_args()
        args["ativo"] = True
        args["dtNascimento"] = datetime.strptime(args["dtNascimento"], "%d/%m/%y")
        user = Cliente(**args)

        db.session.add(user)
        db.session.commit()

        return user
