# Checklist e Resumo — Projetos Embarcados

## Checklist Visual da Função

- [ ] Retorno e nome separados em linhas distintas no `.c`?
- [ ] Chaves em linhas exclusivas (Allman)?
- [ ] Early returns no topo (fail-fast)?
- [ ] Constantes à esquerda com sufixo `u`?
- [ ] Booleanos avaliados por si mesmos?
- [ ] Sem comentários óbvios?
- [ ] Arquivo termina com `/*** end of file ***/`?

## Resumo Rápido

| Regra | Exemplo |
|-------|---------|
| Chaves Allman | `{` em linha própria |
| Yoda conditions | `if (0u == count)` |
| Sufixo unsigned | `100u`, `0x3Cu` |
| Sufixo float | `3.14f` |
| Tipos fixos | `uint8_t`, nunca `int` |
| Bool direto | `if (flag)`, nunca `== true` |
| Prefixos | `g_`, `gb_`, `p_`, `b_` |
| Funções | `Modulo_Acao()` |
| Retorno separado | Linha própria no `.c` |
| Loop infinito | `for (;;)` |
| Indentação | 4 espaços, sem tabs |
| Largura linha | 80 chars máx |
| Loop vars | Mín 3 chars (`row`) |
| Arquivo termina | `/*** end of file ***/` |
| Doxygen | `.h` público, `.c` static |
| Fail-fast | Early returns, sem nesting |
| Casts | Comentário obrigatório |
| `//` comments | Proibidos — usar `/* */` |
