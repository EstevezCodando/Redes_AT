from flask import Blueprint, request, render_template_string
from services.state_service import StateService

home_bp = Blueprint("home_bp", __name__)
state_service = StateService()  # Instância única para este exemplo

@home_bp.route("/", methods=["GET", "POST"])
def index():
    """
    Rota principal que exibe o estado atual e permite alterná-lo.
    """
    if request.method == "POST":
        state_service.toggle_state()
    
    # Recuperamos o estado para exibir na página
    current_state = state_service.get_state()
    # Um html simples pra mudar o status e verificar o servidor funcionando

    html = """
    <html>
      <head>
        <title>Servidor Web Python</title>
      </head>
      <body>
        <h1>Estado atual: {{state}}</h1>
        <form method="POST" action="/">
          <button type="submit">Alternar Estado</button>
        </form>
      </body>
    </html>
    """

    return render_template_string(html, state=current_state)
