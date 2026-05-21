# 07 — Guia Técnico do SSD1306

## 1. Visão Geral

O SSD1306 é um controlador CMOS de chip único para matrizes de pontos
OLED/PLED de 128×64. Integra driver de segmento e comum, oscilador RC
interno e gerenciamento de contraste, reduzindo o consumo de energia e
a necessidade de componentes externos.

---

## 2. Arquitetura Interna

### 2.1 Interface com MCU

O controlador suporta:

| Interface     | Descrição                                    |
|---------------|----------------------------------------------|
| I2C           | 2 fios (SDA, SCL) — modo usado neste projeto |
| SPI 3 fios    | SCLK, SDIN, CS#/DC                           |
| SPI 4 fios    | SCLK, SDIN, CS#, DC                          |
| 6800-paralelo | 8 bits, E, R/W#, D/C#, CS#                  |
| 8080-paralelo | 8 bits, RD#, WR#, D/C#, CS#                 |

No modo I2C, o byte de controle (Co + D/C#) define se o payload é
comando (`0x00`) ou dado (`0x40`).

### 2.2 GDDRAM (Graphic Display Data RAM)

- Tamanho total: 128 × 64 bits = 1024 bytes.
- Organizada em **8 páginas** (PAGE0–PAGE7).
- Cada página contém **128 colunas**.
- Cada coluna em uma página = **1 byte** (8 pixels verticais).

```
        Col 0  Col 1  Col 2  ...  Col 127
        +------+------+------+----+------+
PAGE 0  | D0-D7| D0-D7| D0-D7|... | D0-D7|   Linhas  0-7
        +------+------+------+----+------+
PAGE 1  | D0-D7| D0-D7| D0-D7|... | D0-D7|   Linhas  8-15
        +------+------+------+----+------+
  ...   |  ... |  ... |  ... |... |  ... |
        +------+------+------+----+------+
PAGE 7  | D0-D7| D0-D7| D0-D7|... | D0-D7|   Linhas 56-63
        +------+------+------+----+------+
```

### 2.3 Mapeamento de Bits

- **D0** (LSB) → pixel superior da página.
- **D7** (MSB) → pixel inferior da página.
- Quando um byte é escrito na GDDRAM, ele preenche uma **coluna inteira**
  (8 pixels verticais) da página atual.

### 2.4 Charge Pump

O OLED requer tensão mais alta do que a MCU fornece (3V3). O SSD1306
possui um circuito interno de **bomba de carga** (Charge Pump) que eleva
essa tensão. O comando `8Dh` com valor `14h` ativa a bomba de carga
interna — **isto é crítico** para o funcionamento do display.

---

## 3. Modos de Endereçamento

Definidos pelo comando `20h`:

| Valor | Modo       | Descrição                                                            |
|-------|------------|----------------------------------------------------------------------|
| 00h   | Horizontal | Após escrever, ponteiro avança coluna; ao fim da linha, salta para a próxima página. |
| 01h   | Vertical   | Ponteiro avança página (verticalmente); ao fim, salta para a próxima coluna. |
| 02h   | Page       | Padrão. Ponteiro avança coluna mas fica na mesma página até comando manual. |

**Este projeto usa o Modo Horizontal** (`20h`, `00h`), que permite
enviar todo o frame buffer (1024 bytes) de forma contínua, pois o
controlador percorre automaticamente todas as colunas de PAGE0 a PAGE7.

---

## 4. Fluxo de Inicialização Recomendado

Sequência obrigatória para ligar o display sem artefatos:

```
1.  Display OFF                         (AEh)
2.  Set Display Clock Divide Ratio      (D5h, 80h)
3.  Set Multiplex Ratio                 (A8h, 3Fh)  → 128×64 = 63
4.  Set Display Offset                  (D3h, 00h)
5.  Set Display Start Line              (40h)       → Linha 0
6.  Charge Pump Setting                 (8Dh, 14h)  → CRÍTICO: ativa
7.  Set Memory Addressing Mode          (20h, 00h)  → Horizontal
8.  Set Segment Re-map                  (A1h)       → Col 127 = SEG0
9.  Set COM Output Scan Direction       (C8h)       → Invertido
10. Set COM Pins Hardware Configuration (DAh, 12h)  → Alternative
11. Set Contrast Control                (81h, CFh)
12. Set Pre-charge Period               (D9h, F1h)
13. Set VCOMH Deselect Level            (DBh, 40h)
14. Entire Display ON (resume RAM)      (A4h)
15. Set Normal Display                  (A6h)
16. Display ON                          (AFh)
```

**Notas importantes:**

- O Display OFF no início garante que nada é exibido durante a
  configuração.
- O Charge Pump **deve** ser ativado antes de Display ON.
- A ordem é importante — particularmente, o Charge Pump antes do
  Display ON.

---

## 5. Comandos — Referência Completa

### 5.1 Comandos Fundamentais

| Comando       | Nome                | Descrição                                        |
|---------------|---------------------|--------------------------------------------------|
| 81h, 00-FFh   | Set Contrast        | Ajusta brilho (00h = mín, FFh = máx).           |
| A4h           | Resume RAM          | Exibe conteúdo da GDDRAM.                        |
| A5h           | Entire Display ON   | Força todos os pixels a ligar (ignora RAM).      |
| A6h           | Normal Display      | 1 = ligado, 0 = desligado.                       |
| A7h           | Inverse Display     | 1 = desligado, 0 = ligado.                       |
| AEh           | Display OFF         | Modo sleep (painel desligado).                   |
| AFh           | Display ON          | Liga o painel.                                   |

### 5.2 Configuração de Endereçamento

| Comando        | Nome              | Descrição                                              |
|----------------|-------------------|--------------------------------------------------------|
| 20h, 00h       | Horizontal Mode   | Ponteiro avança horizontal; salta página ao fim.      |
| 20h, 01h       | Vertical Mode     | Ponteiro avança verticalmente.                        |
| 20h, 02h       | Page Mode         | Padrão. Ponteiro fica na mesma página.                |
| 21h, S, E      | Column Address    | Coluna inicial (S) e final (E), modos Horiz/Vert.     |
| 22h, S, E      | Page Address      | Página inicial (S) e final (E), modos Horiz/Vert.     |
| B0h–B7h        | Page Start        | Página 0–7 (modo Page).                               |

### 5.3 Configuração de Hardware

| Comando        | Nome              | Descrição                                              |
|----------------|-------------------|--------------------------------------------------------|
| 40h–7Fh        | Start Line        | Linha física no topo (0–63).                          |
| A0h / A1h      | Segment Remap     | A0: col 0 = SEG0; A1: col 127 = SEG0.                |
| C0h / C8h      | COM Scan Dir      | C0: normal; C8: invertido (baixo→cima).              |
| A8h, 00-3Fh    | Multiplex Ratio   | Número de linhas varridas (63 para 128×64).           |
| D3h, 00-3Fh    | Display Offset    | Deslocamento vertical.                                |
| DAh, 02h/12h   | COM Pins Conf     | Sequential (02h) ou Alternative (12h).               |

### 5.4 Timing e Potência

| Comando        | Nome              | Descrição                                              |
|----------------|-------------------|--------------------------------------------------------|
| D5h, 80h       | Clock Divide      | Frequência do oscilador e divisor de clock.           |
| D9h, 00-FFh    | Pre-charge        | Duração das fases de pré-carga.                       |
| DBh, 00-FFh    | VCOMH Level       | Nível de tensão de deseleção.                         |
| 8Dh, 14h/10h   | Charge Pump       | 14h = ativa; 10h = desativa.                          |

### 5.5 Scrolling

| Comando        | Nome              | Descrição                                              |
|----------------|-------------------|--------------------------------------------------------|
| 26h / 27h      | Horizontal Scroll | Configura rolagem horizontal (direita/esquerda).      |
| 2Fh            | Activate Scroll   | Inicia rolagem configurada.                           |
| 2Eh            | Deactivate Scroll | Para rolagem.                                         |

---

## 6. Protocolo I2C — Detalhes

### 6.1 Endereço I2C

O endereço padrão do SSD1306 é `0x3C` (7-bit), que corresponde a:

- Escrita: `0x78` (0x3C << 1)
- Leitura: `0x79` (0x3C << 1 | 1)

> **Nota:** Alguns módulos usam `0x3D` dependendo do pino SA0.

### 6.2 Byte de Controle

Após o endereço, o primeiro byte enviado é o **byte de controle**:

```
+-----+-----+-----+-----+-----+-----+-----+-----+
| Co  | D/C |  0  |  0  |  0  |  0  |  0  |  0  |
+-----+-----+-----+-----+-----+-----+-----+-----+
  bit7  bit6
```

- **Co = 0, D/C = 0** → bytes seguintes são comandos (`0x00`).
- **Co = 0, D/C = 1** → bytes seguintes são dados (`0x40`).
- **Co = 1** → apenas UM byte de comando/dado segue; após ele, volta ao
  estado de espera de byte de controle.

> **Atenção:** Usar `Co = 1` (0x80 ou 0xC0) permite enviar apenas UM
> byte por transação. Para múltiplos bytes, sempre use `Co = 0`.

### 6.3 Transações I2C

**Envio de comando:**
```
[START] [ADDR+W] [0x00] [CMD] [STOP]
```

**Envio de múltiplos dados (frame buffer):**
```
[START] [ADDR+W] [0x40] [D0] [D1] [D2] ... [D1023] [STOP]
```

> O Pico SDK (`i2c_write_blocking`) tem limite prático para transações
> I2C. Para 1024 bytes de dados (+ 1 byte controle = 1025), pode ser
> necessário fragmentar em blocos menores (ex: 16 bytes de dados por
> transação) para garantir transferência confiável.

---

## 7. Frame Buffer — Layout

O frame buffer no MCU espelha a GDDRAM:

```
Índice linear:    byte 0     = PAGE0, COL0
                  byte 1     = PAGE0, COL1
                  ...
                  byte 127   = PAGE0, COL127
                  byte 128   = PAGE1, COL0
                  ...
                  byte 1023  = PAGE7, COL127
```

Fórmula para acesso direto:
```
index = (page * 128) + column
```

Para renderizar um caractere 5×7 na posição (x, page_y):
- Cada coluna do caractere é escrita como 1 byte inteiro no frame buffer.
- O byte da fonte já contém os 8 bits verticais corretamente mapeados
  (D0 = topo, D7 = base).
- **Não** é necessário processar bit a bit — basta copiar o byte da
  fonte diretamente para a posição do frame buffer.

---

## 8. Lições Aprendidas (Erros Comuns)

### 8.1 — Chuvisco / Pixels Aleatórios

**Causa:** Frame buffer não é enviado completamente ao display.
O SSD1306 exibe o conteúdo residual da GDDRAM não inicializada.

**Solução:**
- Garantir que **todos** os 1024 bytes do frame buffer sejam enviados.
- Fragmentar envio I2C em blocos menores (ex: 16 bytes por transação).
- Sempre chamar `display_clear()` ao final da inicialização.

### 8.2 — Caracteres Corrompidos

**Causa:** Escrita bit a bit no frame buffer em vez de byte a byte.
Os bits de uma mesma coluna se sobrepõem incorretamente.

**Solução:**
- Escrever o byte inteiro da fonte diretamente na posição do frame
  buffer: `g_frame_buf[offset + col] = font_byte;`

### 8.3 — Display Não Liga

**Causa:** Charge Pump não ativado, ou Display ON enviado antes do
Charge Pump.

**Solução:**
- Sempre enviar `8Dh, 14h` **antes** de `AFh` (Display ON).

### 8.4 — I2C Timeout

**Causa:** Tentativa de enviar mais bytes do que o controlador I2C do
RP2040 suporta em uma única transação.

**Solução:**
- Fragmentar dados em blocos de até 32 bytes por transação I2C.
