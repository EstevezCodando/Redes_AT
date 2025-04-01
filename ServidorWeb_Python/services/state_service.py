class StateService:
    """
    Serviço responsável por gerenciar o estado (Ligado/Desligado).
    Demonstra uma lógica simples, mas isolada da camada de controle.
    """
    def __init__(self) -> None:
        self._state = "Desligado"

    def get_state(self) -> str:
        """
        Retorna o estado atual.
        """
        return self._state

    def toggle_state(self) -> None:
        """
        Alterna o estado entre 'Ligado' e 'Desligado'.
        """
        if self._state == "Desligado":
            self._state = "Ligado"
        else:
            self._state = "Desligado"
