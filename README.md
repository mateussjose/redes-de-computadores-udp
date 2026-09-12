# Chat via UDP — Confirmação de Entrega e Reenvio Manual
 
Atividade prática da disciplina de Redes de Computadores. Implementa um chat simplificado sobre **UDP** (`SOCK_DGRAM`), onde a própria aplicação — e não o protocolo de transporte — é responsável por confirmar a entrega das mensagens e retransmitir as que forem perdidas.
 
## Estrutura
 
```
chat-udp/
├── chat_sender.py    # Cliente: envia mensagens e controla pendências
└── chat_receiver.py  # Servidor: recebe mensagens e envia recibos
```
 
## Protocolo de Aplicação
 
| Tipo               | Formato                  | Exemplo                  |
|---------------------|---------------------------|----------------------------|
| Mensagem de texto   | `MSG\|<ID>\|<CONTEUDO>`   | `MSG\|1\|Oi, tudo bem?`    |
| Recibo de entrega   | `DELIVERED\|<ID>`         | `DELIVERED\|1`            |
 
O servidor simula perda de pacotes (`DROP_RATE = 0.4`, 40%) descartando datagramas aleatoriamente antes de processá-los.
 
## Como executar
 
Abra dois terminais na pasta `chat-udp/`:
 
**Terminal 1 — Servidor:**
```bash
python3 chat_receiver.py
```
 
**Terminal 2 — Cliente:**
```bash
python3 chat_sender.py
```
 
Digite mensagens normalmente no cliente. Use também os comandos especiais:
 
- `/status` — mostra quais mensagens ainda estão pendentes de confirmação.
- `/reenviar` — reenvia todas as mensagens pendentes para o servidor.
## Estratégia adotada
 
- Cada mensagem enviada recebe um **ID sequencial** e é guardada em `pending_messages` até que o recibo correspondente chegue.
- Uma **thread separada** (`listen_receipts`) fica escutando os recibos `DELIVERED|<ID>` em paralelo, sem travar a digitação de novas mensagens.
- Um `Lock` protege o acesso ao dicionário de pendências entre as threads.
- O reenvio (`/reenviar`) é **manual**, simulando em nível de aplicação o que o TCP faria automaticamente por timeout.
## Relatório
 
O relatório completo (estratégia, capturas de tela e discussão UDP x TCP) está disponível em [`relatorio_chat_udp.pdf`](./relatorio_chat_udp.pdf).
 
