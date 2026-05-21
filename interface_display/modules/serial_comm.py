import json

import serial
import serial.tools.list_ports


_serial_port = None


def connect(port: str, baudrate: int = 115200) -> None:
    """Inicializa a conexao serial.

    Args:
        port: Porta serial (ex: COM3 ou /dev/ttyACM0).
        baudrate: Velocidade da conexao, default 115200.

    Raises:
        serial.SerialException: Se nao for possivel abrir a porta.
    """
    global _serial_port
    _serial_port = serial.Serial(port=port, baudrate=baudrate, timeout=2.0)


def disconnect() -> None:
    """Fecha a conexao serial se estiver aberta."""
    global _serial_port
    if _serial_port and _serial_port.is_open:
        _serial_port.close()
    _serial_port = None


def send_data(data: dict) -> None:
    """Converte dict para JSON e envia pela serial com newline.

    Args:
        data: Dicionario com os dados a enviar.

    Raises:
        serial.SerialException: Se a porta serial nao estiver aberta.
        TypeError: Se o dict nao for serializavel para JSON.
    """
    global _serial_port
    if not _serial_port or not _serial_port.is_open:
        raise serial.SerialException("Porta serial nao esta aberta.")
    payload = (json.dumps(data) + "\n").encode("utf-8")
    _serial_port.write(payload)


def read_response() -> dict | None:
    """Le uma linha da serial, parseia o JSON e retorna o dict.

    Returns:
        dict: Dicionario parseado do JSON de resposta, ou None se
              houver timeout ou erro de parsing.
    """
    global _serial_port
    if not _serial_port or not _serial_port.is_open:
        return None
    try:
        raw_line = _serial_port.readline()
        if not raw_line:
            return None
        decoded = raw_line.decode("utf-8").strip()
        if not decoded:
            return None
        return json.loads(decoded)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def list_available_ports() -> list[str]:
    """Lista as portas seriais disponiveis no sistema.

    Returns:
        Lista de strings com os dispositivos seriais encontrados.
    """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in sorted(ports, key=lambda p: p.device)]
