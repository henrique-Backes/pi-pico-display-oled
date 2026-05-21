Módulo: Serial Comm (serial_comm.py)

1. Responsabilidade
Gerenciar a conexão USB Serial com o Pico, serializar os dicionários de dados em JSON e garantir o término com \n. Ler as respostas (ACK/NACK).

2. Interface Esperada

```python
def connect(port: str, baudrate: int = 115200) -> None:
    """Inicializa a conexão serial."""

def send_data(data: dict) -> None:
    """Converte dict para JSON e envia pela serial com '\\n'."""

def read_response() -> dict | None:
    """Lê uma linha da serial, parseia o JSON e retorna o dict."""
```

3. Guia de Desenvolvimento
- Utilizar a lib serial do pyserial.
- Garantir que o encode seja UTF-8 e adicionar \n no final: `serial_port.write((json.dumps(data) + '\n').encode('utf-8'))`.
- Implementar um timeout de leitura para evitar que o software trave esperando o Pico.
- Adicionar tratamento de exceções (serial.SerialException) para desconexão abrupta do Pico.
