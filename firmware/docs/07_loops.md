# Loops e Condicionais — Projetos Embarcados

## 1. Yoda Conditions

- Constante sempre à esquerda em comparações de igualdade:

```c
if (NULL == p_object)
if (0u == count)
if (2u == config)
```

Razão: se esquecer um `=`, o compilador acusa erro (não se pode atribuir a constante).

## 2. Loops Infinitos

- Usar **sempre** `for (;;)`.
- **Proibido:** `while (1)`, `while (true)`.

```c
void alarm_thread(void *p_data)
{
    alarm_t alarm = ALARM_NONE;

    for (;;)
    {
        alarm = OS_MboxPend(alarm_mbox, &err);
        /* Processa o alarme... */
    }
}
```

## 3. Números Mágicos

- Proibidos em validações ou valores iniciais de loop.

```c
/* Errado */
for (int row = 0; row < 100; ++row)

/* Certo */
for (int col = 0; col < NUM_COLS; ++col)
```

## 4. Loops com Corpo Vazio

- Devem usar chaves e comentário.

```c
while ((status_reg & READY_BIT) == 0u)
{
    /* Aguarda hardware ficar pronto */
}
```

## 5. Condicionais

- If-else mais curto primeiro.
- Máximo 2 níveis de nesting.
- Sem atribuição dentro de `if` ou `else-if`.
- Todo `else if` deve terminar com `else`.
- Booleanos avaliados por si mesmos:

```c
if (flag)       /* certo */
if (!flag)      /* certo */
if (flag == true)  /* proibido */
```

## 6. Switch

- `break` alinhado com `case`.
- Todo switch deve ter `default`.
- Fall-through deve ter comentário.

```c
switch (err)
{
    case ERR_A:
        /* ... */
        break;
    case ERR_B:
        /* ... */
        /* Also perform the steps for ERR_C. */
    case ERR_C:
        /* ... */
        break;
    default:
        /* ... */
        break;
}
```
