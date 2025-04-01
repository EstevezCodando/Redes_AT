from flask import Flask
from controllers.home_controller import home_bp

def create_app():
    """
    Fábrica de criação da aplicação Flask, seguindo boas práticas.
    Permite maior flexibilidade e testes.
    """
    app = Flask(__name__)
    # Registro do blueprint
    app.register_blueprint(home_bp)
    return app

if __name__ == "__main__":
    # Inicializa e roda o servidor
    application = create_app()
    # debug=True é útil em desenvolvimento; em prod, utilize de outro modo
    application.run(debug=True, host="127.0.0.1", port=5000)
