# Tipos de Dados — Projetos Embarcados

## 1. Inteiros de Largura Fixa

- Usar **sempre** `int8_t`, `uint8_t`, `int16_t`, `uint32_t`, etc.
- **Proibido:** `short`, `long`, `long long`.
- `char` apenas para strings.

## 2. Signed vs Unsigned

- Bit-fields nunca em tipos signed.
- Operadores bit-a-bit (`&`, `|`, `~`, `^`, `<<`, `>>`) nunca em dados signed.
- Nunca misturar signed e unsigned em comparações — usar sufixo `u`.

```c
if (0u == count)  /* certo */
if (0 == count)   /* errado se count for unsigned */
```

## 3. Booleanos

- Tipo `bool` (`<stdbool.h>`).
- Avaliar diretamente: `if (flag)` / `if (!flag)`.
- **Proibido:** `if (flag == true)` / `if (flag == false)`.
- Conversão com operador relacional:

```c
bool b_in_motion = (0 != speed_in_mph);
```

## 4. Ponto Flutuante

- Preferir aritmética de ponto fixo.
- Quando necessário:
  - Usar `float32_t`, `float64_t`.
  - Sufixo `f` em literais: `3.141592f`.
  - Nunca testar igualdade — usar `>` / `<`.
  - Verificar resultados com `isfinite()`.

## 5. Literais

| Tipo | Sufixo | Exemplo |
|------|--------|---------|
| Unsigned | `u` | `0u`, `100u`, `0x3Cu` |
| Float | `f` | `3.14f`, `100.0f` |

## 6. Structs e Uniões

- Cuidado com padding em structs que comunicam com rede/barramento.
- Verificar ordem de bit-fields.
- Usar `#if` para validar tamanho:

```c
#if (8 != sizeof(timer_reg_t))
# error "timer_reg_t struct size incorrect (expected 8 bytes)"
#endif
```

## 7. Tipos Nomeados

- `snake_case` terminando com `_t`: `timer_reg_t`.
- Sempre via `typedef`.
- Prefixo do módulo para tipos públicos.
