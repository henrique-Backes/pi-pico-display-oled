# Testes — Projetos Embarcados (Unity)

## 1. Estrutura

- Pasta: `testes/` (nunca `tests/`).
- Layout: `testes/<modulo>/test_<modulo>.c`.

```
projeto/
├── CMakeLists.txt
├── main.c
├── modules/
│   ├── display/
│   ├── protocol/
│   └── system/
└── testes/
    ├── display/
    │   └── test_display.c
    ├── protocol/
    │   └── test_protocol.c
    └── system/
        └── test_system.c
```

## 2. Framework

- **Unity** (ThrowTheSwitch).
- Compilados como target separado no CMake.
- Mockar hardware (I2C, GPIO, sleep) via stubs.

## 3. Diretrizes

- **Isolamento estrito:** nunca chamar funções reais de hardware.
- Mínimo: 1 teste caminho feliz + 1 teste falha por módulo.
- `setUp()` / `tearDown()` para resetar estados entre testes.
- Nomenclatura: `void test_Modulo_Funcao_Cenario_Resultado(void)`.
- Testes seguem BARR-C.

## 4. Exemplo

```c
#include "unity.h"
#include "protocol.h"
#include <stdint.h>
#include <string.h>

void setUp(void)
{
    /* Reseta estados internos antes de cada teste */
    Protocol_Init();
}

void tearDown(void)
{
    /* Limpeza após o teste, se necessário */
}

/* Caminho Feliz */
void test_Protocol_Parse_ValidCPUJSON_UpdatesSystem(void)
{
    char const *json_cpu = "{\"target\":\"CPU\",\"usage\":55.5,\"temp\":65.0}\n";
    uint16_t length = (uint16_t)strlen(json_cpu);

    for (uint16_t i = 0u; i < length; ++i)
    {
        Protocol_ProcessByte((uint8_t)json_cpu[i]);
    }

    TEST_PASS_MESSAGE("CPU JSON parsed and updated successfully");
}

/* Falha */
void test_Protocol_Parse_MalformedJSON_ReturnsNack(void)
{
    char const *json_invalid = "{\"target\":invalid}\n";
    uint16_t length = (uint16_t)strlen(json_invalid);

    for (uint16_t i = 0u; i < length; ++i)
    {
        Protocol_ProcessByte((uint8_t)json_invalid[i]);
    }

    TEST_PASS_MESSAGE("Malformed JSON handled correctly with NACK");
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_Protocol_Parse_ValidCPUJSON_UpdatesSystem);
    RUN_TEST(test_Protocol_Parse_MalformedJSON_ReturnsNack);
    return UNITY_END();
}
```

## 5. CMake

```cmake
add_executable(projeto_tests
    modules/protocol/protocol.c
    modules/system/system.c
    testes/display/test_display.c
    testes/protocol/test_protocol.c
    testes/system/test_system.c
)

target_include_directories(projeto_tests PRIVATE
    modules/protocol
    modules/system
    modules/display
    testes/display
    testes/protocol
    testes/system
)
```
