from flask.cli import FlaskGroup

from project import app, db, User, AtendimentoSchema


cli = FlaskGroup(app)

@cli.command("destroy_db")
def destroy_db():
    db.drop_all()
    db.session.commit()

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    atendimento_schema = AtendimentoSchema(many=True)
    atendimento = {
        'cpf': '042.098.288-40',
        'private': 0,
        'incompleto': 0,
        'dta_u_compra': '2013-06-12',
        'tkt_medio': 161.22,
        'tkt_u_compra': 161.22,
        'loja_frequente': '79.379.491/0008-50',
        'loja_u_compra': '79.379.491/0008-50'
    }

    validate = atendimento_schema.load(atendimento)
    print(atendimento)
    print(validate)
    return

    db.session.add(User(
        cpf="042.098.288-40",
        private=0,
        incompleto=0,
        dta_u_compra="2013-06-12",
        tkt_medio=161.22,
        tkt_u_compra=161.22,
        loja_frequente="79.379.491/0008-50",
        loja_u_compra="79.379.491/0008-50"))
    db.session.commit()


if __name__ == "__main__":
    cli()