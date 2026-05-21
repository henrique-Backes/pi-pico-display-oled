# Formatação — Projetos Embarcados

## 1. Espaços

| Contexto | Regra | Exemplo |
|----------|-------|---------|
| Keywords `if`, `while`, `for`, `switch`, `return` | 1 espaço após | `if (cond)` |
| Operadores binários (`=`, `+`, `==`, `&&`) | 1 espaço antes e depois | `a = b + c` |
| Operadores unários (`!`, `++`, `--`) | Sem espaço | `!flag`, `++i` |
| Ponteiros em declaração | Espaço em ambos lados | `int * p_ptr` |
| Ponteiros em uso | Sem espaço | `*p_ptr` |
| Ternário (`?`, `:`) | 1 espaço antes e depois | `a ? b : c` |
| Acesso struct (`->`, `.`) | Sem espaços | `ptr->field`, `obj.field` |
| Colchetes array | Sem espaços | `arr[0]` |
| Parênteses expressão | Sem espaços internos | `(a + b)` |
| Chamada de função | Sem espaço | `func(arg)` |
| Declaração de função | 1 espaço antes de `(` | `void foo (int arg)` |
| Vírgula parâmetros | 1 espaço após | `func(a, b)` |
| Ponto e vírgula no `for` | 1 espaço após | `for (i = 0; i < n; ++i)` |
| Ponto e vírgula fim instrução | Sem espaço antes | `stmt;` |

## 2. Alinhamento

- Variáveis em declarações em série: alinhar primeiro caractere.
- Membros de struct/union: alinhados.
- Operadores de atribuição em blocos adjacentes: alinhados.
- `#` de diretivas sempre no início da linha.

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

## 3. Indentação

- **4 espaços** por nível.
- `switch`: `case` alinhado ao `switch`, conteúdo recuado.

```c
switch (err)
{
    case ERR_THE_FIRST:
        /* ... */
        break;
    default:
        /* ... */
        break;
}
```

## 4. Tabs

- **Proibido** — apenas espaços.

## 5. Linhas em Branco

- Máximo uma instrução por linha.
- Linha em branco antes e depois de cada bloco natural.
- Arquivo termina com comentário de fim + linha em branco.

## 6. Caracteres Não-Imprimíveis

- LF (0x0A) apenas — nunca CR-LF.
- FF (0x0C) permitido.
