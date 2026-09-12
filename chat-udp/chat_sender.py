import socket
import threading

TARGET_IP = "127.0.0.1"
PORT = 5001

pending_messages = {}  # Guarda as mensagens que ainda não receberam confirmação
msg_counter = 1
lock = threading.Lock()


def listen_receipts(sock):
    """Thread em background para receber recibos sem bloquear o terminal."""
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            raw = data.decode("utf-8")

            # TODO 1: Faz o parsing do recibo usando '|'
            # Exemplo: "DELIVERED|1"
            parts = raw.split("|")

            # TODO 2: Verifica se o tipo do recibo é "DELIVERED"
            if len(parts) == 2 and parts[0] == "DELIVERED":

                # TODO 3: Extrai o ID confirmado e transforma em inteiro
                message_id = int(parts[1])

                # TODO 4: Adquire o lock para acessar o dicionário
                # de forma segura enquanto a thread principal também pode acessá-lo
                with lock:
                    if message_id in pending_messages:
                        # Remove a mensagem da lista de pendentes
                        message_text = pending_messages.pop(message_id)

                        # Exibe aviso de que a mensagem foi entregue
                        print(
                            f"\n[✓✓ Entregue] ID: {message_id} | "
                            f"Mensagem: {message_text}"
                        )

        except Exception:
            # Encerra a thread caso ocorra algum erro no socket
            break


def run_chat_sender():
    global msg_counter

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Inicia a thread que processa os ACKs recebidos em segundo plano
        listener = threading.Thread(
            target=listen_receipts,
            args=(s,),
            daemon=True
        )
        listener.start()

        print("=== Mini-Chat UDP ===")
        print("Comandos especiais:")
        print("  /status   -> Mostra mensagens ainda pendentes")
        print("  /reenviar -> Reenvia todas as mensagens pendentes\n")

        while True:
            try:
                user_input = input("Digite uma mensagem: ").strip()

                if not user_input:
                    continue

                if user_input == "/status":
                    # TODO 5: Exibe quantas mensagens ainda estão pendentes
                    # e quais são seus IDs e conteúdos
                    with lock:
                        if not pending_messages:
                            print("[STATUS] Nenhuma mensagem pendente.")
                        else:
                            print(
                                f"[STATUS] {len(pending_messages)} "
                                f"mensagem(ns) pendente(s):"
                            )

                            for message_id, message_text in pending_messages.items():
                                print(
                                    f"  ID: {message_id} | "
                                    f"Mensagem: {message_text}"
                                )

                    continue

                if user_input == "/reenviar":
                    # TODO 6: Itera pelas mensagens pendentes e
                    # reenvia cada uma para o servidor
                    with lock:
                        if not pending_messages:
                            print("[REENVIAR] Nenhuma mensagem pendente.")
                        else:
                            for message_id, message_text in pending_messages.items():

                                # Monta novamente o pacote da mensagem
                                packet = f"MSG|{message_id}|{message_text}"

                                # Envia o pacote para o receiver
                                s.sendto(
                                    packet.encode("utf-8"),
                                    (TARGET_IP, PORT)
                                )

                                print(
                                    f"[REENVIADO] ID: {message_id} | "
                                    f"Mensagem: {message_text}"
                                )

                    continue

                # Fluxo de envio de mensagem normal:

                # TODO 7: Salva a mensagem atual no dicionário
                # usando o contador como ID
                with lock:
                    pending_messages[msg_counter] = user_input

                # TODO 8: Monta o pacote no formato:
                # "MSG|<ID>|<CONTEUDO>"
                packet = f"MSG|{msg_counter}|{user_input}"

                # TODO 9: Envia o pacote via UDP para o receiver
                s.sendto(
                    packet.encode("utf-8"),
                    (TARGET_IP, PORT)
                )

                # TODO 10: Informa que a mensagem foi enviada,
                # mas ainda está aguardando confirmação
                print(
                    f"[PENDENTE] ID: {msg_counter} | "
                    f"Mensagem enviada, aguardando entrega..."
                )

                # Incrementa o contador para a próxima mensagem
                msg_counter += 1

            except KeyboardInterrupt:
                print("\nEncerrando cliente...")
                break


if __name__ == "__main__":
    run_chat_sender()