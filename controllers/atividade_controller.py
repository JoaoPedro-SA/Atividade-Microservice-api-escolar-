from flask import Blueprint, jsonify, request
import requests

from config import GESTAO_API_BASE_URL
from models.bancoSQLite import BancoSQLite

atividade_bp = Blueprint("atividade_bp", __name__)

API_ESCOLAR_URL = f"{GESTAO_API_BASE_URL}/api/professores"


def validar_professor(id_professor):
    try:
        resposta = requests.get(f"{API_ESCOLAR_URL}/{id_professor}", timeout=10)
        return resposta.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao validar professor: {e}")
        return None


@atividade_bp.route("/atividades", methods=["POST"])
def criar_atividade():
    data = request.get_json(silent=True) or {}
    campos = ["id_professor", "nome_atividade", "nota"]
    if not all(campo in data for campo in campos):
        return jsonify({"erro": "Dados incompletos"}), 400
    if not str(data["id_professor"]).isdigit():
        return jsonify({"erro": "id_professor deve ser um numero inteiro"}), 400
    if not str(data["nome_atividade"]).strip():
        return jsonify({"erro": "nome_atividade e obrigatorio"}), 400

    try:
        nota = float(data["nota"])
    except (TypeError, ValueError):
        return jsonify({"erro": "nota deve ser um numero"}), 400
    if nota < 0 or nota > 10:
        return jsonify({"erro": "nota deve estar entre 0 e 10"}), 400

    id_professor = int(data["id_professor"])
    professor_valido = validar_professor(id_professor)
    if professor_valido is None:
        return jsonify({"erro": "Erro ao conectar com a API de Professor"}), 503
    if not professor_valido:
        return jsonify({"erro": "Professor nao encontrado"}), 404

    banco = BancoSQLite()
    try:
        banco.cursor.execute(
            """
            INSERT INTO ATIVIDADES (id_professor, nome_atividade, nota)
            VALUES (?, ?, ?)
            """,
            (id_professor, data["nome_atividade"], nota),
        )
        banco.conexao.commit()
        return jsonify({"mensagem": "Atividade criada com sucesso", "id": banco.cursor.lastrowid}), 201
    except Exception as e:
        print("Erro ao criar atividade:", e)
        return jsonify({"erro": "Erro ao criar atividade: " + str(e)}), 500
    finally:
        banco.close()


@atividade_bp.route("/atividades", methods=["GET"])
def listar_atividades():
    banco = BancoSQLite()
    try:
        banco.cursor.execute("SELECT * FROM ATIVIDADES")
        linhas = banco.cursor.fetchall()
        return jsonify([
            {
                "id": linha["id"],
                "id_professor": linha["id_professor"],
                "nome_atividade": linha["nome_atividade"],
                "nota": linha["nota"],
            }
            for linha in linhas
        ])
    except Exception as e:
        print("Erro ao listar atividades:", e)
        return jsonify({"erro": "Erro ao buscar atividades"}), 500
    finally:
        banco.close()


@atividade_bp.route("/atividades/<int:atividade_id>", methods=["DELETE"])
def deletar_atividade(atividade_id):
    banco = BancoSQLite()
    try:
        banco.cursor.execute("DELETE FROM ATIVIDADES WHERE id = ?", (atividade_id,))
        banco.conexao.commit()
        if banco.cursor.rowcount == 0:
            return jsonify({"erro": "Atividade nao encontrada"}), 404
        return jsonify({"mensagem": "Atividade removida com sucesso"}), 200
    except Exception as e:
        print("Erro ao deletar atividade:", e)
        return jsonify({"erro": "Erro ao deletar atividade: " + str(e)}), 500
    finally:
        banco.close()
