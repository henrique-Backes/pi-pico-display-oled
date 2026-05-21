# Funções — Projetos Embarcados

## 1. Tamanho

- Máximo ~100 linhas (1 página impressa).

## 2. Fail-Fast / Early Returns

- Testar condições de falha no início.
- Retornar imediatamente.
- Caminho feliz fica no final, com indentação rasa.
- **Proibido:** nested ifs profundos (máx 2 níveis).

```c
int8_t
process_data(uint8_t const * const p_data, uint16_t length)
{
    int8_t result = ERROR;

    if (NULL == p_data)
    {
        return (ERR_NULL_PTR);
    }

    if (0u == length)
    {
        return (ERR_EMPTY);
    }

    /* Caminho feliz */
    result = parse_buffer(p_data, length);

    return (result);
}
```

## 3. Tipo de Retorno

- Em **linha separada** do nome no `.c`:

```c
int8_t
max8(int8_t num1, int8_t num2)
{
    return ((num1 > num2) ? num1 : num2);
}
```

## 4. Visibilidade

- `static` para funções locais ao módulo.
- Protótipos públicos no `.h`.
- Parâmetros explicitamente declarados e nomeados.

## 5. Macros do Tipo Função

- Evitar — preferir `inline` functions (C99).
- Se usadas:
  - Corpo entre parênteses.
  - Cada parâmetro entre parênteses.
  - Usar parâmetro no máximo 1 vez.
  - Sem `return` dentro.

```c
/* Não faça */
#define MAX(A, B) ((A) > (B) ? (A) : (B))

/* Faça */
inline int
max(int num1, int num2)
{
    return ((num1 > num2) ? num1 : num2);
}
```
