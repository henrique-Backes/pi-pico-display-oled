import json
from unittest.mock import MagicMock, call, patch

import pytest
import serial

from modules import serial_comm


class TestConnect:
    """Testes para a funcao connect."""

    @patch("modules.serial_comm.serial.Serial")
    def test_connect_opens_serial_port(self, mock_serial_class):
        """Caminho Feliz: Conecta na porta com baudrate correto."""
        mock_instance = MagicMock()
        mock_serial_class.return_value = mock_instance

        serial_comm.connect(port="COM3", baudrate=115200)

        mock_serial_class.assert_called_once_with(
            port="COM3", baudrate=115200, timeout=2.0
        )
        assert serial_comm._serial_port == mock_instance

    @patch("modules.serial_comm.serial.Serial")
    def test_connect_raises_on_failure(self, mock_serial_class):
        """Falha: SerialException ao abrir a porta."""
        mock_serial_class.side_effect = serial.SerialException("Port not found")

        with pytest.raises(serial.SerialException, match="Port not found"):
            serial_comm.connect(port="COM_INVALID")

    def teardown_method(self):
        """Fecha conexao serial apos cada teste."""
        serial_comm.disconnect()


class TestDisconnect:
    """Testes para a funcao disconnect."""

    @patch("modules.serial_comm.serial.Serial")
    def test_disconnect_closes_open_port(self, mock_serial_class):
        """Caminho Feliz: Fecha a porta serial aberta."""
        mock_instance = MagicMock()
        mock_instance.is_open = True
        mock_serial_class.return_value = mock_instance

        serial_comm.connect(port="COM3")
        serial_comm.disconnect()

        mock_instance.close.assert_called_once()
        assert serial_comm._serial_port is None

    def test_disconnect_when_not_connected(self):
        """Falha: Desconectar sem conexao nao gera erro."""
        serial_comm._serial_port = None
        serial_comm.disconnect()
        assert serial_comm._serial_port is None


class TestSendData:
    """Testes para a funcao send_data."""

    @patch("modules.serial_comm.serial.Serial")
    def test_send_data_formats_json_correctly(self, mock_serial_class):
        """Caminho Feliz: Converte dict para JSON com newline e envia."""
        mock_instance = MagicMock()
        mock_instance.is_open = True
        mock_serial_class.return_value = mock_instance

        serial_comm.connect(port="COM_FAKE")

        sample_data = {"target": "CPU", "usage": 50.0, "temp": 60.0, "clock": 3000}
        serial_comm.send_data(sample_data)

        expected = (json.dumps(sample_data) + "\n").encode("utf-8")
        mock_instance.write.assert_called_once_with(expected)

    @patch("modules.serial_comm.serial.Serial")
    def test_send_data_raises_when_port_not_open(self, mock_serial_class):
        """Falha: Enviar sem conexao gera SerialException."""
        serial_comm._serial_port = None

        with pytest.raises(serial.SerialException, match="nao esta aberta"):
            serial_comm.send_data({"target": "CPU"})

    @patch("modules.serial_comm.serial.Serial")
    def test_send_data_raises_on_non_serializable(self, mock_serial_class):
        """Falha: Dict com tipo nao serializavel gera TypeError."""
        mock_instance = MagicMock()
        mock_instance.is_open = True
        mock_serial_class.return_value = mock_instance

        serial_comm.connect(port="COM_FAKE")

        with pytest.raises(TypeError):
            serial_comm.send_data({"target": object()})

    def teardown_method(self):
        """Fecha conexao serial apos cada teste."""
        serial_comm.disconnect()


class TestReadResponse:
    """Testes para a funcao read_response."""

    @patch("modules.serial_comm.serial.Serial")
    def test_read_response_returns_parsed_dict(self, mock_serial_class):
        """Caminho Feliz: Le linha e parseia JSON corretamente."""
        mock_instance = MagicMock()
        mock_instance.is_open = True
        ack_json = '{"status": "ACK", "msg": "CPU data updated"}\n'
        mock_instance.readline.return_value = ack_json.encode("utf-8")
        mock_serial_class.return_value = mock_instance

        serial_comm.connect(port="COM_FAKE")
        result = serial_comm.read_response()

        assert result == {"status": "ACK", "msg": "CPU data updated"}

    @patch("modules.serial_comm.serial.Serial")
    def test_read_response_returns_none_on_timeout(self, mock_serial_class):
        """Falha: Timeout na leitura retorna None."""
        mock_instance = MagicMock()
        mock_instance.is_open = True
        mock_instance.readline.return_value = b""
        mock_serial_class.return_value = mock_instance

        serial_comm.connect(port="COM_FAKE")
        result = serial_comm.read_response()

        assert result is None

    @patch("modules.serial_comm.serial.Serial")
    def test_read_response_returns_none_on_invalid_json(self, mock_serial_class):
        """Falha: JSON malformatado retorna None."""
        mock_instance = MagicMock()
        mock_instance.is_open = True
        mock_instance.readline.return_value = b"{invalid json}\n"
        mock_serial_class.return_value = mock_instance

        serial_comm.connect(port="COM_FAKE")
        result = serial_comm.read_response()

        assert result is None

    def test_read_response_returns_none_when_not_connected(self):
        """Falha: Leitura sem conexao retorna None."""
        serial_comm._serial_port = None
        result = serial_comm.read_response()
        assert result is None

    @patch("modules.serial_comm.serial.Serial")
    def test_read_response_returns_nack_dict(self, mock_serial_class):
        """Caminho Feliz: Parseia resposta NACK corretamente."""
        mock_instance = MagicMock()
        mock_instance.is_open = True
        nack_json = '{"status": "NACK", "msg": "JSON parse error"}\n'
        mock_instance.readline.return_value = nack_json.encode("utf-8")
        mock_serial_class.return_value = mock_instance

        serial_comm.connect(port="COM_FAKE")
        result = serial_comm.read_response()

        assert result == {"status": "NACK", "msg": "JSON parse error"}

    def teardown_method(self):
        """Fecha conexao serial apos cada teste."""
        serial_comm.disconnect()


class TestListAvailablePorts:
    """Testes para a funcao list_available_ports."""

    @patch("modules.serial_comm.serial.tools.list_ports.comports")
    def test_list_available_ports_returns_devices(self, mock_comports):
        """Caminho Feliz: Retorna lista de dispositivos seriais."""
        mock_port1 = MagicMock()
        mock_port1.device = "COM3"
        mock_port2 = MagicMock()
        mock_port2.device = "COM4"
        mock_comports.return_value = [mock_port2, mock_port1]

        result = serial_comm.list_available_ports()

        assert result == ["COM3", "COM4"]

    @patch("modules.serial_comm.serial.tools.list_ports.comports")
    def test_list_available_ports_returns_empty(self, mock_comports):
        """Falha: Nenhuma porta disponivel retorna lista vazia."""
        mock_comports.return_value = []

        result = serial_comm.list_available_ports()

        assert result == []
