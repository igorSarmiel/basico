from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from secrets import token_hex
from os import path
from werkzeug.security import generate_password_hash
from datetime import timedelta
from flask_mail import Mail

app = Flask(__name__, template_folder="htmls", static_folder="utils")
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def Usuario_admin(Tabela, nome, email, senha):
    usuario_admin = Tabela.query.all()
    if len(usuario_admin) < 1:
        usuario_admin = Tabela(nome=nome, email=email, senha=generate_password_hash(senha), admin=True, ativo=True)
        db.session.add(usuario_admin)
        db.session.commit()



def criar_app():
    
    #Configuração do app
    app.config['SECRET_KEY'] = token_hex(32)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{path.join(path.dirname(path.abspath(__file__)), 'db/estudos.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.permanent_session_lifetime =  timedelta(minutes=15)


    #Iniciar o banco de dados  
    db.init_app(app)
    migrate.init_app(app, db, command='migrate')


    #configurando email
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587,
    app.config['MAIL_USERNAME'] = 'bolsaimw@gmail.com'
    app.config['MAIL_PASSWORD'] = 'sycn yuja lymr vcmi '
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail.init_app(app)


    from .models import Usuarios
    with app.app_context():
        db.create_all()
        Usuario_admin(Usuarios, "Administrador","igor_sarmiel@hotmail.com","123456")

    #Registrar as blueprints
    from .views import urls
    from .auth import auth
    from .questoes import questoes
    app.register_blueprint(urls)
    app.register_blueprint(auth)
    app.register_blueprint(questoes)

    return app

