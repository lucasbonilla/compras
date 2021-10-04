from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_cors import CORS
from os.path import isfile, join
from datetime import datetime
from pycpfcnpj import cpfcnpj
import os
import re
import threading
import time
MM = Marshmallow()

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "atendimentos"

    id = db.Column(db.Integer, primary_key=True)

    # CPF 11 dígitos
    cpf = db.Column(db.String(11), nullable=False)

    private = db.Column(db.Boolean(), nullable=False)
    incompleto = db.Column(db.Boolean(), nullable=False)

    dta_u_compra = db.Column(db.Date())
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
        return computed_cpf if cpfcnpj.validate(computed_cpf) and len(computed_cpf) == 11 else "00000000000"

    def _serialize(self, value, *args, **kwargs):
        return value

class cnpj(fields.Field):
    def _deserialize(self, value, *args, **kwargs):
        computed_cnpj = ''.join(filter(str.isdigit, value))
        return computed_cnpj if cpfcnpj.validate(computed_cnpj) and len(computed_cnpj) == 14 else None

    def _serialize(self, value, *args, **kwargs):
        return value

class my_date(fields.Field):
    def _deserialize(self, value, *args, **kwargs):
        return datetime.strptime(value, '%Y-%m-%d') if value not in['NULL', ''] else None

    def _serialize(self, value, *args, **kwargs):
        return value

class my_float(fields.Field):
    def _deserialize(self, value, *args, **kwargs):
        return float(value) if value not in['NULL', ''] else None

    def _serialize(self, value, *args, **kwargs):
        return value

class AtendimentoSchema(MM.Schema):
    cpf = cpf(required=True)
    private = fields.Boolean(required=True)
    incompleto = fields.Boolean(required=True)
    dta_u_compra = my_date()
    tkt_medio = my_float()
    tkt_u_compra = my_float()
    loja_frequente = cnpj()
    loja_u_compra = cnpj()

@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.route("/upload-file", methods = ['GET', 'POST'])
def upload_file():
    # print(request)
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        print(app.config['UPLOAD_FOLDER']+uploaded_file.filename)
        uploaded_file.save(app.config['UPLOAD_FOLDER']+uploaded_file.filename)
    # print(file)

@app.route("/process-file")
def process_file():
    with open(app.config['UPLOAD_FOLDER']+"base_teste.txt",'r') as file:
        lines = file.readlines()[1:]

    iteration = 1
    start = 0
    insertThreads = []
    for step in range(10000, len(lines), 10000):
        insertThreads.append(threading.Thread(target=thread_cleanup, args=("thread_"+str(iteration), lines[start:step])))
            
        if step+10000 > len(lines):
            insertThreads.append(threading.Thread(target=thread_cleanup, args=("thread_"+str(iteration+1), lines[start+10001: len(lines)])))

        start = step
        iteration+=1

    for t in insertThreads:
        t.start()

    for t in insertThreads:
        t.join()

    return jsonify(lines=len(lines))

def thread_cleanup(thread_name, data, generate=False):
    cleanup_data = []
    if generate:
        with open(app.config['UPLOAD_FOLDER']+"clean/"+thread_name,'w') as file:
            for line in data:
                file.write(re.sub('\s+', ',', re.sub(',', '.', line))[:-1]+'\r')
        return
    else:
        for i in range(len(data)):
            new_user = re.sub('\s+', ',', re.sub(',', '.', data[i]))[:-1].split(',')
            if len(new_user) != 8:
                print(new_user)
                continue
            cleanup_data.append({
                "cpf": new_user[0],
                "private": new_user[1],
                "incompleto": new_user[2],
                "dta_u_compra": new_user[3],
                "tkt_medio": new_user[4],
                "tkt_u_compra": new_user[5],
                "loja_frequente": new_user[6],
                "loja_u_compra": new_user[7]
                })
    atendimentos_checked = AtendimentoSchema(many=True).load(cleanup_data)
    atendimento_to_insert = []
    for ac in atendimentos_checked:
        atendimento_to_insert.append(
            User(
                cpf=ac["cpf"],
                private=ac["private"],
                incompleto=ac["incompleto"],
                dta_u_compra=ac["dta_u_compra"],
                tkt_medio=ac["tkt_medio"],
                tkt_u_compra=ac["tkt_u_compra"],
                loja_frequente=ac["loja_frequente"],
                loja_u_compra=ac["loja_u_compra"]
            )
        )
    db.session.add_all(atendimento_to_insert)
    db.session.commit()



    print('\n')
    print(thread_name, atendimentos_checked[0])
    print('\n')
    
@app.route("/test-file")
def test_file():
    atendimento_schema = AtendimentoSchema(many=True)
    atendimento = [
        {
            'cpf': '042.098.288-40',
            'private': 0,
            'incompleto': 0,
            'dta_u_compra': '2013-06-12',
            'tkt_medio': 161.22,
            'tkt_u_compra': 161.22,
            'loja_frequente': '79.379.491/0008-50',
            'loja_u_compra': '79.379.491/0008-50'
        },
        {
            'cpf': '042.098.288-40',
            'private': 0,
            'incompleto': 0,
            'dta_u_compra': '2013-06-12',
            'tkt_medio': 161.22,
            'tkt_u_compra': 161.22,
            'loja_frequente': '79.379.491/0008-50',
            'loja_u_compra': '79.379.491/0008-50'
        },
    ]
    print(atendimento[0]['cpf'])

    validate = atendimento_schema.load(atendimento)
    print(atendimento)
    print(validate)
    return jsonify(lines=validate)