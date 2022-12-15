from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import Cliente
from datetime import datetime

from app import db

user_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'cpf': fields.String,
    'dtNascimento': fields.DateTime,
      
}

user_list_fields = {
    'count': fields.Integer,
    'users': fields.List(fields.Nested(user_fields)),
}

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('nome', type=str, required=True, location=['json'],
                              help='O parâmetro nome é obrigatório')
user_post_parser.add_argument('cpf', type=int, required=True, location=['json'],
                              help='O parâmetro CPF é obrigatório')
user_post_parser.add_argument('dtNascimento', type=str, required=True, location=['json'],
                              help='O parâmetro dtNascimento é obrigatório')                         

class ClientsResource(Resource):
    def get(self, id=None):
        if id:
            user = Cliente.query.filter_by(id=id).first()
            return marshal(user, user_fields)

    @marshal_with(user_fields)
    def post(self):
        args = user_post_parser.parse_args()
        args['ativo'] = True
        args['dtNascimento'] = datetime.strptime(args['dtNascimento'], '%d/%m/%y')
        user = Cliente(**args)
        # user.dtNascimento = user.
        db.session.add(user)
        db.session.commit()

        return user

    # @marshal_with(user_fields)
    # def put(self, user_id=None):
    #     user = User.query.get(user_id)

    #     if 'name' in request.json:
    #         user.name = request.json['name']

    #     db.session.commit()
    #     return user

    # @marshal_with(user_fields)
    # def delete(self, user_id=None):
    #     user = User.query.get(user_id)

    #     db.session.delete(user)
    #     db.session.commit()

    #     return user
