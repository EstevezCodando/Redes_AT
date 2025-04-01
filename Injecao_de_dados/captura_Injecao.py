import pcapy
import struct
import time

def callback_captura(hdr, dados):
    # hdr inclui timestamp e tamanho do pacote
    print(f"[Pacote Recebido] Tamanho: {hdr.getlen()} bytes")
    # Exibindo apenas os 14 primeiros bytes (cabeçalho Ethernet)
    ethernet_header = dados[:14]
    eth_fields = struct.unpack('!6s6sH', ethernet_header)
    tipo_eth = eth_fields[2]
    print(f"  Tipo Ethernet: 0x{tipo_eth:04x}")

def capturar_pacotes(nome_interface, num_pacotes=5):
    # Abre a interface no modo promíscuo, snaplen = 65535, timeout = 100ms
    capturador = pcapy.open_live(nome_interface, 65535, 1, 100)
    print(f"Iniciando captura na interface: {nome_interface}")
    capturador.loop(num_pacotes, callback_captura)
    print(f"Captura de {num_pacotes} pacotes finalizada.")

def injetar_pacote(nome_interface):
    # Cria uma instância para injeção
    # Usamos o mesmo open_live; 'sendpacket' injeta pacotes brutos
    injecao = pcapy.open_live(nome_interface, 65535, 1, 100)

    # Montando um pacote Ethernet + IP + UDP muito simples (incompleto)
    # Exemplo: MAC de destino (ff:ff:ff:ff:ff:ff), MAC de origem (00:11:22:33:44:55),
    # tipo Ethernet 0x0800 (IPv4), cabeçalho IPv4 e cabeçalho UDP minimamente artificiais
    mac_destino = b'\xff\xff\xff\xff\xff\xff'
    mac_origem = b'\x00\x11\x22\x33\x44\x55'
    tipo_ethernet = b'\x08\x00'
    # Cabeçalho IP (20 bytes, MUITO simplificado): 
    # versão e IHL, DSCP/ECN, total length, ID, flags/offset, TTL, protocolo, checksum, IP src e IP dst
    ip_header = b'\x45\x00\x00\x1c\xab\xcd\x00\x00\x40\x11\x00\x00\x0a\x00\x00\x01\x0a\x00\x00\x02'
    # Cabeçalho UDP (8 bytes: porta origem, porta destino, comprimento, checksum)
    udp_header = b'\x04\xd2\x00\x35\x00\x08\x00\x00'

    pacote = mac_destino + mac_origem + tipo_ethernet + ip_header + udp_header

    print(f"Injetando pacote de teste na interface: {nome_interface}")
    injecao.sendpacket(pacote)
    print("Pacote injetado com sucesso.")

def main():
    interface_teste = "wlp4s0"

    capturar_pacotes(interface_teste, num_pacotes=5)

    # Aguardar alguns segundos antes de injetar
    time.sleep(2)

    # Injetar um pacote
    injetar_pacote(interface_teste)

if __name__ == "__main__":
    main()
