from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("home.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")

        if senha != confirmar:
            return "<h3>As senhas não coincidem!</h3>"

        return redirect(url_for("login"))

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/inicio")
def pagina_inicial():
    return render_template("home.html")

@app.route("/categorias")
def turismo():
    return render_template("categorias.html")

@app.route("/gastronomia")
def gastronomia():
    return render_template("gastronomia.html")

@app.route("/historia")
def historia():
    return render_template("historia.html")

@app.route("/religioso")
def religioso():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
  return render_template("sobre.html")

@app.route("/favoritos")
def favoritos():
    return "<h1>Página de favoritos ainda em construção</h1>"

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

@app.route("/cultural")
def cultura():
    return render_template("cultural.html")


if __name__ == "__main__":
    app.run(debug=True)