# Módulo: Display

## 1. Responsabilidade

Controlar o hardware I2C e renderizar os dados no display OLED SSD1306. Isolar completamente a lógica de desenho do restante do sistema.

## 2. Configuração de Hardware

- **I2C:** I2C0
- **SDA:** GPIO 16
- **SCL:** GPIO 17
- **Clock:** 400 kHz (Fast Mode)

## 3. Interface (display.h)

```c
#ifndef DISPLAY_H
#define DISPLAY_H

#include <stdint.h>

void Display_Init(void);
void Display_Clear(void);
void Display_ShowCPU(float usage, float temp, uint32_t clock);
void Display_ShowGPU(float usage, float temp, float vram_used, float vram_total);

#endif /* DISPLAY_H */
```

## 4. Guia de Desenvolvimento

- **`Display_Init()`**: Deve configurar o `hardware_i2c`, mapear os GPIOs 16 e 17 via `gpio_set_function()`, e enviar a sequência de inicialização do SSD1306.
- **`Display_ShowCPU/GPU()`**: Devem formatar os números em strings usando `snprintf`, posicionar o cursor e enviar os bytes via I2C para o buffer do display.
