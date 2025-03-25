from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
DATA_FILE = "data.csv"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        proyecto = request.form["proyecto"]
        fecha = request.form["fecha"]
        horas = request.form["horas"]
        comentario = request.form["comentario"]

        with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([proyecto, fecha, horas, comentario])

        return redirect("/")  # Redirige para evitar reenvíos

    # Leer datos
    registros = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            registros = list(reader)

    return render_template("index.html", registros=registros)

if __name__ == "__main__":
    app.run(debug=True)
