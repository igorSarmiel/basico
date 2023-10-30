from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import Usuarios
from functools import wraps
from random import randint

auth = Blueprint('auth', __name__, url_prefix='/auth')



#decorator para testar o login
def login_required(f):
    @wraps(f)
    def funcao_decorator(*args, **kwargs):
        if not "Nome" in session or not session['Admin']:
            flash("Para ter acesso você deve estar logado.",category="warning ")
            return redirect(url_for("urls.index"))
        return f(*args, **kwargs)
    return funcao_decorator



#logar usuario
@auth.route("/entrar", methods=['GET','POST'])
def entrar():
    if request.method == "POST":
        email = request.form.get('email_login')
        senha = request.form.get('senha_login')

        try:
            usuario_logar = Usuarios.query.filter_by(email=email).one()    
            if check_password_hash(usuario_logar.senha, senha): 
                session['Nome'] = usuario_logar.nome
                session['Admin'] = usuario_logar.admin
                session['Ip'] = request.remote_addr
                session['Id'] = usuario_logar.id
                
                return redirect(url_for('urls.index'))
            else:
                flash("Email ou senha não encontrados. ", category='danger')
                return redirect(url_for('urls.index'))
        except:
            flash("Email ou senha não encontrados. ", category='danger')
            return redirect(url_for('urls.index'))
    else:
        return redirect(url_for('urls.index'))



#deslogar usuario
@auth.route("/sair")
def sair():
    session.pop('Nome', None)
    session.pop('Admin', None)
    session.pop("Ip", None)
    return redirect(url_for('urls.index'))





#criar usuário
@auth.route("/registrar", methods=['GET','POST'])
def registrar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')
        if senha1 != senha2:
            flash("As senhas digitadas são diferentes.", category='danger')
            return redirect(url_for("auth.registrar"))
        else:
            try:
                novo_usuario = Usuarios(nome=nome, email=email, senha=generate_password_hash(senha1))
                db.session.add(novo_usuario)
                db.session.commit()
                flash("Registro feito com sucesso! Pode acessar o sistema.", category="success")
                return redirect(url_for("urls.index"))
            except:
                flash("Ocorreu um erro ao criar o usuário. \nPossivelmento o email já existe em nosso sistema. \nPor favor tente outro.", category="danger")
                return redirect(url_for("auth.registrar"))
    else:
        return render_template('registrar.html')




#apagar o usuário
@auth.route("/apagar/<int:id>", methods=['GET','POST'])
@login_required
def apagar(id):
    if request.method == 'POST':
        id_usuario = request.form.get('id_usuario')
        usuario_apagar = db.get_or_404(Usuarios, id_usuario)
        db.session.delete(usuario_apagar)
        db.session.commit()
        return redirect("/auth/listar")
    else:
        usuario_apagar = db.get_or_404(Usuarios, id)
        return render_template("usuarios.html", usuario_apagar=usuario_apagar)
        


#editar o usuário

#função para converter a string para boolean
funcao = lambda a: True if a == "True" else False

@auth.route("/editar/<int:id>", methods=["GET","POST"])
@login_required
def editar(id):
    if request.method == "POST":
        usuario_editar = db.get_or_404(Usuarios, id)
        novo_status_admin = funcao(request.form.get("user_admin"))
        novo_status_ativo = funcao(request.form.get("user_ativo"))
        print(type(novo_status_admin), usuario_editar.admin, novo_status_ativo, usuario_editar.ativo)
        if (novo_status_admin != usuario_editar.admin) or (novo_status_ativo != usuario_editar.ativo):
            usuario_editar.admin = novo_status_admin
            usuario_editar.ativo = novo_status_ativo
            db.session.commit()
            flash("Alterações salvas com sucesso.", "info")
            return redirect("/auth/listar")
        else:
            flash("Sem alterações feitas.", "info")
            return redirect("/auth/listar")
    else:
        usuario_editar = db.get_or_404(Usuarios, id)
        return render_template("usuarios.html", usuario_editar=usuario_editar)




#listar os usuários
@auth.route("/listar")
@login_required
def listar():
    lista_usuarios = db.session.execute(db.select(Usuarios).order_by(Usuarios.nome)).scalars()
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)


#mostra código de verificação quando pedir a alteração de senha
@auth.route("/verifica_codigo/<int:id>", methods=["GET","POST"])
@login_required
def verifica_codigo(id):
    if request.method == "POST":
        usuario_alterar_senha = Usuarios.query.get(id)
        token_informado = request.form.get("cod_ver")
        if usuario_alterar_senha.token == token_informado:
            return render_template("alterar_senha.html")
        else:
            flash("O código de verificação informado não é o mesmo que lhe foi enviado.", "danger")
            return redirect(url_for('urls.index'))
        
    else:
        try:
            from flask_mail import Message
            from . import mail
            #pegar tokem e email do usuario
            usuario_alterar_senha = Usuarios.query.get(id)

            msg = Message('Olá teste de email', sender = 'bolsaimw@gmail.com', recipients = [f'{usuario_alterar_senha.email}'])
            msg.body = f"Este email foi enviado devido a uma solicitação para alteração da senha do usuario {usuario_alterar_senha.nome}. Seu código de verificação é {usuario_alterar_senha.tokem}. Caso não tenha solicitado a alteração desconsidere."
            msg.html = "<h2>Código de verificação para alteração de senha.</h2>"
            mail.send(msg)
            return render_template("verifica_codigo.html")
        except Exception as e:
            flash(f"Erro apresentado: {e}", "danger")
            return render_template("verifica_codigo.html")
            


#alterar senha
@auth.route("/alterar_senha",  methods=["POST"])
@login_required
def alterar_senha():
    if request.method == "POST":
        nova_senha1 = request.form.get("nova_senha1")
        nova_senha2 = request.form.get("nova_senha2")
        if nova_senha1 == nova_senha2:
            usuario_alterar_senha = Usuarios.query.get(id)
            usuario_alterar_senha.senha = nova_senha1
            usuario_alterar_senha.token = str(randint(1000,9999))
            db.session.commit()
        return redirect(url_for('urls.index'))
    