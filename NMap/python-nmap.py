import nmap
import time

def varredura_sincrona(alvo, portas="1-1024"):
    scanner = nmap.PortScanner()
    resultado = {}
    # Alterado de -sS para -sT:
    scanner.scan(hosts=alvo, ports=portas, arguments='-sT')
    for host in scanner.all_hosts():
        portas_abertas = []
        if 'tcp' in scanner[host]:
            for porta, info in scanner[host]['tcp'].items():
                if info['state'] == 'open':
                    portas_abertas.append(porta)
        resultado[host] = portas_abertas
    return resultado

def varredura_assincrona(alvo, portas="1-1024"):
    scanner = nmap.PortScannerAsync()
    hosts_resultados = {}

    def callback_result(host, scan_result):
        portas_abertas = []
        if host in scan_result:
            if 'tcp' in scan_result[host]:
                for porta, info in scan_result[host]['tcp'].items():
                    if info['state'] == 'open':
                        portas_abertas.append(porta)
        hosts_resultados[host] = portas_abertas

    # Alterado de -sS para -sT:
    scanner.scan(hosts=alvo, ports=portas, arguments='-sT', callback=callback_result)
    while scanner.still_scanning():
        time.sleep(2)
    return hosts_resultados

def main():
    alvo_sincrono = "127.0.0.1"
    alvo_assincrono = "scanme.nmap.org"
    
    print("=== Varredura Síncrona ===")
    resultado_sincrono = varredura_sincrona(alvo_sincrono, "21-443")
    for host, portas in resultado_sincrono.items():
        print(f"Host: {host} - Portas abertas: {portas}")
    
    print("\n=== Varredura Assíncrona ===")
    resultado_assincrono = varredura_assincrona(alvo_assincrono, "21-443")
    for host, portas in resultado_assincrono.items():
        print(f"Host: {host} - Portas abertas: {portas}")

if __name__ == "__main__":
    main()
