Módulo: Hardware Info (hardware_info.py)

1. Responsabilidade
Coletar os dados reais de hardware (CPU e GPU) do sistema operacional e retorná-los em dicionários que correspondam exatamente ao formato JSON estipulado no 02_Protocolo_JSON.md.

2. Interface Esperada

```python
def get_cpu_info() -> dict:
    """Retorna dict no formato: {"target": "CPU", "usage": x, "temp": y, "clock": z}"""

def get_gpu_info() -> dict:
    """Retorna dict no formato: {"target": "GPU", "usage": x, "temp": y, "vram_used": z, "vram_total": w}"""
```

3. Guia de Desenvolvimento
- CPU: Usar a biblioteca psutil.
  - Uso: `psutil.cpu_percent(interval=1)`
  - Clock: `psutil.cpu_freq().current`
  - Temp: `psutil.sensors_temperatures().get('coretemp', [{}])[0].current`
  - Atenção: temperatura requer configuração por SO, no Windows pode ser necessário bibliotecas alternativas como wmi ou pythonnet.
- GPU: Usar a biblioteca GPUtil.
  - Uso, Temp e VRAM podem ser extraídos de `GPUtil.getGPUs()[0]`.
  - Nota: Em Windows, GPUtil usa WMI via subprocess. Em Linux, usa nvidia-smi. Funciona nativamente apenas para NVIDIA. Caso use AMD/Intel, mapear bibliotecas específicas.
- Tipagem: Garantir que os retornos estejam no tipo correto (float para uso/temp, int para clock).
