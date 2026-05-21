# Módulos e Arquivos — Projetos Embarcados

## 1. Headers (.h)

- Um `.h` por `.c`, mesmo nome base.
- Include guard obrigatório.
- Apenas o estritamente necessário para outros módulos.
- Nenhuma variável declarada (`extern`) ou alocada.
- Nenhum header público inclui header privado.

```c
#ifndef MODULE_H
#define MODULE_H

#ifdef __cplusplus
extern "C" {
#endif

int8_t max8(int8_t num1, int8_t num2);

#ifdef __cplusplus
}
#endif

#endif /* MODULE_H */

/*** end of file ***/
```

## 2. Source (.c)

- Cada `.c` inclui seu próprio `.h` como primeiro include local.
- Ordem das seções:
  1. Header comment
  2. Includes
  3. Defines/macros
  4. Variáveis estáticas
  5. Protótipos privados
  6. Funções públicas
  7. Funções privadas
- Sem caminhos absolutos nos includes.
- Nenhum `.c` inclui outro `.c`.
- Livre de includes não utilizados.
- **Todo arquivo termina com:** `/*** end of file ***/`

## 3. Inicialização de Variáveis

- Todas inicializadas antes do uso.
- Locais definidas perto do uso (C99).
- Globais agrupadas no topo do `.c`.
- Ponteiros inicializados com `NULL`.
- Sem vírgula em declarações em série:

```c
/* Errado */
char *x, y;  /* y não é ponteiro */

/* Certo */
char *p_x;
char  y;
```
