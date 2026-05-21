# Módulo: Sistema e Main

## 1. Responsabilidade

Controlar o tempo de alternância de tela (3 segundos), armazenar os dados recebidos e orquestrar as chamadas entre Protocol e Display.

## 2. Interface (system.h)

```c
#ifndef SYSTEM_H
#define SYSTEM_H

#include <stdint.h>

void System_SetCPUData(float usage, float temp, uint32_t clock);
void System_SetGPUData(float usage, float temp, float vram_used, float vram_total);
void System_Run(void);

#endif /* SYSTEM_H */
```

## 3. Guia de Desenvolvimento

- **pico_pc_monitor.c (Main):** Chamar `stdio_init_all()`, inicializar os módulos (`Display_Init()`, `Protocol_Init()`). O loop principal deve ler `getchar_timeout_us()` ou `stdio_getchar()` e passar o byte para `Protocol_ProcessByte()`, além de chamar `System_Run()`.
- **System_Run():** Usar `get_absolute_time()` e `to_ms_since_boot()` para calcular o tempo. Se passaram-se 3 segundos, inverte uma flag estática (`screen_state`). Se `screen_state` for 0, chama `Display_ShowCPU()`, se for 1, chama `Display_ShowGPU()`.
- **Dados Estáticos:** Os dados de CPU e GPU devem ficar em variáveis `static` dentro do `system.c`, atualizados apenas por `System_SetCPUData()` e `System_SetGPUData()`.
