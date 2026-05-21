Guia de Estrutura e Geração de Testes Automatizados - Python

Este documento define a arquitetura padrão de testes para o projeto interface_display (Python). O princípio fundamental é o isolamento: cada módulo do projeto possui uma pasta exclusiva dentro do diretório de testes, garantindo organização, facilidade de manutenção e clareza na hora de rastrear falhas.

1. Regra de Ouro da Estrutura de Testes
A pasta de testes sempre ficará na raiz do projeto e se chamará testes. Dentro dela, haverá uma pasta homônima ao módulo testado, e dentro desta pasta, os arquivos de teste.
Fórmula: testes / [nome_do_modulo] / test_[nome_do_modulo].py

2. Estrutura no Projeto Python (interface_display)
No projeto Python, utilizaremos o pytest. O pytest descobre os testes automaticamente, desde que sigam o padrão de nomenclatura test_*.py.

```
interface_display/
├── main.py
├── modules/
│   ├── serial_comm.py
│   └── hardware_info.py
└── testes/
    ├── serial_comm/
    │   └── test_serial_comm.py
    └── hardware_info/
        └── test_hardware_info.py
```

3. Configuração do pytest.ini
Para que o pytest encontre os testes nessa estrutura aninhada, crie um arquivo pytest.ini na raiz do projeto interface_display:

```ini
[pytest]
testpaths = testes
python_files = test_*.py
python_functions = test_*
```

4. Diretrizes para Geração de Testes

Regra 1: Isolamento Estrito de Hardware e I/O
Sempre utilizar unittest.mock.patch para simular a lib pyserial, psutil e GPUtil. O teste não deve tentar acessar a serial real ou o hardware da máquina onde está rodando.

Regra 2: Pelo menos 1 teste de "Caminho Feliz" e 1 de "Falha"
Cada módulo deve ter, no mínimo:
- Um teste de sucesso (ex: JSON válido, hardware respondeu corretamente ao mock).
- Um teste de erro/tratamento de exceção (ex: JSON malformatado gerando NACK, falha ao abrir porta serial).

Regra 3: Nomenclatura Descritiva
As funções de teste devem descrever a ação e o resultado esperado.
- Python (Pytest): `def test_get_cpu_info_returns_correct_format():`

Regra 4: Setup/Teardown
Usar fixtures do pytest ou setUp/tearDown do unittest para instanciar e destruir os mocks antes e depois de cada teste.

Regra 5: Padrão de Código PEP 8
Os testes em Python devem seguir o PEP 8 (Snake case, 4 espaços, docstrings).

5. Exemplo Prático (Módulo Serial Comm)

```python
import pytest
from unittest.mock import patch, MagicMock
from modules import serial_comm

"""Testes do módulo de comunicação serial.
Segue PEP 8 e utiliza mocks para isolar o hardware real.
"""

@patch('modules.serial_comm.serial.Serial')
def test_send_data_formats_json_correctly(mock_serial_class):
    """Teste de Caminho Feliz: Verifica se o dict é convertido para JSON com \\n"""
    mock_instance = MagicMock()
    mock_serial_class.return_value = mock_instance
    serial_comm.connect(port="COM_FAKE")
    sample_data = {"target": "CPU", "usage": 50.0, "temp": 60.0, "clock": 3000}
    serial_comm.send_data(sample_data)
```
