from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from urllib.parse import quote_plus

app = Flask(__name__)

user = quote_plus("Ramon_DESC")
password = quote_plus("Ramon@DESC")  # Aqui está o problema

uri = f"mongodb+srv://{user}:{password}@cluster0.yvcp4gy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["horarios_uerj"]
aulas = db["disciplinas"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/aula')
def get_aula():
    codigo = request.args.get('codigo')
    turma = request.args.get('turma')

    resultado = aulas.find_one({
        "codigo": codigo,
        "turma": turma
    })

    if resultado:
        return jsonify({
            "disciplina": resultado["disciplina"],
            "professor": resultado["professor"],
            "aulas": resultado["aulas"]
        })
    else:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/api/busca_por_nome')
def busca_por_nome():
    nome = request.args.get('nome', '').lower()

    resultado = aulas.find_one({
        "$or": [
            {"disciplina": {"$regex": nome, "$options": "i"}},
            {"codigo": {"$regex": nome}}  # permite buscar por 03559
        ]
    })

    if resultado:
        return jsonify({
            "codigo": resultado["codigo"],
            "disciplina": resultado["disciplina"],
            "aulas": resultado["aulas"]
        })
    else:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)



