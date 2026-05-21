Guia Geral do Projeto PC (Python)

1. Formatação e Padrões (PEP 8)
- Indentação: 4 espaços (nunca tabs).
- Nomenclatura:
  - Módulos/Variáveis/Funções: snake_case
  - Constantes: UPPER_SNAKE_CASE
- Imports: Agrupados na ordem: Bibliotecas padrão, bibliotecas de terceiros, módulos locais. Separados por linha em branco.
- Linting/Formatador: Utilizar Black e Flake8 para garantir a conformidade estrita com o PEP 8.
- Docstrings: Utilizar docstrings no estilo Google ou NumPy para documentar funções e classes.

2. Arquitetura de Pastas

```
pc_monitor/
├── requirements.txt
├── main.py            # Arquivo principal que orquestra a execução
└── modules/
    ├── __init__.py
    ├── serial_comm.py    # Módulo de comunicação serial / JSON
    └── hardware_info.py  # Módulo de coleta de dados da CPU/GPU
```

3. Dependências (requirements.txt)

```
pyserial>=3.5
psutil>=5.9.0
GPUtil>=1.4.0
```
