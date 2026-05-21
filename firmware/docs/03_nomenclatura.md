# Nomenclatura — Projetos Embarcados

## 1. Variáveis

### Prefixos

| Prefixo | Uso | Exemplo |
|---------|-----|---------|
| `g_` | Globais | `g_zero_offset` |
| `gb_` | Globais booleanas | `gb_system_ready` |
| `p_` | Ponteiros | `p_led_reg` |
| `pp_` | Ponteiro para ponteiro | `pp_vector_table` |
| `b_` | Booleanos locais (respondem pergunta) | `b_is_buffer_full` |
| `h_` | Handles não-ponteiros | `h_input_file` |

- Ordem múltipla: `[g][p|pp][b|h]` — ex: `gp_buffer` (global pointer).

### Regras

- Mínimo **3 caracteres** (inclusive loop: `row`, não `i`).
- Máximo 31 caracteres.
- `snake_case`, sem maiúsculas.
- Sem números embutidos no nome.
- Sem underline inicial.
- Sem conflito com lib padrão C/C++.

## 2. Funções

- Formato: `Modulo_VerbosSubstantivo()` — ex: `Display_Init()`, `Protocol_Parse()`.
- Públicas prefixadas com módulo.
- Verbos-substantivo: `sensor_read()`, `adc_convert()`.
- Booleanas: `led_is_on()`, `button_is_pressed()`.
- Máximo 31 caracteres.
- Sem underline inicial.
- Sem conflito com lib padrão.

## 3. Tipos

- `snake_case` terminando com `_t`: `timer_reg_t`.
- Prefixo do módulo para tipos públicos.
- Sempre via `typedef`.

## 4. Módulos

- Minúsculas, números e `_`.
- Únicos nos primeiros 8 caracteres.
- Sem conflito com lib padrão C/C++.
- Arquivo com `main()` deve ter "main" no nome.

## 5. Threads/ISRs

- Threads: terminam com `_thread`, `_task` ou `_process`.
- ISRs: terminam com `_isr`.

```c
void alarm_thread(void *p_data);
void timer_isr(void);
```
