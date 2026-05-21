import threading
import time

import customtkinter as ctk

from modules.hardware_info import detect_hardware
from modules.hardware_info import get_cpu_info, get_gpu_info, shutdown as hw_shutdown
from modules.serial_comm import connect, disconnect, list_available_ports
from modules.serial_comm import send_data, read_response

CYCLE_INTERVAL = 3.0


class PcMonitorApp(ctk.CTk):
    """Aplicacao GUI principal do PC Monitor com estilo Win11."""

    def __init__(self):
        super().__init__()

        self.title("PC Monitor - Pico Display")
        self.geometry("520x600")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._monitoring = False
        self._monitor_thread = None

        self._build_ui()
        self._refresh_ports()
        self._detect_and_show_hardware()

    def _build_ui(self) -> None:
        """Constroi toda a interface grafica."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_controls()
        self._build_log_terminal()
        self._build_status_bar()

    def _build_header(self) -> None:
        """Cabecalho com titulo."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")

        title = ctk.CTkLabel(
            header,
            text="PC Monitor",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.pack(side="left")

        self._hw_info_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        self._hw_info_label.pack(side="left", padx=(10, 0), pady=(8, 0))

    def _detect_and_show_hardware(self) -> None:
        """Detecta fabricantes de CPU/GPU e exibe no cabecalho e log."""
        hw = detect_hardware()
        cpu_v = hw["cpu_vendor"]
        gpu_v = hw["gpu_vendor"]
        cpu_libs = ", ".join(hw["cpu_libs"])
        gpu_libs = ", ".join(hw["gpu_libs"])

        self._hw_info_label.configure(text=f"CPU: {cpu_v} | GPU: {gpu_v}")
        self._log(f"Hardware detectado -> CPU: {cpu_v} (libs: {cpu_libs})")
        self._log(f"Hardware detectado -> GPU: {gpu_v} (libs: {gpu_libs})")

    def _build_controls(self) -> None:
        """Painel de controles: selecao de porta, baudrate, botoes."""
        controls = ctk.CTkFrame(self)
        controls.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        controls.grid_columnconfigure(1, weight=1)

        port_label = ctk.CTkLabel(controls, text="Porta COM:", font=ctk.CTkFont(size=13))
        port_label.grid(row=0, column=0, padx=(15, 5), pady=15, sticky="w")

        self._port_combo = ctk.CTkComboBox(
            controls,
            values=[""],
            width=160,
            font=ctk.CTkFont(size=13),
        )
        self._port_combo.grid(row=0, column=1, padx=5, pady=15, sticky="w")

        self._refresh_btn = ctk.CTkButton(
            controls,
            text="Atualizar",
            width=80,
            command=self._refresh_ports,
            font=ctk.CTkFont(size=12),
        )
        self._refresh_btn.grid(row=0, column=2, padx=5, pady=15)

        baud_label = ctk.CTkLabel(controls, text="Baud:", font=ctk.CTkFont(size=13))
        baud_label.grid(row=0, column=3, padx=(15, 5), pady=15, sticky="w")

        self._baud_entry = ctk.CTkEntry(controls, width=80, font=ctk.CTkFont(size=13))
        self._baud_entry.grid(row=0, column=4, padx=5, pady=15, sticky="w")
        self._baud_entry.insert(0, "115200")

        self._start_btn = ctk.CTkButton(
            controls,
            text="Iniciar",
            width=100,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self._start_monitoring,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self._start_btn.grid(row=1, column=0, padx=(15, 5), pady=(0, 15), sticky="w")

        self._stop_btn = ctk.CTkButton(
            controls,
            text="Parar",
            width=100,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self._stop_monitoring,
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self._stop_btn.grid(row=1, column=1, padx=5, pady=(0, 15), sticky="w")

    def _build_log_terminal(self) -> None:
        """Terminal de log das medidas atuais."""
        terminal_frame = ctk.CTkFrame(self)
        terminal_frame.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        terminal_frame.grid_columnconfigure(0, weight=1)
        terminal_frame.grid_rowconfigure(1, weight=1)

        term_label = ctk.CTkLabel(
            terminal_frame,
            text="Terminal de Log",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        term_label.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")

        self._log_text = ctk.CTkTextbox(
            terminal_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            state="disabled",
            wrap="word",
        )
        self._log_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")

    def _build_status_bar(self) -> None:
        """Barra de status na parte inferior."""
        status_frame = ctk.CTkFrame(self, height=32, fg_color="#1a1a2e")
        status_frame.grid(row=3, column=0, padx=0, pady=0, sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)

        self._status_label = ctk.CTkLabel(
            status_frame,
            text="Desconectado",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        )
        self._status_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")

    def _refresh_ports(self) -> None:
        """Atualiza a lista de portas COM disponiveis."""
        ports = list_available_ports()
        if not ports:
            ports = [""]
        self._port_combo.configure(values=ports)
        self._port_combo.set(ports[0])
        self._log(f"Portas encontradas: {', '.join(ports) if ports[0] else 'Nenhuma'}")

    def _log(self, message: str) -> None:
        """Adiciona mensagem ao terminal de log de forma thread-safe.

        Args:
            message: Texto a ser adicionado ao log.
        """
        timestamp = time.strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        self.after(0, self._append_log, line)

    def _append_log(self, line: str) -> None:
        """Insere texto no textbox (deve rodar na main thread).

        Args:
            line: Linha formatada com timestamp.
        """
        self._log_text.configure(state="normal")
        self._log_text.insert("end", line)
        self._log_text.see("end")
        self._log_text.configure(state="disabled")

    def _set_status(self, text: str, color: str = "gray") -> None:
        """Atualiza a barra de status.

        Args:
            text: Texto do status.
            color: Cor do texto.
        """
        self._status_label.configure(text=text, text_color=color)

    def _start_monitoring(self) -> None:
        """Inicia o monitoramento em uma thread separada."""
        port = self._port_combo.get()
        if not port:
            self._log("Erro: Nenhuma porta selecionada!")
            return

        baudrate = 115200
        try:
            baudrate = int(self._baud_entry.get())
        except ValueError:
            self._log("Erro: Baudrate invalido, usando 115200")

        try:
            connect(port=port, baudrate=baudrate)
        except Exception as e:
            self._log(f"Erro ao conectar: {e}")
            return

        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop, daemon=True
        )
        self._monitor_thread.start()

        self._start_btn.configure(state="disabled")
        self._stop_btn.configure(state="normal")
        self._port_combo.configure(state="disabled")
        self._refresh_btn.configure(state="disabled")
        self._baud_entry.configure(state="disabled")
        self._set_status(f"Monitorando - {port} @ {baudrate}", "#2ecc71")
        self._log(f"Conectado em {port} @ {baudrate}")

    def _stop_monitoring(self) -> None:
        """Para o monitoramento e desconecta a serial."""
        self._monitoring = False
        disconnect()

        self._start_btn.configure(state="normal")
        self._stop_btn.configure(state="disabled")
        self._port_combo.configure(state="normal")
        self._refresh_btn.configure(state="normal")
        self._baud_entry.configure(state="normal")
        self._set_status("Desconectado", "gray")
        self._log("Monitoramento parado.")

    def _monitor_loop(self) -> None:
        """Loop de monitoramento que roda em thread separada."""
        while self._monitoring:
            try:
                cpu_data = get_cpu_info()
                if self._send_and_validate(cpu_data):
                    self._log(
                        f"CPU: {cpu_data['usage']:5.1f}% | "
                        f"{cpu_data['temp']:5.1f}C | "
                        f"{cpu_data['clock']} MHz  [ACK]"
                    )
                else:
                    self._log("CPU: Falha no envio [NACK]")

                time.sleep(CYCLE_INTERVAL)
                if not self._monitoring:
                    break

                gpu_data = get_gpu_info()
                if self._send_and_validate(gpu_data):
                    self._log(
                        f"GPU: {gpu_data['usage']:5.1f}% | "
                        f"{gpu_data['temp']:5.1f}C | "
                        f"{gpu_data['vram_used']:.1f}/{gpu_data['vram_total']:.1f} GB  [ACK]"
                    )
                else:
                    self._log("GPU: Falha no envio [NACK]")

                time.sleep(CYCLE_INTERVAL)

            except Exception as e:
                self._log(f"Erro: {e}")
                self.after(0, self._stop_monitoring)
                break

    def _send_and_validate(self, data: dict) -> bool:
        """Envia dados e verifica resposta ACK/NACK.

        Args:
            data: Dicionario com dados de hardware.

        Returns:
            bool: True se ACK, False caso contrario.
        """
        try:
            send_data(data)
            response = read_response()
            return response is not None and response.get("status") == "ACK"
        except Exception:
            return False

    def destroy(self) -> None:
        """Encerra a aplicacao, parando monitoramento se ativo."""
        self._monitoring = False
        disconnect()
        hw_shutdown()
        super().destroy()
