from flask.cli import FlaskGroup

from project import app, db, Atendimento, AtendimentoSchema


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()