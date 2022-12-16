from datetime import datetime

from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import request
from sqlalchemy.exc import ProgrammingError

from .model import Cliente
from app import db

user_fields = {
    "id": fields.Integer,
    "nome": fields.String,
    "cpf": fields.String,
    "dtNascimento": fields.String,
    "ativo": fields.Boolean,
    "data_criacao": fields.String,
}

user_list_fields = {
    'count': fields.Integer,
    'users': fields.List(fields.Nested(user_fields)),
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
        """
        Retorna um dado cliente quando fornecido seu cliente_id, caso contrario retorna todos clientes
        ---
        tags:
          - Clientes
        parameters:
          - in: path
            name: id
            required: false
            description: O id do cliente, tente 1
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
            description: Informação do Cliente
            schema:
              id: cliente
              properties:
                id:
                  type: string
                  default: 1
                nome:
                  type: string
                  default: Stevie Harris
                cpf:
                    type: int
                    default: 11111111111
                dtNascimento:
                    type: Date
                    default: 10/10/10
                ativo:
                    type: Bool
                    default: True
                data_criacao:
                    type: Date
                    default: 16/12/2022 15:15
          404:
            description: "Cliente não encontrado"
        """
        try:
            if id:
                user = Cliente.query.filter_by(id=id).first()
                if user:
                    return marshal(user, user_fields)
                else:
                    abort(404, message="Cliente não encontrado")
            else:
                args = request.args.to_dict()
                limit = args.get('limit', 0)
                offset = args.get('offset', 0)

                args.pop('limit', None)
                args.pop('offset', None)

                user = Cliente.query.filter_by(**args).order_by(Cliente.id)
                if limit:
                    user = user.limit(limit)

                if offset:
                    user = user.offset(offset)

                user = user.all()

                return marshal({
                    'count': len(user),
                    'users': [marshal(u, user_fields) for u in user]
                }, user_list_fields)

        except ProgrammingError:
            abort(500, message="Erro interno")

    @marshal_with(user_fields)
    def post(self):
        """
        Cadastra um novo cliente
        ---
        tags:
          - Clientes
        parameters:
          - in: body
            name: body
            schema:
              id: cliente_insert
              properties:
                nome: 
                  type: string
                  default: Stevie Harris
                cpf:
                    type: int
                    default: 11111111111
                dtNascimento:
                    type: Date
                    default: 10/10/10
        responses:
          200:
            description: Informação do Cliente
            schema:
              id: cliente
          400:
            description: "CPF já cadastrado"
        """
        args = user_post_parser.parse_args()
        cpf = int(args['cpf'])

        user = Cliente.query.filter_by(cpf=cpf).first()
        if user:
            abort(400, message= "CPF já cadastrado")
        args["ativo"] = True
        args["dtNascimento"] = datetime.strptime(args["dtNascimento"], "%d/%m/%y")
        
        user = Cliente(**args)

        db.session.add(user)
        db.session.commit()

        return user
