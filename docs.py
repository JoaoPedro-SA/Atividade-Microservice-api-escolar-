from flask import Blueprint, jsonify, Response

docs_bp = Blueprint("docs", __name__)

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "API de Atividades",
        "version": "1.0.0",
        "description": "Microservico para cadastro e listagem de atividades vinculadas a professores.",
    },
    "servers": [
        {"url": "https://atividade-microservice-api-escolar.onrender.com"},
        {"url": "http://localhost:5002"},
    ],
    "paths": {
        "/atividades": {
            "get": {
                "summary": "Lista atividades",
                "responses": {
                    "200": {
                        "description": "Lista de atividades",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Atividade"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "summary": "Cria uma atividade",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/NovaAtividade"},
                            "example": {
                                "id_professor": 1,
                                "nome_atividade": "RPA",
                                "nota": 5,
                            },
                        }
                    },
                },
                "responses": {
                    "201": {"description": "Atividade criada"},
                    "400": {"description": "Dados incompletos"},
                    "404": {"description": "Professor nao encontrado"},
                    "503": {"description": "Erro ao conectar com a API de Professor"},
                },
            },
        },
        "/atividades/{atividade_id}": {
            "delete": {
                "summary": "Remove uma atividade",
                "parameters": [
                    {
                        "name": "atividade_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "responses": {
                    "200": {"description": "Atividade removida"},
                    "404": {"description": "Atividade nao encontrada"},
                    "500": {"description": "Erro ao deletar atividade"},
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Atividade": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "id_professor": {"type": "integer", "example": 1},
                    "nome_atividade": {"type": "string", "example": "RPA"},
                    "nota": {"type": "number", "example": 5},
                },
            },
            "NovaAtividade": {
                "type": "object",
                "required": ["id_professor", "nome_atividade", "nota"],
                "properties": {
                    "id_professor": {"type": "integer", "example": 1},
                    "nome_atividade": {"type": "string", "example": "RPA"},
                    "nota": {"type": "number", "example": 5},
                },
            },
        }
    },
}


@docs_bp.get("/swagger.json")
def swagger_json():
    return jsonify(OPENAPI_SPEC)


@docs_bp.get("/docs")
def swagger_ui():
    html = """
<!doctype html>
<html>
  <head>
    <title>API de Atividades - Docs</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.onload = () => {
        window.ui = SwaggerUIBundle({
          url: "/swagger.json",
          dom_id: "#swagger-ui"
        });
      };
    </script>
  </body>
</html>
"""
    return Response(html, mimetype="text/html")
