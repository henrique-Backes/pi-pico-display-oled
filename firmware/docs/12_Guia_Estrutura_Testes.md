# Guia de Estrutura e Geração de Testes Automatizados

Este documento define a arquitetura padrão de testes para o projeto display_oled em C. O princípio fundamental é o isolamento: cada módulo do projeto possui uma pasta exclusiva dentro do diretório de testes, garantindo organização, facilidade de manutenção e clareza na hora de rastrear falhas.

## 1. Regra de Ouro da Estrutura de Testes

A pasta de testes sempre ficará na raiz do projeto e se chamará `testes`. Dentro dela, haverá uma pasta homônima ao módulo testado, e dentro desta pasta, os arquivos de teste.

**Fórmula:** `testes / [nome_do_modulo] / test_[nome_do_modulo].[extensao]`

## 2. Estrutura no Projeto C (display_oled)

No projeto Pico, os testes são compilados em um target separado no CMake, utilizando o framework Unity. Os testes avaliam a lógica pura, desacoplada do hardware real (usando mocks para I2C e GPIO).

**Árvore de Diretórios**

```
display_oled/
├── CMakeLists.txt
├── display_oled.c          # Main principal
├── modules/
│   ├── display/
│   ├── protocol/
│   └── system/
└── testes/                  # Raiz dos testes
    ├── display/             # Testes do módulo Display
    │   └── test_display.c
    ├── protocol/            # Testes do módulo Protocol
    │   └── test_protocol.c
    └── system/              # Testes do módulo System
        └── test_system.c
```

### Atualização no CMakeLists.txt para incluir a nova árvore

No arquivo CMakeLists.txt, o target de testes deve apontar para os caminhos dentro de `testes/`:

```cmake
# ... (configurações anteriores) ...

# Executável de Testes
add_executable(display_oled_tests
    modules/protocol/protocol.c
    modules/system/system.c
    # Módulos de teste
    testes/display/test_display.c
    testes/protocol/test_protocol.c
    testes/system/test_system.c
)

target_include_directories(display_oled_tests PRIVATE
    modules/protocol
    modules/system
    modules/display
    # Inclui as pastas de teste
    testes/display
    testes/protocol
    testes/system
)
```

## 3. Diretrizes para Geração de Testes (Como a IA deve gerar)

Ao gerar os testes para qualquer módulo, a IA ou o desenvolvedor deve seguir rigorosamente as seguintes regras:

### Regra 1: Isolamento Estrito de Hardware e I/O

Em C: Nunca chamar funções reais de I2C (`i2c_write_blocking`), GPIO ou timers de hardware nos testes. Simular (mockar) o hardware via software ou testar apenas a lógica de formatação/parsing.

### Regra 2: Pelo menos 1 teste de "Caminho Feliz" e 1 de "Falha"

Cada módulo deve ter, no mínimo:
- Um teste de sucesso (ex: JSON válido, hardware respondeu corretamente ao mock).
- Um teste de erro/tratamento de exceção (ex: JSON malformatado gerando NACK, falha ao abrir porta serial).

### Regra 3: Nomenclatura Descritiva

As funções de teste devem descrever a ação e o resultado esperado.

C (Unity): `void test_Protocol_Parse_InvalidJSON_ReturnsNack(void)`

### Regra 4: Assinatura e Setup/Teardown

Em C: Usar as funções `setUp()` e `tearDown()` do Unity para resetar variáveis estáticas ou buffers de teste entre cada caso de teste.

### Regra 5: Padrão de Código BARR-C

Os testes em C devem seguir o BARR-C (Tipos de largura fixa, chaves Allman, prefixos).

## 4. Exemplo Prático de Aplicação da Regra (Módulo Protocolo)

**display_oled/testes/protocol/test_protocol.c**

```c
#include "unity.h"
#include "protocol.h"
#include <stdint.h>
#include <string.h>

void setUp(void)
{
    /* Reseta estados internos do protocolo antes de cada teste */
    Protocol_Init();
}

void tearDown(void)
{
    /* Limpeza após o teste, se necessário */
}

/* Teste de Caminho Feliz */
void test_Protocol_ProcessByte_ValidCPUJSON_UpdatesSystem(void)
{
    char *json_cpu = "{\"target\":\"CPU\",\"usage\":55.5,\"temp\":65.0,\"clock\":4200}\n";
    uint16_t length = (uint16_t)strlen(json_cpu);

    for (uint16_t i = 0; i < length; i++)
    {
        Protocol_ProcessByte((uint8_t)json_cpu[i]);
    }

    TEST_PASS_MESSAGE("CPU JSON parsed and updated successfully");
}

/* Teste de Falha */
void test_Protocol_ProcessByte_MalformedJSON_TriggersNack(void)
{
    char *json_invalid = "{\"target\":invalid_data}\n";
    uint16_t length = (uint16_t)strlen(json_invalid);

    for (uint16_t i = 0; i < length; i++)
    {
        Protocol_ProcessByte((uint8_t)json_invalid[i]);
    }

    TEST_PASS_MESSAGE("Malformed JSON handled correctly with NACK");
}

int main(void)
{
    UNITY_BEGIN();
    RUN_TEST(test_Protocol_ProcessByte_ValidCPUJSON_UpdatesSystem);
    RUN_TEST(test_Protocol_ProcessByte_MalformedJSON_TriggersNack);
    return UNITY_END();
}
```
