from flask import Flask, render_template, request, redirect, session, flash, url_for

class Loja:
    def __init__(self, nome, segmento,endereco):
        self.nome=nome
        self.segmento=segmento
        self.endereco=endereco

loja1 = Loja("haurum", "Horifruit", "Rua cenoura, 123")
loja2 = Loja("1,99", "Diversos", "Rua Batata, 321")

lista = [loja1, loja2]

app = Flask(__name__)
app.secret_key = "Haurum"

@app.route("/index")
def index():
    if "user_logado" not in session or session["user_logado"] == None:
        return redirect(url_for("login", proxima=url_for("index")))
    return render_template("haurum.html", titulo="Teste", mercado_lista=lista)

@app.route("/cadastro")
def cadastro():
    if "user_logado" not in session or session["user_logado"] == None:
        return redirect(url_for("login", proxima=url_for("cadastro")))
    return render_template("add_loja.html", titulo="Cadastro")

@app.route("/criar", methods=["POST",])
def criar():
    nome = request.form["nome"]
    segmento = request.form["segmento"]
    endereco = request.form["endereco"]
    lista.append(Loja(nome, segmento, endereco))
    return redirect(url_for("index"))

@app.route("/autenticar", methods=["POST",])
def autenticar():
    if "batata" == request.form["senha"]:
        proxima = request.form["proxima"]
        if proxima == "None": proxima = url_for("index")
        session["user_logado"] = request.form["usuario"]
        flash(session["user_logado"] + " Usuario logado!" + proxima)
        return redirect(proxima)
    else:
        flash(f"Login errado")
        return redirect(url_for("login"))
    
@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", titulo="Login", proxima=proxima)

@app.route("/logout")
def logout():
    session["user_logado"] = None
    flash("Logout Feito")
    return redirect(url_for("login"))

app.run()