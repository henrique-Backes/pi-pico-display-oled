# Práticas de Codificação — Projetos Embarcados (C)

> Padrão BARR-C:2018 para firmware Raspberry Pi Pico e Arduino.

## Documentos

| Arquivo | Tópico |
|---------|--------|
| `00_regras_gerais.md` | C99, line width, chaves, parênteses, keywords |
| `01_formatacao.md` | Espaços, indentação, tabs, linhas em branco |
| `02_tipos_dados.md` | Tipos fixos, booleanos, float, literais, structs |
| `03_nomenclatura.md` | Prefixos variáveis, funções, tipos, módulos |
| `04_funcoes.md` | Tamanho, fail-fast, return type separado, static |
| `05_comentarios.md` | Doxygen, estilo PT-BR, casts, código desativado |
| `06_modulos.md` | Headers, source, include guards, templates |
| `07_loops.md` | for (;;), Yoda conditions, switch, sem números mágicos |
| `08_testes.md` | Unity, estrutura testes/, mocks, setUp/tearDown |
| `09_checklist.md` | Checklist visual + resumo rápido em tabela |

## Princípios Fundamentais

- Documentação em **PT-BR**, código em **English**
- `main()` como orquestrador — módulos encapsulados
- Gerar arquivos completos, sem remendos
- Sem validações não solicitadas
