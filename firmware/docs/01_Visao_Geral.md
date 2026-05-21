# Projeto: PC Monitor via Raspberry Pi Pico

## 1. Objetivo

Criar um sistema onde um Raspberry Pi Pico atua como um display secundário para o PC, exibindo alternadamente informações de GPU e CPU em um display OLED. A comunicação é feita via USB Serial (CDC) utilizando JSON.

## 2. Fluxo de Dados

- O PC (Python) coleta dados de hardware a cada ciclo.
- O PC formata os dados em JSON e envia via USB Serial para o Pico.
- O Pico (C) recebe o pacote, parseia o JSON e envia um retorno (ACK/NACK).
- O Pico armazena os dados e alterna a exibição no OLED a cada 3 segundos (CPU -> GPU -> CPU).

## 3. Hardware Utilizado

- **Microcontrolador:** Raspberry Pi Pico
- **Display:** OLED SSD1306 (128x64)
- **Interface:** I2C0 (SDA: GPIO 16 | SCL: GPIO 17)

## 4. Documentação Modular

Para entender as regras de formatação, arquitetura e desenvolvimento, consulte os documentos específicos:

- **02_Protocolo_JSON.md** - Estrutura dos pacotes trocados.
- **03_Pico_C_Guia_Geral.md** a **06_Pico_Modulo_Sistema.md** - Guia completo do firmware.
