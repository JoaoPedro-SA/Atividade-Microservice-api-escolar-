from flask import Blueprint, jsonify, request
from models.bancoSQLite import BancoSQLite
import requests
from config import GESTAO_API_BASE_URL

atividade_bp = Blueprint('atividade_bp', __name__)

API_ESCOLAR_URL = f"{GESTAO_API_BASE_URL}/api/professores"

def validar_professor(id_professor):
    try:
        resposta = requests.get(f"{API_ESCOLAR_URL}/{id_professor}", timeout=10)
        return resposta.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao validar professor: {e}")
        return None
    
@atividade_bp.route('/atividades', methods=['POST'])
def criar_atividade():
    data = request.get_json(silent=True) or {}
    campos_obrigatorios = ["id_professor", "nome_atividade", "nota"]

    if not all(campo in data for campo in campos_obrigatorios):
        return jsonify({"erro": "Dados incompletos"}), 400

    professor_valido = validar_professor(data["id_professor"])
    if professor_valido is None:
        return jsonify({"erro": "Erro ao conectar com a API de Professor"}), 503
    if not professor_valido:
        return jsonify({"erro": "Professor não encontrado"}), 404

    banco = BancoSQLite()
    try:
        banco.cursor.execute('''
            INSERT INTO ATIVIDADES ("id_professor", "nome_atividade", "nota")
            VALUES (?, ?, ?)
        ''', (
            data["id_professor"],
            data["nome_atividade"],
            data["nota"]
        ))
        banco.conexao.commit()
        return jsonify({"mensagem": "Atividade criada com sucesso"}), 201
    except Exception as e:
        print("Erro ao criar atividade:", e)
        return jsonify({"erro": "Erro ao criar atividade: " + str(e)}), 500
    finally:
        banco.close()

@atividade_bp.route('/atividades', methods=['GET'])
def listar_atividades():
    banco = BancoSQLite()
    try:
        banco.cursor.execute("SELECT * FROM ATIVIDADES")
        linhas = banco.cursor.fetchall()
        atividades = [{
            "id": linha["id"],
            "id_professor": linha["id_professor"],
            "nome_atividade": linha["nome_atividade"],
            "nota": linha["nota"]
        } for linha in linhas]
        return jsonify(atividades)
    except Exception as e:
        print("Erro ao listar atividades:", e)
        return jsonify({"erro": "Erro ao buscar atividades"}), 500
    finally:
        banco.close()
