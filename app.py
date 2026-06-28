from config import *
from controllers.atividade_controller import atividade_bp
from models.bancoSQLite import importar_professores_da_api
from models.bancoSQLite import inicializar_banco

app = create_app()
app.register_blueprint(atividade_bp)


inicializar_banco()
importar_professores_da_api()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
