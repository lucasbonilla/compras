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


class Atendimento(db.Model):
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
    ''' recebe o dado e limpa os caracteres '''
    def _deserialize(self, value, *args, **kwargs):
        computed_cpf = ''.join(filter(str.isdigit, value))
        return computed_cpf if cpfcnpj.validate(computed_cpf) and len(computed_cpf) == 11 else "00000000000"

    def _serialize(self, value, *args, **kwargs):
        return value

class cnpj(fields.Field):
    ''' recebe o dado e limpa os caracteres '''
    def _deserialize(self, value, *args, **kwargs):
        computed_cnpj = ''.join(filter(str.isdigit, value))
        return computed_cnpj if cpfcnpj.validate(computed_cnpj) and len(computed_cnpj) == 14 else None

    def _serialize(self, value, *args, **kwargs):
        return value

class my_date(fields.Field):
    ''' recebe a string e transforma em data '''
    def _deserialize(self, value, *args, **kwargs):
        return datetime.strptime(value, '%Y-%m-%d') if value not in['NULL', ''] else None

    def _serialize(self, value, *args, **kwargs):
        return value

class my_float(fields.Field):
    ''' recebe uma string no formato valor decimal e transfrma em float '''
    def _deserialize(self, value, *args, **kwargs):
        return float(value) if value not in['NULL', ''] else None

    def _serialize(self, value, *args, **kwargs):
        return value

class AtendimentoSchema(MM.Schema):
    ''' schema do atendimento '''
    cpf = cpf(required=True)
    private = fields.Boolean(required=True)
    incompleto = fields.Boolean(required=True)
    dta_u_compra = my_date()
    tkt_medio = my_float()
    tkt_u_compra = my_float()
    loja_frequente = cnpj()
    loja_u_compra = cnpj()

# rota que inicia o projeto
@app.route("/")
def hello_world():
    return jsonify(start=True)

# rota para upload de arquivo
@app.route("/upload-file", methods = ['GET', 'POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # salva o arquivo para consulta e processamento futuro
        uploaded_file.save(app.config['UPLOAD_FOLDER']+uploaded_file.filename)
    # inicia o processamento do arquivo
    process_file()
    return jsonify(processed=True)

def process_file():
    # abre e carrega o arquivo
    with open(app.config['UPLOAD_FOLDER']+"base_teste.txt",'r') as file:
        lines = file.readlines()[1:]

    iteration = 1
    start = 0
    insertThreads = []
    # "corta" as linhas de 10000 em 10000 independentemente de quantas linhas o arquivo possui
    # e gera as threads que precisar
    for step in range(10000, len(lines), 10000):
        insertThreads.append(
            threading.Thread(
                target=thread_cleanup,
                args=("thread_"+str(iteration), lines[start:step])))      
        if step+10000 > len(lines):
            insertThreads.append(
                threading.Thread(
                    target=thread_cleanup,
                    args=("thread_"+str(iteration+1), lines[start+10001: len(lines)])))

        start = step
        iteration+=1

    for t in insertThreads:
        t.start()

    for t in insertThreads:
        t.join()

    return jsonify(lines=len(lines))

def thread_cleanup(thread_name, data, generate=False):
    print("Iniciando thread %s" % thread_name)
    cleanup_data = []
    if generate:
        # validação feita somente para ver se o arquivo estava sendo gerado corretamente
        with open(app.config['UPLOAD_FOLDER']+"clean/"+thread_name,'w') as file:
            for line in data:
                file.write(re.sub('\s+', ',', re.sub(',', '.', line))[:-1]+'\r')
        return
    else:
        for i in range(len(data)):
            # remove as veirgulas de cada linha para tratar os valores decimais e
            # remove os espaços transformando tudo para uma linha separada por vírgulas
            # por fim gera um array desses dados
            new_user = re.sub('\s+', ',', re.sub(',', '.', data[i]))[:-1].split(',')
            # se o array contém menos que 8 itens ignora essa iteração
            if len(new_user) != 8:
                print(new_user)
                continue
            # cria o json para validação do marshmallow
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
    # carrega a lista de json no validador do marshmallow
    # o processamento pega cada json e valida e transforma tudo para o dado correto
    # que o model do sistema espera
    atendimentos_checked = AtendimentoSchema(many=True).load(cleanup_data)
    atendimento_to_insert = []
    for ac in atendimentos_checked:
        # carrega todos os dados em um array com o model do atendimento
        atendimento_to_insert.append(
            Atendimento(
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
    # salva na base de dados
    db.session.add_all(atendimento_to_insert)
    db.session.commit()
    print("Finalizando thread %s" % thread_name)
    
# função para teste do algoritmo de salvamento dos dados no postgres
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