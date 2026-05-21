from unittest.mock import MagicMock, patch

import pytest


class TestPcMonitorAppCreation:
    """Testes de criacao da aplicacao GUI com CustomTkinter mockado."""

    def test_app_title_and_geometry_set_on_init(self):
        """Caminho Feliz: App define titulo e geometria na inicializacao."""
        from modules.gui import PcMonitorApp

        with patch.object(PcMonitorApp, "__init__", lambda self: None):
            app = PcMonitorApp()
            app.title = MagicMock()
            app.geometry = MagicMock()
            app.resizable = MagicMock()
            app._monitoring = False
            app._monitor_thread = None

            app.title("PC Monitor - Pico Display")
            app.geometry("520x600")

            app.title.assert_called_once_with("PC Monitor - Pico Display")
            app.geometry.assert_called_once_with("520x600")

    @patch("modules.gui.list_available_ports", return_value=["COM3", "COM4"])
    def test_refresh_ports_populates_combo(self, mock_list_ports):
        """Caminho Feliz: Refresh ports atualiza a lista de portas."""
        mock_combo = MagicMock()
        mock_log = MagicMock()

        from modules.gui import PcMonitorApp

        with patch.object(PcMonitorApp, "__init__", lambda self: None):
            app = PcMonitorApp()
            app._port_combo = mock_combo
            app._log = mock_log
            app._refresh_ports()

            mock_combo.configure.assert_called_once_with(values=["COM3", "COM4"])
            mock_combo.set.assert_called_once_with("COM3")

    @patch("modules.gui.list_available_ports", return_value=[])
    def test_refresh_ports_no_ports_shows_empty(self, mock_list_ports):
        """Falha: Nenhuma porta disponivel, combo mostra vazio."""
        mock_combo = MagicMock()
        mock_log = MagicMock()

        from modules.gui import PcMonitorApp

        with patch.object(PcMonitorApp, "__init__", lambda self: None):
            app = PcMonitorApp()
            app._port_combo = mock_combo
            app._log = mock_log
            app._refresh_ports()

            mock_combo.configure.assert_called_once_with(values=[""])
            mock_combo.set.assert_called_once_with("")


class TestPcMonitorAppStartStop:
    """Testes de inicio e parada do monitoramento."""

    def _make_app(self):
        """Cria uma instancia de PcMonitorApp com __init__ mockado."""
        from modules.gui import PcMonitorApp

        with patch.object(PcMonitorApp, "__init__", lambda self: None):
            app = PcMonitorApp()
            app._monitoring = False
            app._monitor_thread = None
            app._port_combo = MagicMock()
            app._baud_entry = MagicMock()
            app._baud_entry.get.return_value = "115200"
            app._start_btn = MagicMock()
            app._stop_btn = MagicMock()
            app._refresh_btn = MagicMock()
            app._log_text = MagicMock()
            app._status_label = MagicMock()
            app._log = MagicMock()
            app._set_status = MagicMock()
            app.after = MagicMock()
            return app

    @patch("modules.gui.connect")
    @patch("modules.gui.threading.Thread")
    def test_start_monitoring_connects_and_starts_thread(
        self, mock_thread, mock_connect
    ):
        """Caminho Feliz: Iniciar monitoramento conecta e cria thread."""
        app = self._make_app()
        app._port_combo.get.return_value = "COM3"
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        app._start_monitoring()

        mock_connect.assert_called_once_with(port="COM3", baudrate=115200)
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()
        assert app._monitoring is True
        app._start_btn.configure.assert_called_with(state="disabled")
        app._stop_btn.configure.assert_called_with(state="normal")

    @patch("modules.gui.connect")
    def test_start_monitoring_no_port_shows_error(self, mock_connect):
        """Falha: Iniciar sem porta selecionada loga erro."""
        app = self._make_app()
        app._port_combo.get.return_value = ""

        app._start_monitoring()

        mock_connect.assert_not_called()
        app._log.assert_called()

    @patch("modules.gui.connect", side_effect=Exception("Port not found"))
    def test_start_monitoring_connection_failure(self, mock_connect):
        """Falha: Erro ao conectar loga erro e nao inicia thread."""
        app = self._make_app()
        app._port_combo.get.return_value = "COM_INVALID"

        app._start_monitoring()

        app._log.assert_called()

    @patch("modules.gui.disconnect")
    def test_stop_monitoring_disconnects(self, mock_disconnect):
        """Caminho Feliz: Parar monitoramento desconecta e atualiza UI."""
        app = self._make_app()
        app._monitoring = True

        app._stop_monitoring()

        mock_disconnect.assert_called_once()
        assert app._monitoring is False
        app._start_btn.configure.assert_called_with(state="normal")
        app._stop_btn.configure.assert_called_with(state="disabled")


class TestSendAndValidate:
    """Testes para o metodo _send_and_validate."""

    def _make_app(self):
        """Cria uma instancia de PcMonitorApp com __init__ mockado."""
        from modules.gui import PcMonitorApp

        with patch.object(PcMonitorApp, "__init__", lambda self: None):
            app = PcMonitorApp()
            return app

    @patch("modules.gui.send_data")
    @patch("modules.gui.read_response")
    def test_send_and_validate_ack(self, mock_read, mock_send):
        """Caminho Feliz: Envia e recebe ACK."""
        mock_read.return_value = {"status": "ACK", "msg": "CPU data updated"}
        app = self._make_app()

        result = app._send_and_validate({"target": "CPU"})

        assert result is True

    @patch("modules.gui.send_data")
    @patch("modules.gui.read_response")
    def test_send_and_validate_nack(self, mock_read, mock_send):
        """Falha: Recebe NACK."""
        mock_read.return_value = {"status": "NACK", "msg": "JSON parse error"}
        app = self._make_app()

        result = app._send_and_validate({"target": "CPU"})

        assert result is False

    @patch("modules.gui.send_data", side_effect=Exception("Serial error"))
    def test_send_and_validate_exception_returns_false(self, mock_send):
        """Falha: Excecao no envio retorna False."""
        app = self._make_app()

        result = app._send_and_validate({"target": "CPU"})

        assert result is False

    @patch("modules.gui.send_data")
    @patch("modules.gui.read_response", return_value=None)
    def test_send_and_validate_no_response(self, mock_read, mock_send):
        """Falha: Sem resposta (timeout) retorna False."""
        app = self._make_app()

        result = app._send_and_validate({"target": "CPU"})

        assert result is False


class TestLogMethods:
    """Testes para os metodos de log."""

    def _make_app(self):
        """Cria uma instancia de PcMonitorApp com __init__ mockado."""
        from modules.gui import PcMonitorApp

        with patch.object(PcMonitorApp, "__init__", lambda self: None):
            app = PcMonitorApp()
            app._log_text = MagicMock()
            app.after = MagicMock(side_effect=lambda ms, fn, *args: fn(*args))
            return app

    def test_append_log_inserts_text(self):
        """Caminho Feliz: _append_log insere texto no textbox."""
        app = self._make_app()

        app._append_log("[12:00:00] Test message\n")

        app._log_text.insert.assert_called_with("end", "[12:00:00] Test message\n")
        app._log_text.see.assert_called_with("end")
        configure_calls = app._log_text.configure.call_args_list
        states = [c[1].get("state") for c in configure_calls if "state" in c[1]]
        assert "normal" in states and "disabled" in states

    def test_set_status_updates_label(self):
        """Caminho Feliz: _set_status atualiza o label de status."""
        app = self._make_app()
        app._status_label = MagicMock()

        app._set_status("Conectado", "#2ecc71")

        app._status_label.configure.assert_called_once_with(
            text="Conectado", text_color="#2ecc71"
        )
