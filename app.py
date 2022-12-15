from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import settings
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS

db = SQLAlchemy(app)
api = Api(app)
api.prefix = '/v1'

from flask_migrate import Migrate
migrate = Migrate()
migrate.init_app(app, db)


from endpoints.clientes.resource import ClientsResource
from endpoints.produtos.resource import ProdutosResource

api.add_resource(ClientsResource, '/clientes', '/clientes/<int:id>')
api.add_resource(ProdutosResource, '/produtos', '/produtos/<int:id>')


if __name__ == '__main__':
    app.run()
