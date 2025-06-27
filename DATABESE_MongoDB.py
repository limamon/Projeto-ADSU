import json
import os
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# === Credenciais seguras ===
usuario = os.getenv("MONGO_USER")
senha = quote_plus(os.getenv("MONGO_PASS"))

# === String de conexão ===
MONGO_URI = f"mongodb+srv://{usuario}:{senha}@cluster0.yvcp4gy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# === Nome do banco e coleção ===
DATABASE_NAME = "horarios_uerj"
COLLECTION_NAME = "disciplinas"

# === Carrega o arquivo JSON correto ===
with open("disciplinas_com_aulas.json", encoding="utf-8") as f:
    dados = json.load(f)

# === Conecta e atualiza ===
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
colecao = db[COLLECTION_NAME]

# === Apaga dados antigos e insere os novos ===
colecao.delete_many({})
colecao.insert_many(dados)

print("✅ Arquivo correto enviado com sucesso para o MongoDB Atlas.")
