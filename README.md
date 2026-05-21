# Pi Pico Display OLED - PC Monitor

Monitor de hardware para PC usando Raspberry Pi Pico com display OLED SSD1306 (I2C).

## Visao Geral

O firmware recebe estatisticas de CPU/GPU do PC via USB Serial (CDC) como JSON, parse com cJSON, e alterna entre telas de CPU e GPU no display OLED a cada 3 segundos.

A interface Python (`interface_display/`) coleta dados de hardware e envia para o Pico.

## Estrutura do Repositorio

```
├── firmware/                 # Firmware Pi Pico (Pico SDK)
│   ├── display_oled.c        # Entry point
│   ├── modules/              # display, protocol, system
│   ├── libs/cJSON/           # JSON parser
│   └── testes/               # Unity tests
├── interface_display/        # Python GUI (CustomTkinter)
│   ├── main.pyw
│   ├── modules/              # gui, hardware_info, serial_comm
│   ├── libs/                 # LHM .NET DLLs
│   └── requirements.txt
└── README.md
```

## Diagrama

```
[PC] -- Python GUI (interface_display/) --> [USB CDC] --> [Pi Pico] --> [OLED SSD1306]
         (LHM / WMI / psutil)              JSON + \n      firmware
```

## Hardware

- Raspberry Pi Pico (RP2040)
- Display OLED SSD1306 128x64 (I2C)

### Conexoes I2C

| Sinal | GPIO |
|-------|------|
| SDA   | GP16 |
| SCL   | GP17 |

- I2C0, 400kHz, endereco 0x3C

## Firmware

### Modulos

| Modulo | Descricao |
|--------|-----------|
| `display_oled.c` | Entry point, main loop |
| `modules/display/` | Driver SSD1306 I2C (frame buffer, fonts 7x10 + 5x7) |
| `modules/protocol/` | JSON parser over USB CDC (cJSON, byte-by-byte, `\n` delimiter) |
| `modules/system/` | Screen toggle timer + data store |
| `libs/cJSON/` | Vendored JSON parser |

### Protocolo JSON

**Recebido (PC -> Pico):**

```json
{"target":"CPU","usage":45.5,"temp":62.0,"clock":3600}
{"target":"GPU","usage":80.0,"temp":71.0,"vram_used":6.2,"vram_total":8.0}
```

**Enviado (Pico -> PC):**

```json
{"status":"ACK","msg":"..."}
{"status":"NACK","msg":"..."}
```

### Build

Requer Pico SDK 2.2.0 + ARM toolchain 14_2_Rel1.

```bash
cmake -G Ninja -B build
ninja -C build
```

Output: `build/display_oled.elf`, `.uf2`, `.hex`

### Flash

```bash
picotool load build/display_oled.uf2 -fx
```

## Interface Python

A GUI em CustomTkinter coleta dados de hardware e envia para o Pico via serial.

### Coleta de Hardware

- **CPU:** LibreHardwareMonitor (.NET) -> WMI -> psutil
- **GPU NVIDIA:** LHM -> pynvml
- **GPU AMD:** LHM -> pyadl
- **GPU Intel:** LHM only

### Instalacao

```bash
cd interface_display/
pip install -r requirements.txt
```

### Uso

```bash
python main.pyw
```

### Dependencias

- `pyserial>=3.5`
- `psutil>=5.9.0`
- `customtkinter>=5.2.0`
- `pytest>=7.0.0` (para testes)

> **Nota:** Runtime Windows-only (requer LHM .NET DLLs). Testes rodam em qualquer OS com mocks.

## Testes

Framework: Unity (C firmware) + pytest (Python).

```bash
# Firmware (testes em testes/)
# Veja docs/12_Guia_Estrutura_Testes.md

# Python
cd interface_display/
pytest
```

## Padrao de Codigo

Barr-C:2018 completo. Veja `docs/barr_c.md` e `docs/00_Regras_Codificacao.md`.

- Allman braces, Yoda conditions
- Fixed-width types (`uint8_t`, `uint32_t`)
- Suffixes `u`/`f` em literais
- Prefixos `g_`, `p_`, `b_`
- Doxygen em funcoes publicas
- `for (;;)` loops, 80-char line width

## Documentacao Adicional

| Arquivo | Descricao |
|---------|-----------|
| `docs/02_Protocolo_JSON.md` | Especificacao do protocolo JSON |
| `docs/barr_c.md` | Regras de codificacao Barr-C |
| `docs/12_Guia_Estrutura_Testes.md` | Guia de testes com Unity |
