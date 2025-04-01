import dns.resolver
from dns.exception import DNSException

def consultar_dns(dominio):
    print(f"\n🔍 Consultas DNS para: {dominio}\n")
    tipos = ["NS", "A", "MX", "TXT", "SOA"]
    for tipo in tipos:
        try:
            respostas = dns.resolver.resolve(dominio, tipo)
            for rdata in respostas:
                print(f"{tipo}: {rdata.to_text()}")
        except DNSException as e:
            print(f"{tipo}: Erro ao consultar ({e})")

if __name__ == "__main__":
    dominio = input("Informe o domínio (ex: google.com): ").strip()
    consultar_dns(dominio)
