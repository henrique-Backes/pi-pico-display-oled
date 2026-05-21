# Guia Geral do Projeto Pico (C / Pico SDK)

## 1. Formatação e Padrões (BARR-C)

- **Chaves:** Estilo Allman (abre na linha de baixo).
- **Tipos:** Usar tipos de largura fixa (`uint8_t`, `uint32_t`, `float`) em vez de `int`, `char`, etc.
- **Nomenclatura:** `Módulo_Prefixo_Ação` (Ex: `Display_Init()`, `Protocol_Parse()`).
- **Variáveis:** Descritivas, sem abreviações obscuras.
- **Comentários:** `/* Bloco */` e `// Linha`.

## 2. Arquitetura de Pastas

O projeto segue o padrão do Pico SDK, com o arquivo principal na raiz e módulos em pastas isoladas contendo seus `.c` e `.h`.

```
pico_pc_monitor/
├── CMakeLists.txt          # Configuração do CMake
├── pico_pc_monitor.c       # Arquivo principal (main) na raiz
├── pico_sdk_import.cmake   # Script do SDK (padrão)
├── build/                  # Pasta de build e binários compilados
└── modules/
    ├── display/
    │   ├── display.c
    │   └── display.h
    ├── protocol/
    │   ├── protocol.c
    │   └── protocol.h
    └── system/
        ├── system.c
        └── system.h
```

## 3. Configuração do CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)

project(pico_pc_monitor C CXX ASM)
set(CMAKE_C_STANDARD 11)

pico_sdk_init()

# Inclusão do cJSON (assumindo pasta libs/cJSON)
add_library(cJSON STATIC libs/cJSON/cJSON.c)
target_include_directories(cJSON PUBLIC libs/cJSON/)

# Arquivo principal
add_executable(pico_pc_monitor pico_pc_monitor.c)

# Módulos
target_sources(pico_pc_monitor PRIVATE
    modules/display/display.c
    modules/protocol/protocol.c
    modules/system/system.c
)

target_include_directories(pico_pc_monitor PRIVATE
    modules/display
    modules/protocol
    modules/system
)

# Dependências
target_link_libraries(pico_pc_monitor pico_stdlib hardware_i2c cJSON)

# USB CDC e saídas
pico_enable_stdio_usb(pico_pc_monitor 1)
pico_enable_stdio_uart(pico_pc_monitor 0)
pico_add_extra_outputs(pico_pc_monitor)
```
