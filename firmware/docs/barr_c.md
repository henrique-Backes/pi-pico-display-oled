/** @file barr_c.md
 *
 * @brief Padrão de Codificação C para Sistemas Embarcados (BARR-C:2018).
 *
 * @par
 Documentação de referência completa do padrão BARR-C:2018 aplicado ao projeto. */

# Padrão de Codificação C para Sistemas Embarcados (BARR-C:2018)

## 1. Regras Gerais

### 1.1 Qual C?

- a. Todos os programas devem ser escritos em conformidade com a versão C99 do Padrão ISO da Linguagem de Programação C.
- b. Sempre que um compilador C++ for usado, as opções apropriadas devem ser definidas para restringir a linguagem à versão selecionada do ISO C.
- c. O uso de extensões proprietárias de palavras-chave, `#pragma` e assembly inline deve ser mantido no mínimo necessário e localizado em um pequeno número de módulos de driver de dispositivo.
- d. A diretiva `#define` não deve ser usada para alterar ou renomear nenhuma palavra-chave ou outro aspecto da linguagem de programação.

```c
#define begin {   // Não faça algo assim...
#define end   }   // ... nem assim.

// ... for (int row = 0; row < MAX_ROWS; row++) begin
// ... end

// Deixe o C ser C, não uma linguagem que você amou no passado.
```

### 1.2 Largura das Linhas

- a. A largura de todas as linhas em um programa deve ser limitada a um máximo de 80 caracteres.

### 1.3 Chaves

- a. As chaves devem sempre envolver os blocos de código após `if`, `else`, `switch`, `while`, `do` e `for`; instruções únicas e vazias também devem sempre estar entre chaves.
- b. Cada chave de abertura (`{`) deve aparecer sozinha na linha abaixo do início do bloco. A chave de fechamento correspondente (`}`) deve aparecer sozinha na mesma posição de alinhamento após o fim do bloco.

```c
{
    if (depth_in_ft > 10)
    {
        dive_stage = DIVE_DEEP;
    }
    else if (depth_in_ft > 0)
    {
        dive_stage = DIVE_SHALLOW;
    }
    else
    {
        dive_stage = DIVE_SURFACE;
    }
}
```

### 1.4 Parênteses

- a. Não confie nas regras de precedência de operadores do C. Use parênteses para garantir a ordem correta de execução.
- b. Cada operando dos operadores lógicos AND (`&&`) e OR (`||`) deve estar entre parênteses.

```c
if ((depth_in_cm > 0) && (depth_in_cm < MAX_DEPTH))
{
    depth_in_ft = convert_depth_to_ft(depth_in_cm);
}
```

### 1.5 Abreviações Comuns

- a. Abreviações e siglas geralmente devem ser evitadas, a menos que seus significados sejam ampla e consistentemente compreendidos.
- b. Uma tabela de abreviações e siglas específicas do projeto deve ser mantida.

### 1.6 Casts (Conversões de Tipo)

- a. Cada conversão de tipo (cast) deve apresentar um comentário associado descrevendo como o código garante o comportamento adequado em toda a gama de valores possíveis.

```c
uint16_t sample = adc_read(ADC_CHANNEL_1);
result = abs((int) sample); // AVISO: Assume-se que o int tenha 32 bits.
```

### 1.7 Palavras-chave a Evitar

- a. A palavra-chave `auto` não deve ser usada.
- b. A palavra-chave `register` não deve ser usada.
- c. É preferível evitar todo uso de `goto`. Se usado, só deve pular para um rótulo declarado mais adiante no mesmo bloco.
- d. É preferível evitar todo uso de `continue`.

### 1.8 Palavras-chave a Frequentar

- a. A palavra-chave `static` deve ser usada para declarar todas as funções e variáveis que não precisam ser visíveis fora do módulo.
- b. A palavra-chave `const` deve ser usada sempre que apropriado:
  - i. Variáveis que não devem mudar após inicialização;
  - ii. Parâmetros passados por referência que não devem ser modificados;
  - iii. Campos em struct ou union que não devem ser modificados;
  - iv. Como alternativa fortemente tipada ao `#define` para constantes.
- c. A palavra-chave `volatile` deve ser usada sempre que apropriado:
  - i. Variável global acessível por ISRs;
  - ii. Variável global acessível por múltiplas threads;
  - iii. Ponteiro para registradores de I/O mapeados em memória;
  - iv. Contador de loop de atraso.

```c
typedef struct
{
    uint16_t count;
    uint16_t max_count;
    uint16_t const _unused;  // registrador somente leitura
    uint16_t control;
} timer_reg_t;

timer_reg_t volatile * const p_timer =
    (timer_reg_t *) HW_TIMER_ADDR;
```

## 2. Regras de Comentários

### 2.1 Formatos Aceitáveis

- a. Comentários de linha única no estilo C++ (`//`) são preferíveis.
- b. Comentários nunca devem conter os tokens `/*`, `//`, ou `\`.
- c. Código nunca deve ser comentado. Use `#if 0 ... #endif` para desativar código temporariamente.
- d. Código de log/depuração deve ser cercado por `#ifndef NDEBUG ... #endif`.

### 2.2 Locais e Conteúdo

- a. Frases claras, completas, com ortografia e gramática corretas.
- b. Comentários mais úteis precedem um bloco de código. Uma linha em branco deve seguir o bloco.
- c. Evite explicar o óbvio.
- d. O número e comprimento dos comentários devem ser proporcionais à complexidade do código.
- e. Referências a documentos externos devem ser suficientes para localizar a fonte original.
- f. Suposições devem ser escritas nos comentários.
- g. Módulos e funções devem ser comentados para ferramentas como Doxygen.
- h. Use marcadores em letras maiúsculas: `WARNING:`, `NOTE:`, `TODO:`.

```c
// Step 1: Fechar as escotilhas.
for (int hatch = 0; hatch < NUM_HATCHES; hatch++)
{
    if (hatch_is_open(hatches[hatch]))
    {
        hatch_close(hatches[hatch]);
    }
}

// Step 2: Levantar o mastro principal.
// TODO: Definir a API do driver do mastro principal.
```

## 3. Regras de Espaço em Branco

### 3.1 Espaços

- a. Palavras-chave `if`, `while`, `for`, `switch` e `return` devem ser seguidas de 1 espaço.
- b. Operadores de atribuição (`=`, `+=`, etc.) devem ter 1 espaço antes e depois.
- c. Operadores binários (`+`, `-`, `<`, `&&`, etc.) devem ter 1 espaço antes e depois.
- d. Operadores unários (`+`, `-`, `++`, `--`, `!`, `~`) sem espaço no lado do operando.
- e. Operadores de ponteiro (`*` e `&`) com espaço em ambos os lados nas declarações, sem espaço no uso.
- f. Operador ternário (`?` e `:`) com 1 espaço antes e depois.
- g. Operadores de acesso a struct (`->` e `.`) sem espaços.
- h. Colchetes de array (`[` e `]`) sem espaços.
- i. Parênteses em expressões sem espaços internos adjacentes.
- j. Parênteses de chamada de função sem espaços, exceto na declaração onde deve haver 1 espaço entre o nome e o parêntese.
- k. Vírgulas entre parâmetros com 1 espaço após.
- l. Ponto e vírgula no `for` com 1 espaço após.
- m. Ponto e vírgula de fim de instrução sem espaço antes.

### 3.2 Alinhamento

- a. Nomes de variáveis em declarações em série devem alinhar o primeiro caractere.
- b. Nomes de membros de struct e union alinhados.
- c. Operadores de atribuição em blocos adjacentes alinhados.
- d. O `#` de diretivas do pré-processador deve estar sempre no início da linha.

```c
#ifdef USE_UNICODE_STRINGS
# define BUFFER_BYTES 128
#else
# define BUFFER_BYTES 64
#endif

typedef struct
{
    uint8_t buffer[BUFFER_BYTES];
    uint8_t checksum;
} string_t;
```

### 3.3 Linhas em Branco

- a. Nenhuma linha de código deve conter mais de uma instrução.
- b. Deve haver uma linha em branco antes e depois de cada bloco natural de código.
- c. Cada arquivo deve terminar com um comentário de fim de arquivo seguido por uma linha em branco.

### 3.4 Indentação

- a. Cada nível de recuo deve ser um múltiplo de 4 caracteres.
- b. No `switch`, `case` deve ser alinhado ao `switch`, e seu conteúdo recuado uma vez.
- c. Quebras longas de linha devem ser indentadas para legibilidade.

```c
sys_error_handler(int err)
{
    switch (err)
    {
        case ERR_THE_FIRST:
            // ...
            break;
        default:
            // ...
            break;
    }
}
```

### 3.5 Tabulações (Tabs)

- a. O caractere tab (ASCII 0x09) nunca deve aparecer em código-fonte (apenas espaços).

### 3.6 Caracteres Não-Imprimíveis

- a. Linhas de código terminam apenas com 'LF' (0x0A), nunca com 'CR'-'LF'.
- b. Único outro permitido é o 'FF' (Form Feed, 0x0C).

## 4. Regras de Módulo

### 4.1 Convenções de Nomenclatura

- a. Nomes de módulo apenas com letras minúsculas, números e underlines (`_`).
- b. Únicos nos primeiros 8 caracteres.
- c. Nenhum nome deve conflitar com a Biblioteca Padrão C/C++.
- d. Módulo contendo a função `main()` deve ter "main" no nome do arquivo.

### 4.2 Arquivos de Cabeçalho (Headers)

- a. Apenas um `.h` para cada `.c`, com o mesmo nome base.
- b. Deve conter guarda de pré-processador contra múltiplas inclusões.
- c. Deve conter apenas o estritamente necessário para outros módulos. Nenhuma variável declarada (com `extern`) ou alocada.
- d. Nenhum cabeçalho público deve incluir um cabeçalho privado.

```c
#ifndef ADC_H
#define ADC_H
// ...
#endif /* ADC_H */
```

### 4.3 Arquivos de Origem (Source)

- a. Cada arquivo controla apenas uma "entidade".
- b. Ordem das seções: comentário de cabeçalho, includes, defines/macros, variáveis estáticas, protótipos privados, funções públicas e funções privadas.
- c. Deve incluir o próprio `.h` para garantir a conferência do protótipo pelo compilador.
- d. Não usar caminhos absolutos nos includes.
- e. Livre de includes não utilizados.
- f. Nenhum `.c` deve incluir outro `.c`.

## 5. Regras de Tipos de Dados

### 5.1 Convenções de Nomenclatura

- a. Nomes de novos tipos em letras minúsculas, underlines e terminando com `_t`.
- b. Todos devem ser nomeados via `typedef`.
- c. O nome dos tipos públicos deve ser prefixado com o nome do módulo.

```c
typedef struct
{
    uint16_t count;
    uint16_t max_count;
    uint16_t _unused;
    uint16_t control;
} timer_reg_t;
```

### 5.2 Inteiros de Largura Fixa

- a. Sempre use `int8_t`, `uint8_t`, `int16_t`, `uint32_t`, etc., em vez de `char`, `short`, `int`, `long` ou `long long` quando a largura em bits importar.
- b. Palavras-chave `short` e `long` não devem ser usadas.
- c. `char` é restrito a declaração/uso de strings.

### 5.3 Inteiros Com Sinal e Sem Sinal

- a. Bit-fields não devem ser definidos dentro de tipos inteiros com sinal (signed).
- b. Operadores bit-a-bit (`&`, `|`, `~`, `^`, `<<`, `>>`) não devem ser usados em dados assinados.
- c. Inteiros assinados e não-assinados não devem ser combinados em comparações ou expressões. (Use sufixo `u` em literais).

### 5.4 Ponto Flutuante (Float)

- a. Evite constantes/variáveis de ponto flutuante. Prefira aritmética de ponto fixo.
- b. Quando necessário:
  - i. Use `float32_t`, `float64_t`.
  - ii. Adicione `f` aos literais de precisão simples (ex: `3.141592f`).
  - iii. Verifique suporte a double precision.
  - iv. Nunca teste igualdade/desigualdade (use `>` / `<`).
  - v. Verifique resultados com macro `isfinite()`.

### 5.5 Estruturas e Uniões

- a. Tome cuidado para evitar bytes de preenchimento (padding) em structs que comunicam com rede ou barramento.
- b. Cuidado com a alteração da ordem dos bit-fields pelo compilador.

```c
typedef struct
{
    uint16_t count;          // offset 0
    uint16_t max_count;      // offset 2
    uint16_t _unused;        // offset 4
    uint16_t enable : 2;     // offset 6 bits 15-14
    uint16_t b_interrupt : 1; // offset 6 bit 13
    uint16_t _unused1 : 7;   // offset 6 bits 12-6
    uint16_t b_complete : 1; // offset 6 bit 5
    uint16_t _unused2 : 4;   // offset 6 bits 4-1
    uint16_t b_periodic : 1; // offset 6 bit 0
} timer_reg_t;

// Checagem de pré-processador
#if ((8 != sizeof(timer_reg_t)))
# error "timer_reg_t struct size incorrect (expected 8 bytes)"
#endif
```

### 5.6 Booleanos

- a. Variáveis booleanas devem ser declaradas como tipo `bool`.
- b. Valores não booleanos devem ser convertidos em Booleanos usando operadores relacionais (ex: `!=`), não com casts.

```c
#include <stdbool.h>

bool b_in_motion = (0 != speed_in_mph);
```

## 6. Regras de Procedimentos (Funções)

### 6.1 Convenções de Nomenclatura

- a. Sem uso de palavras-chave do C/C++ ou `interrupt`, `inline`, `true`, etc.
- b. Sem conflitos com a Biblioteca Padrão.
- c. Não deve começar com sublinhado (`_`).
- d. Máximo de 31 caracteres.
- e. Sem letras maiúsculas (para macros).
- f. Palavras separadas por underline (`_`).
- g. Descritivos (usar verbo-substantivo, ex: `adc_read()`). Ou para respostas booleanas: `led_is_on()`.
- h. Públicas prefixadas com o módulo (`sensor_read()`).

### 6.2 Funções

- a. Tamanho limitado a 1 página impressa (cerca de 100 linhas).
- b. Tentar iniciar a função no topo da página.
- c. Preferível apenas 1 ponto de saída (`return` no final).
- d. Protótipo para todas funções públicas no `.h`.
- e. Funções privadas declaradas como `static`.
- f. Parâmetros explicitamente declarados e nomeados com clareza.

```c
int
state_change(int event)
{
    int result = ERROR;

    if (EVENT_A == event)
    {
        result = STATE_A;
    }
    else
    {
        result = STATE_B;
    }

    return (result);
}
```

### 6.3 Macros do tipo Função

- a. Macros parametrizadas não devem ser usadas se uma função resolve o problema.
- b. Se usadas:
  - i. Envolva todo o corpo entre parênteses.
  - ii. Envolva cada uso de parâmetro entre parênteses.
  - iii. Use o parâmetro no máximo 1 vez.
  - iv. Nunca transfira controle (sem `return` dentro da macro).

```c
// Não faça isso ...
#define MAX(A, B) ((A) > (B) ? (A) : (B))

// ... faça isso preferencialmente (C99)
inline int
max(int num1, int num2)
```

### 6.4 Threads de Execução

- a. Nomes de tarefas/threads devem terminar com `_thread`, `_task` ou `_process`.

```c
void
alarm_thread(void *p_data)
{
    alarm_t alarm = ALARM_NONE;
    int err = OS_NO_ERR;

    for (;;)
    {
        alarm = OSMboxPend(alarm_mbox, &err);
        // Processa o alarme...
    }
}
```

### 6.5 Rotinas de Serviço de Interrupção (ISRs)

- a. Avisar o compilador usando `#pragma` ou `__interrupt`.
- b. Nomes devem terminar com `_isr`.
- c. Declarar a ISR como `static` caso a plataforma permita.
- d. Um stub deve estar na tabela de vetor para interrupções não tratadas.

```c
#pragma irq_entry
void
timer_isr(void)
{
    uint8_t static prev = 0x00;
    uint8_t curr = *gp_button_reg;

    // Compara atual e anterior.
    g_debounced |= (prev & curr);   // registra fechamentos
    g_debounced &= (prev | curr);   // registra aberturas

    // Salva para a próxima interrupção.
    prev = curr;

    // Confirma hardware, se necessário.
}
```

## 7. Regras de Variáveis

### 7.1 Convenções de Nomenclatura

- a/b/c. Sem palavras-chave do C/C++, sem conflitos de Lib Padrão, não iniciais com underline.
- d. Máximo 31 caracteres.
- e. Mínimo 3 caracteres, inclusive contadores de loop (`row`, não `i`).
- f. Sem maiúsculas.
- g. Sem valores numéricos embutidos no nome.
- h. Separar com underlines.
- i. Descritivos.
- j. Variáveis Globais começam com `g_` (`g_zero_offset`).
- k. Variáveis de Ponteiro começam com `p_` (`p_led_reg`).
- l. Ponteiro para Ponteiro começa com `pp_` (`pp_vector_table`).
- m. Inteiros usados como Booleanos devem começar com `b_` e responder uma pergunta (`b_is_buffer_full`).
- n. Handles não-ponteiros começam com `h_` (`h_input_file`).
- o. Se múltiplo, a ordem é `[g][p|pp][b|h]`.

### 7.2 Inicialização

- a. Todas as variáveis inicializadas antes do uso.
- b. Definir variáveis locais perto de onde for necessário (C99).
- c. Variáveis globais de projeto ou de arquivo agrupadas no topo do `.c`.
- d. Ponteiros devem ser inicializados com `NULL`.

```c
uint32_t g_array[NUM_ROWS][NUM_COLS] = { ... };

for (int col = 0; col < NUM_COLS; col++)
{
    g_array[row][col] = ...;
}
```

## 8. Regras de Instruções (Statements)

### 8.1 Declarações de Variáveis

- a. O operador vírgula (`,`) não deve ser usado em declarações de variáveis.

```c
char * x, y;  // O 'y' deveria ser ponteiro também? Não faça isso.
```

### 8.2 Instruções Condicionais

- a. A estrutura if-else mais curta deve ser a primeira.
- b. Instruções if-else aninhadas não devem ter mais de 2 níveis de profundidade.
- c. Sem atribuições dentro de um teste `if` ou `else-if`.
- d. Qualquer declaração com um `else if` deve terminar com um `else`.

```c
if (NULL == p_object)
{
    result = ERR_NULL_PTR;
}
else if (p_object = malloc(sizeof(object_t)))  // ERRO: Sem atribuição!
{
    // ...
}
else
{
    // Processamento normal...
}
```

### 8.3 Switch

- a. O `break` deve ser recuado e alinhado com o `case`.
- b. Todos devem conter um bloco `default`.
- c. Qualquer case com fall-through deve possuir um comentário.

```c
switch (err)
{
    case ERR_A:
        // ...
        break;
    case ERR_B:
        // ...
        // Also perform the steps for ERR_C.
    case ERR_C:
        // ...
        break;
    default:
        // ...
        break;
}
```

### 8.4 Loops

- a. Sem números mágicos nas validações ou valores iniciais.
- b. Exceto contadores no `for`, não se pode fazer atribuição em condição de loop.
- c. Loop infinito deve ser feito usando `for (;;)`.
- d. Loops com corpo vazio devem usar chaves e ter comentários.

```c
// Errado (número mágico 100):
for (int row = 0; row < 100; row++)

// Certo:
for (int col = 0; col < NUM_COLS; col++)
{
    // ...
}
```

### 8.5 Saltos (Jumps)

- a. Restrito o uso de `goto` (apenas para pulos a frente na mesma função).
- b. Não usar `abort()`, `exit()`, `setjmp()`, `longjmp()`.

### 8.6 Testes de Equivalência

- a. O valor da constante deve ser colocado sempre à esquerda do operador `==`.

```c
if (NULL == p_object)
{
    return (ERR_NULL_PTR);
}
```

Raciocínio: Se você esquecer um `=`, o compilador acusará erro, pois não se pode atribuir valor ao `NULL` ou a uma constante.

---

## Templates de Arquivos (Apêndices B e C)

### Template de Arquivo de Cabeçalho (module.h)

```c
/** @file module.h
 *
 * @brief A description of the module's purpose.
 *
 * @par
 * COPYRIGHT NOTICE: (c) 2018 Barr Group. All rights reserved.
 */

#ifndef MODULE_H
#define MODULE_H

int8_t max8(int8_t num1, int8_t num2);

#endif /* MODULE_H */

/*** end of file ***/
```

### Template de Arquivo de Código-Fonte (module.c)

```c
/** @file module.c
 *
 * @brief A description of the module's purpose.
 *
 * @par
 * COPYRIGHT NOTICE: (c) 2018 Barr Group. All rights reserved.
 */

#include <stdint.h>
#include <stdbool.h>
#include "module.h"

/*!
 * @brief Identify the larger of two 8-bit integers.
 *
 * @param[in] num1 The first number to be compared.
 * @param[in] num2 The second number to be compared.
 *
 * @return The value of the larger number.
 */
int8_t
max8(int8_t num1, int8_t num2)
{
    return ((num1 > num2) ? num1 : num2);
}

/*** end of file ***/
```

---

## Programa de Exemplo Completo (Apêndice D: Biblioteca CRC)

### crc.h

```c
/** @file crc.h
 *
 * @brief Compact CRC library for embedded systems for
 *        CRC-CCITT, CRC-16, CRC-32.
 *
 * @par
 * COPYRIGHT NOTICE: (c) 2000, 2018 Michael Barr. This software
 * is placed in the public domain and may be used for any purpose.
 * However, this notice must not be changed or removed. No warranty
 * is expressed or implied by the publication or distribution of
 * this source code.
 */

#ifndef CRC_H
#define CRC_H

// Compile-time selection of the desired CRC algorithm.
//
#if defined(CRC_CCITT)
# define CRC_NAME "CRC-CCITT"
typedef uint16_t crc_t;

#elif defined(CRC_16)
# define CRC_NAME "CRC-16"
typedef uint16_t crc_t;

#elif defined(CRC_32)
# define CRC_NAME "CRC-32"
typedef uint32_t crc_t;

#else
# error "One of CRC_CCITT, CRC_16, or CRC_32 must be #define'd."
#endif

// Public API functions provided by the Compact CRC library.
//
void   crc_init(void);
crc_t  crc_slow(uint8_t const * const p_message, int n_bytes);
crc_t  crc_fast(uint8_t const * const p_message, int n_bytes);

#endif /* CRC_H */

/*** end of file ***/
```

### crc.c

```c
/** @file crc.c
 *
 * @brief Compact CRC generator for embedded systems, with brute
 *        force and table-driven algorithm options. Supports
 *        CRC-CCITT, CRC-16, and CRC-32 standards.
 *
 * @par
 * COPYRIGHT NOTICE: (c) 2000, 2018 Michael Barr. This software
 * is placed in the public domain and may be used for any purpose.
 * However, this notice must not be changed or removed. No warranty
 * is expressed or implied by the publication or distribution of
 * this source code.
 */

#include <stdint.h>
#include "crc.h"

// Algorithmic parameters based on CRC elections made in crc.h.
//
#define BITS_PER_BYTE 8
#define WIDTH         (BITS_PER_BYTE * sizeof(crc_t))
#define TOPBIT        (1 << (WIDTH - 1))

// Allocate storage for the byte-wide CRC lookup table.
//
#define CRC_TABLE_SIZE 256
static crc_t g_crc_table[CRC_TABLE_SIZE];

// Further algorithmic configuration.
//
#if defined(CRC_CCITT)
# define POLYNOMIAL       ((crc_t) 0x1021)
# define INITIAL_REMAINDER ((crc_t) 0xFFFF)
# define FINAL_XOR_VALUE  ((crc_t) 0x0000)
# define REFLECT_DATA(X)       (X)
# define REFLECT_REMAINDER(X)  (X)

#elif defined(CRC_16)
# define POLYNOMIAL       ((crc_t) 0x8005)
# define INITIAL_REMAINDER ((crc_t) 0x0000)
# define FINAL_XOR_VALUE  ((crc_t) 0x0000)
# define REFLECT_DATA(X)  ((uint8_t) reflect((X), BITS_PER_BYTE))
# define REFLECT_REMAINDER(X) ((crc_t) reflect((X), WIDTH))

#elif defined(CRC_32)
# define POLYNOMIAL       ((crc_t) 0x04C11DB7)
# define INITIAL_REMAINDER ((crc_t) 0xFFFFFFFF)
# define FINAL_XOR_VALUE  ((crc_t) 0xFFFFFFFF)
# define REFLECT_DATA(X)  ((uint8_t) reflect((X), BITS_PER_BYTE))
# define REFLECT_REMAINDER(X) ((crc_t) reflect((X), WIDTH))
#endif

/*!
 * @brief Compute the reflection of a set of data bits.
 *
 * @param[in] data  The data bits to be reflected.
 * @param[in] n_bits The number of bits.
 *
 * @return The reflected data.
 */
static uint32_t
reflect(uint32_t data, uint8_t n_bits)
{
    uint32_t reflection = 0x00000000;

    // NOTE: For efficiency, n_bits is not verified to be <= 32.

    // Reflect the data about the center bit.
    //
    for (uint8_t bit = 0u; bit < n_bits; ++bit)
    {
        // If the LSB bit is set, set the reflection of it.
        //
        if (data & 0x01u)
        {
            reflection |= (1u << ((n_bits - 1u) - bit));
        }

        data = (data >> 1u);
    }

    return (reflection);
}

/*!
 * @brief Initialize the lookup table for byte-by-byte CRC.
 *
 * @par
 * This function must be run before crc_fast() or the table
 * stored in ROM.
 */
void
crc_init(void)
{
    // Compute the remainder of each possible dividend.
    //
    for (crc_t dividend = 0u; dividend < CRC_TABLE_SIZE; ++dividend)
    {
        // Start with the dividend followed by zeros.
        //
        crc_t remainder = dividend << (WIDTH - BITS_PER_BYTE);

        // Perform modulo-2 division, a bit at a time.
        //
        for (int bit = BITS_PER_BYTE; bit > 0; --bit)
        {
            // Try to divide the current data bit.
            //
            if (remainder & TOPBIT)
            {
                remainder = (remainder << 1) ^ POLYNOMIAL;
            }
            else
            {
                remainder = (remainder << 1);
            }
        }

        // Store the result into the table.
        //
        g_crc_table[dividend] = remainder;
    }
}

/*!
 * @brief Compute the CRC of an array of bytes, bit-by-bit.
 *
 * @param[in] p_message A pointer to the array of data bytes.
 * @param[in] n_bytes   The number of bytes in the array.
 *
 * @return The CRC of the array of data.
 */
crc_t
crc_slow(uint8_t const * const p_message, int n_bytes)
{
    crc_t remainder = INITIAL_REMAINDER;

    // Perform modulo-2 division, one byte at a time.
    //
    for (int byte = 0; byte < n_bytes; ++byte)
    {
        // Bring the next byte into the remainder.
        //
        remainder ^= (REFLECT_DATA(p_message[byte])
                      << (WIDTH - BITS_PER_BYTE));

        // Perform modulo-2 division, one bit at a time.
        //
        for (int bit = BITS_PER_BYTE; bit > 0; --bit)
        {
            // Try to divide the current data bit.
            //
            if (remainder & TOPBIT)
            {
                remainder = (remainder << 1) ^ POLYNOMIAL;
            }
            else
            {
                remainder = (remainder << 1);
            }
        }
    }

    // The final remainder is the CRC result.
    //
    return (REFLECT_REMAINDER(remainder) ^ FINAL_XOR_VALUE);
}

/*!
 * @brief Compute the CRC of an array of bytes, byte-by-byte.
 *
 * @param[in] p_message A pointer to the array of data bytes.
 * @param[in] n_bytes   The number of bytes in the array.
 *
 * @return The CRC of the array of data.
 */
crc_t
crc_fast(uint8_t const * const p_message, int n_bytes)
{
    crc_t remainder = INITIAL_REMAINDER;

    // Divide the message by the polynomial, a byte at a time.
    //
    for (int byte = 0; byte < n_bytes; ++byte)
    {
        uint8_t data = REFLECT_DATA(p_message[byte])
                       ^ (remainder >> (WIDTH - BITS_PER_BYTE));

        remainder = g_crc_table[data] ^ (remainder << BITS_PER_BYTE);
    }

    // The final remainder is the CRC.
    //
    return (REFLECT_REMAINDER(remainder) ^ FINAL_XOR_VALUE);
}

/*** end of file ***/
```
