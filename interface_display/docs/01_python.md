# Python — Práticas de Codificação

## 1. Padrão (PEP 8)

- **Indentação:** 4 espaços, nunca tabs.
- **Largura de linha:** 79 chars (PEP 8) ou 88 (Black).
- **Formatador:** Black + Flake8.

## 2. Nomenclatura

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Módulos | `snake_case` | `serial_comm.py` |
| Variáveis | `snake_case` | `cpu_usage` |
| Funções | `snake_case` | `get_cpu_info()` |
| Classes | `PascalCase` | `PcMonitorApp` |
| Constantes | `UPPER_SNAKE_CASE` | `DEFAULT_BAUDRATE` |
| Privados | `_leading_underscore` | `_lhm_available` |

## 3. Imports

Agrupados na ordem, separados por linha em branco:

1. Bibliotecas padrão
2. Bibliotecas de terceiros
3. Módulos locais

```python
import json
import sys

import serial
import psutil

from modules import serial_comm
```

## 4. Docstrings

- Estilo **Google** ou **NumPy**.
- Em português (Brazilian).

```python
def connect(port: str, baudrate: int = 115200) -> bool:
    """Estabelece conexão serial com o dispositivo.

    Args:
        port: Nome da porta COM (ex: "COM3").
        baudrate: Velocidade de comunicação.

    Returns:
        True se conectado com sucesso, False caso contrário.
    """
```

## 5. Dependências Opcionais

- Imports com `try/except` para fallback chains.

```python
try:
    import clr
    HAS_PYTHONNET = True
except ImportError:
    HAS_PYTHONNET = False
```

## 6. Arquivo Principal

- Usar `.pyw` para suprimir console window: `python main.pyw`.

## 7. Comunicação Serial

- JSON + `\n` terminated, UTF-8.
- Baudrate padrão: **115200**.
- Resposta: `{"status": "ACK"|"NACK", "msg": "..."}`.
