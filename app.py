from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configurar SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de datos
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proyecto = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(10), nullable=False)
    horas = db.Column(db.Float, nullable=False)
    comentario = db.Column(db.Text)

# Crear la tabla si no existe
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nuevo = Registro(
            proyecto=request.form["proyecto"],
            fecha=request.form["fecha"],
            horas=float(request.form["horas"]),
            comentario=request.form["comentario"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect("/")

    registros = Registro.query.all()
    return render_template("index.html", registros=[[r.proyecto, r.fecha, r.horas, r.comentario] for r in registros])

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
