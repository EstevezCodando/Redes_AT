from scapy.all import ARP, Ether, IP, TCP, srp, sr1, conf
import time

conf.verb = 0  # Silencia a saída do Scapy

def escanear_arp(rede="192.168.1.0/24", interface="wlp4s0"):
    """
    Realiza escaneamento ARP e retorna lista de IPs ativos.
    """
    print(f"[+] Escaneando IPs ativos na rede {rede}...")
    pacote = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=rede)
    respostas, _ = srp(pacote, timeout=2, iface=interface, verbose=False)

    ips = []
    for _, receb in respostas:
        ips.append(receb.psrc)
    
    return ips

def escanear_portas(ip, portas, timeout=1):
    """
    Verifica quais portas TCP estão abertas no IP especificado.
    """
    portas_abertas = []
    for porta in portas:
        pacote = IP(dst=ip)/TCP(dport=porta, flags="S")
        resposta = sr1(pacote, timeout=timeout)

        if resposta and resposta.haslayer(TCP):
            if resposta.getlayer(TCP).flags == 0x12:  # SYN-ACK
                portas_abertas.append(porta)
                # Envia RST para fechar conexão
                sr1(IP(dst=ip)/TCP(dport=porta, flags="R"), timeout=1)
        time.sleep(0.1)  # Evita flood
    return portas_abertas

if __name__ == "__main__":
    # Configurações
    rede_local = "192.168.1.0/24"
    interface = "wlp4s0"
    portas_para_verificar = [22, 80, 443, 53, 3306, 8080]

    # Etapa 1: Descobrir IPs ativos
    ips_ativos = escanear_arp(rede=rede_local, interface=interface)

    print("\n[+] IPs ativos encontrados:")
    for ip in ips_ativos:
        print(f"  - {ip}")

    # Etapa 2: Verificar portas abertas para cada IP
    print("\n[+] Verificando portas abertas para cada IP...\n")

    for ip in ips_ativos:
        print(f"↪ IP: {ip}")
        abertas = escanear_portas(ip, portas_para_verificar)
        if abertas:
            print(f"  Portas abertas: {', '.join(map(str, abertas))}")
        else:
            print("  Nenhuma porta das verificadas está aberta.")
        print("-" * 40)
