# Regras Gerais — Projetos Alto Nível

## 1. Idiomas

- **Documentação e comentários:** Português (Brazilian).
- **Identificadores de código:** English.

## 2. Arquitetura

- **Main como orquestrador** — coordena módulos, não implementa lógica.
- **Módulos encapsulados** — cada módulo cuida de sua responsabilidade.
- **Não adicionar validações não solicitadas** — perguntar antes.

## 3. Geração de Código

- Gerar arquivos completos ou blocos consolidados.
- Proibido remendos ou trechos isolados.

## 4. Estrutura de Testes (Padrão Universal)

- Pasta: `testes/` (sempre em português).
- Layout: `testes/<modulo>/test_<modulo>.<ext>`.
- Mínimo: 1 teste sucesso + 1 teste falha por módulo.
- Isolar hardware/I/O real.
- Nomes descritivos que indicam ação e resultado esperado.

## 5. Protocolo JSON (Comum)

- Mensagens terminam com `\n`.
- Encoding: UTF-8.
- Respostas: `{"status": "ACK", "msg": "..."}` ou `{"status": "NACK", "msg": "..."}`.

## 6. Dependências Opcionais

- Usar fallback chains: tentar lib A → B → C.
- Imports com `try/except` (Python) ou `try/catch` (C#).
- Dependências opcionais não precisam estar em `requirements.txt`.
