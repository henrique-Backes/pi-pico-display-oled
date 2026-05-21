# Python — Testes (pytest)

## 1. Estrutura

- Pasta: `testes/` (nunca `tests/`).
- Layout: `testes/<nome_modulo>/test_<nome_modulo>.py`.

```
projeto/
├── main.pyw
├── pytest.ini
├── modules/
│   ├── serial_comm.py
│   └── hardware_info.py
└── testes/
    ├── serial_comm/
    │   └── test_serial_comm.py
    └── hardware_info/
        └── test_hardware_info.py
```

## 2. Configuração (pytest.ini)

```ini
[pytest]
testpaths = testes
python_files = test_*.py
python_functions = test_*
```

## 3. Diretrizes

- **Isolamento estrito:** mockar hardware I/O com `unittest.mock.patch`.
- Mínimo: 1 teste caminho feliz + 1 teste falha.
- **Reset de estado global** em `teardown_method`:
  - Serial ports → `disconnect()` ou `None`.
  - Singletons/caches → reset explícito.
- Nomenclatura: `def test_get_cpu_info_returns_correct_format():`.
- Usar **fixtures** do pytest para setup/teardown.
- Seguir PEP 8.

## 4. Exemplo

```python
import pytest
from unittest.mock import patch, MagicMock
from modules import serial_comm

@patch('modules.serial_comm.serial.Serial')
def test_send_data_formats_json_correctly(mock_serial_class):
    """Teste de Caminho Feliz: Verifica conversão para JSON com \\n"""
    mock_instance = MagicMock()
    mock_serial_class.return_value = mock_instance
    serial_comm.connect(port="COM_FAKE")
    sample_data = {"target": "CPU", "usage": 50.0}
    serial_comm.send_data(sample_data)
    mock_instance.write.assert_called_once()
```

## 5. Comandos

```bash
pytest                          # Todos os testes
pytest testes/hardware_info/    # Módulo específico
pytest -k test_cpu              # Filtrar por nome
```
