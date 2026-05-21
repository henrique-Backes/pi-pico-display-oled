# Regras Gerais — Projetos Embarcados

## 1. Qual C?

- **C99** obrigatório.
- Compilador C++ deve ser restrito ao subconjunto C.
- Extensões proprietárias, `#pragma` e assembly inline apenas no mínimo necessário em drivers.
- `#define` nunca deve renomear keywords da linguagem.

```c
/* Não faça isso */
#define begin {
#define end   }
```

## 2. Largura de Linha

- Máximo **80 caracteres**.

## 3. Chaves (Allman)

- `{` sempre em linha própria, alinhado com `}`.
- Chaves obrigatórias mesmo em blocos de uma linha.

```c
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
```

## 4. Parênteses

- Nunca confiar em precedência de operadores.
- Operandos de `&&` e `||` sempre entre parênteses.

```c
if ((depth_in_cm > 0) && (depth_in_cm < MAX_DEPTH))
{
    depth_in_ft = convert_depth_to_ft(depth_in_cm);
}
```

## 5. Keywords

### Usar

- `static` — funções/variáveis locais ao módulo.
- `const` — variáveis imutáveis, parâmetros somente leitura, alternativa tipada ao `#define`.
- `volatile` — variáveis acessadas por ISR, múltiplas threads, registradores mapeados, contadores de delay.

### Proibidos

- `auto`, `register`.

### Evitar

- `goto` — apenas para frente no mesmo bloco.
- `continue` — preferível evitar.
- `abort()`, `exit()`, `setjmp()`, `longjmp()` — proibidos.

## 6. Casts

- Todo cast deve ter comentário explicando por que é seguro.

```c
uint16_t sample = adc_read(ADC_CHANNEL_1);
result = abs((int) sample); /* AVISO: Assume-se que int tenha 32 bits. */
```
