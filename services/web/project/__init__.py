from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
import re
MM = Marshmallow()


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "atendimentos"

    id = db.Column(db.Integer, primary_key=True)

    # CPF 11 dígitos
    cpf = db.Column(db.String(11), nullable=False)

    private = db.Column(db.Boolean(), nullable=False)
    incompleto = db.Column(db.Boolean(), nullable=False)

    dta_u_compra = db.Column(db.DateTime())
    tkt_medio = db.Column(db.Float())
    tkt_u_compra = db.Column(db.Float())

    # CNPJ 14 dígitos
    loja_frequente = db.Column(db.String(14))
    loja_u_compra = db.Column(db.String(14))

    def __init__(self, cpf, private, incompleto, dta_u_compra, tkt_medio, tkt_u_compra, loja_frequente, loja_u_compra):
        self.cpf = cpf
        self.private = private
        self.incompleto = incompleto
        self.dta_u_compra = dta_u_compra
        self.tkt_medio = tkt_medio
        self.tkt_u_compra = tkt_u_compra
        self.loja_frequente = loja_frequente
        self.loja_u_compra = loja_u_compra

class cpf(fields.Field):
    def _deserialize(self, value, *args, **kwargs):
        computed_cpf = ''.join(filter(str.isdigit, value))
        return computed_cpf if len(computed_cpf) == 11 else ""

    def _serialize(self, value, *args, **kwargs):
        return value

class cnpj(fields.Field):
    def _deserialize(self, value, *args, **kwargs):
        computed_cpf = ''.join(filter(str.isdigit, value))
        return computed_cpf if len(computed_cpf) == 14 else ""

    def _serialize(self, value, *args, **kwargs):
        return value

class AtendimentoSchema(MM.Schema):
    id = fields.Int(dump_only=True)
    cpf = cpf(required=True)
    private = fields.Boolean()
    incompleto = fields.Boolean()
    dta_u_compra = fields.Date()
    tkt_medio = fields.Float()
    tkt_u_compra = fields.Float()
    loja_frequente = cnpj()
    loja_u_compra = cnpj()

    # def compute_cpf(self, obj):
    #     return obj.cpf
    #     print("oi")
    #     computed_cpf = ''.join(filter(str.isdigit, obj.cpf))
    #     return computed_cpf if len(computed_cpf) == 11 else ""

    # def compute_cnpj(self, obj):
    #     computed_cnpj = ''.join(filter(str.isdigit, obj.loja_frequente))
    #     return computed_cnpj if len(computed_cnpj) == 14 else ""

@app.route("/")
def hello_world():
    return jsonify(hello="world")