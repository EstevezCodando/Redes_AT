from scapy.all import sniff, IP, TCP, UDP, ARP
from datetime import datetime

def exibir_pacote(pacote):
    """
    Função chamada para cada pacote capturado.
    Imprime informações básicas da transferência.
    """
    tempo = datetime.now().strftime("%H:%M:%S")
    if IP in pacote:
        ip_src = pacote[IP].src
        ip_dst = pacote[IP].dst
        protocolo = pacote[IP].proto
        print(f"[{tempo}] IP {ip_src} → {ip_dst} (PROTO {protocolo})")

        if TCP in pacote:
            print(f"   ↳ TCP: Porta {pacote[TCP].sport} → {pacote[TCP].dport}")
        elif UDP in pacote:
            print(f"   ↳ UDP: Porta {pacote[UDP].sport} → {pacote[UDP].dport}")

    elif ARP in pacote:
        print(f"[{tempo}] ARP: {pacote[ARP].psrc} está perguntando quem tem {pacote[ARP].pdst}")

if __name__ == "__main__":
    print("[+] Sniffer iniciado (pressione Ctrl+C para parar)...\n")
    sniff(prn=exibir_pacote, store=0)
