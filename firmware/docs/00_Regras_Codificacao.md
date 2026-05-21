# Regras de Codificação do Projeto

## 1. Teste de Variáveis Booleanas

- **Proibido:** `if (flag == true)` ou `if (flag == false)`
- **Obrigatório:** `if (flag)` ou `if (!flag)`

## 2. Lógica Fail-Fast (Early Returns)

- **Proibido:** Nested ifs profundos
- **Obrigatório:** Testar condições de falha no início e retornar imediatamente. O caminho feliz fica no final, com indentação rasa.

## 3. Padrão BARR-C: Sufixos Literais e Comparações

- Sufixo `u` em literais inteiros sem sinal: `0u`, `60000u`, `100u`
- Yoda Conditions: constante à esquerda: `if (2u == config)`

## 4. Formatação de Chaves

- Abertura e fechamento em linha nova, isolada e alinhada
- Espaço entre keyword e parêntese: `if (`, `while (`, `for (`

## 5. Geração de Código Completa

- Proibido remendos ou trechos isolados
- Gerar arquivo completo ou bloco consolidado

## 6. Documentação (Doxygen)

- **Interface (.h):** Doxygen obrigatório acima de todas as funções públicas
- **Implementação (.c):**
  - Tipo de retorno em linha separada do nome da função
  - Doxygen apenas para funções `static`
  - Comentários internos focam em regras de negócio

## 7. Convenções de Nomenclatura

- Prefixo `g_` para variáveis globais
- Prefixo `gb_` para globais booleanas
- `Módulo_Prefixo_Ação`: `Display_Init()`, `Protocol_Parse()`

## 8. Proibição de Validações de Limites Intrusivas

- Não implementar validações não solicitadas
- Se julgar vital, perguntar antes

## 9. Separação de Responsabilidades

- Módulos são cegos para lógicas alheias
- O main atua como orquestrador (Maestro)

## 10. Checklist Visual da Função

- Retorno e nome separados em linhas distintas no .c?
- Chaves em linhas exclusivas?
- Early returns no topo?
- Constantes à esquerda com `u`?
- Booleanos avaliados por si mesmos?
- Sem comentários óbvios?
