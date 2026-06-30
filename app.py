from config import *
from controllers.atividade_controller import atividade_bp
from docs import docs_bp
from flask import jsonify
from models.bancoSQLite import importar_professores_da_api
from models.bancoSQLite import inicializar_banco

app = create_app()
app.register_blueprint(atividade_bp)
app.register_blueprint(docs_bp)


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "atividade",
        "api_target": API_TARGET,
        "dependencies": {
            "gestao": GESTAO_API_BASE_URL,
            "reserva": RESERVA_API_BASE_URL,
        },
    })


inicializar_banco()
if SYNC_ON_STARTUP:
    importar_professores_da_api()


if __name__ == '__main__':
    import os
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5002)),
    )
