# Comentários e Documentação — Projetos Embarcados

## 1. Formato

- **Interface (.h):** Doxygen obrigatório acima de todas as funções públicas.
- **Implementação (.c):** Doxygen apenas para funções `static`.
- Comentários internos focam em regras de negócio, não no óbvio.

## 2. Estilo

- Documentação e comentários em **Português (Brazilian)**.
- Identificadores de código em **English**.
- Frases claras, completas, gramática correta.
- Evitar explicar o óbvio.
- Número/comprimento proporcional à complexidade.
- Marcadores: `WARNING:`, `NOTE:`, `TODO:`.

```c
/* Step 1: Fechar as escotilhas. */
for (int hatch = 0; hatch < NUM_HATCHES; ++hatch)
{
    if (hatch_is_open(hatches[hatch]))
    {
        hatch_close(hatches[hatch]);
    }
}

/* Step 2: Levantar o mastro principal. */
/* TODO: Definir a API do driver do mastro principal. */
```

## 3. Código Desativado

- Usar `#if 0 ... #endif` — nunca comentar código com `/* */` ou `//`.

## 4. Debug/Depuração

- Cercar por `#ifndef NDEBUG ... #endif`.

## 5. Casts

- Todo cast deve ter comentário explicando por que é seguro.

```c
result = abs((int) sample); /* AVISO: Assume-se que int tenha 32 bits. */
```

## 6. Doxygen — Header (.h)

```c
/** @file module.h
 *
 * @brief Descrição do propósito do módulo.
 *
 * @par
 * COPYRIGHT NOTICE: (c) 2026. All rights reserved.
 */

#ifndef MODULE_H
#define MODULE_H

/**
 * @brief Descrição da função pública.
 *
 * @param[in] num1 Primeiro número.
 * @param[in] num2 Segundo número.
 *
 * @return O maior valor.
 */
int8_t max8(int8_t num1, int8_t num2);

#endif /* MODULE_H */

/*** end of file ***/
```

## 7. Doxygen — Source (.c)

```c
/** @file module.c
 *
 * @brief Descrição do propósito do módulo.
 *
 * @par
 * COPYRIGHT NOTICE: (c) 2026. All rights reserved.
 */

#include <stdint.h>
#include <stdbool.h>
#include "module.h"

/*!
 * @brief Identifica o maior de dois inteiros de 8 bits.
 *
 * @param[in] num1 Primeiro número.
 * @param[in] num2 Segundo número.
 *
 * @return O maior valor.
 */
int8_t
max8(int8_t num1, int8_t num2)
{
    return ((num1 > num2) ? num1 : num2);
}

/*** end of file ***/
```
