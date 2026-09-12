import random
import socket

HOST = "0.0.0.0"
PORT = 5001
DROP_RATE = 0.4  # 40% de perda simulada no canal


def run_chat_receiver():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"[Chat Server] Online na porta {PORT} (Drop Rate: {DROP_RATE * 100}%)...")

        while True:
            data, addr = s.recvfrom(1024)

            # Simulação de descarte de pacote
            if random.random() < DROP_RATE:
                print("[CANAL] Pacote descartado artificialmente!")
                continue

            # Converte os dados recebidos de bytes para texto
            raw_message = data.decode("utf-8")

            # TODO 1: Divide a mensagem usando o caractere '|'
            # Exemplo de mensagem: "MSG|123|Olá, tudo bem?"
            parts = raw_message.split("|")

            # TODO 2: Verifica se a mensagem possui o formato esperado
            # e se o primeiro campo é do tipo 'MSG'
            if len(parts) >= 3 and parts[0] == "MSG":

                # TODO 3: Extrai o ID da mensagem e o texto enviado pelo usuário
                message_id = parts[1]
                message_text = "|".join(parts[2:])

                # TODO 4: Exibe no terminal a mensagem recebida e seu ID
                print(f"[RECEBIDO] ID: {message_id} | Mensagem: {message_text}")

                # TODO 5: Monta o pacote de recibo no formato "DELIVERED|<ID>"
                ack = f"DELIVERED|{message_id}"

                # TODO 6: Envia o recibo de volta para o endereço de origem
                s.sendto(ack.encode("utf-8"), addr)

                print(f"[ACK] Recibo enviado: {ack}")

            else:
                # Caso a mensagem não seja do tipo MSG ou esteja mal formatada
                print("[ERRO] Pacote recebido em formato inválido.")


if __name__ == "__main__":
    run_chat_receiver()
