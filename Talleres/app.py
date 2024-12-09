from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hola():
    return "<H1>HOLA<H1>"


@app.route("/api/saludo", methods=["GET"])
def saludo():
    return "Sueño contigo que me has dado"

@app.route("/api/mongo", methods=["GET"])
def mongo():
    filtro = request.args["col1"]
    churro = ""
    # Simple default connection
    client = MongoClient(churro)  # Connects to localhost:27017
    mydb = client["mydb"]
    tabla = mydb["tabla"]
    return str(list(tabla.find({"col1":filtro},{"_id":0})))


app.run(debug=True)
