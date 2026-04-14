from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def inicio():
    return redirect(url_for("cadastro"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")

        if senha != confirmar:
            return "<h3>As senhas não coincidem!</h3>"

        return redirect(url_for("login"))

    return render_template("cadastro1.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        return redirect(url_for("pagina_inicial"))

    return render_template("login.html")

@app.route("/inicio")
def pagina_inicial():
    return render_template("pagina_inicial.html")

@app.route("/turismo")
def turismo():
    return render_template("turismo.html")

@app.route("/gastronomico")
def gastronomico():
    return render_template("gastronomico.html")

@app.route("/historico")
def historico():
    return render_template("historico.html")

@app.route("/eventos")
def eventos():
    return "<h1>Página de eventos ainda em construção</h1>"

@app.route("/religioso")
def religioso():
    return render_template("religioso.html")

@app.route("/sobre")
def sobre():
    return "<h1>Página de eventos ainda em construção</h1>"

@app.route("/favoritos")
def favoritos():
    return "<h1>Página de eventos ainda em construção</h1>"

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

