import requests
from typing import List

class ResultadoFuzzing:
    def __init__(self, caminho: str, status_http: int, conteudo_resposta: str):
        self.caminho = caminho
        self.status_http = status_http
        self.conteudo_resposta = conteudo_resposta[:100]
    
    def __str__(self):
        return (
            f"Caminho testado: {self.caminho} | "
            f"Status HTTP: {self.status_http} | "
            f"Conteúdo (trecho): {self.conteudo_resposta}"
        )

class FuzzerHTTP:
    def __init__(self, url_base: str, caminhos: List[str]):
        self.url_base = url_base.rstrip('/')
        self.caminhos = caminhos

    def executar_fuzzing(self) -> List[ResultadoFuzzing]:
        resultados = []
        for caminho in self.caminhos:
            url_completa = f"{self.url_base}{caminho}"
            try:
                resposta = requests.get(url_completa, timeout=5)
                resultados.append(
                    ResultadoFuzzing(caminho, resposta.status_code, resposta.text)
                )
            except requests.exceptions.RequestException as erro:
                resultados.append(ResultadoFuzzing(caminho, -1, str(erro)))
        return resultados

    def filtrar_caminhos_suspeitos(self, resultados: List[ResultadoFuzzing]) -> List[ResultadoFuzzing]:
        suspeitos = []
        for r in resultados:
            if (r.status_http == 200 and "não encontrado" not in r.conteudo_resposta.lower()) or r.status_http == 500:
                suspeitos.append(r)
        return suspeitos

def main():
    url_servidor = "http://localhost:8080"
    caminhos_para_testar = [
        "/",
        "/admin",
        "/login",
        "/teste",
        "/usuario",
        "/painel",
        "/etc/passwd",
        "/config",
        "/.git",
        "/robots.txt"
    ]

    fuzzer = FuzzerHTTP(url_servidor, caminhos_para_testar)
    resultados = fuzzer.executar_fuzzing()
    
    print("=== RESULTADOS DO FUZZING ===")
    for r in resultados:
        print(r)
    
    suspeitos = fuzzer.filtrar_caminhos_suspeitos(resultados)
    print("\n=== RESULTADOS SUSPEITOS ===")
    if not suspeitos:
        print("Nenhum caminho suspeito identificado.")
    else:
        for s in suspeitos:
            print(s)

if __name__ == "__main__":
    main()
