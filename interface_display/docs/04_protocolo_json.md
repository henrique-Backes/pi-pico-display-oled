# Protocolo JSON — PC ↔ Embarcado

## 1. Formato

- Encoding: **UTF-8**.
- Terminador: `\n` (newline).
- Método de envio: `WriteLine()` (C#) ou `write(data + "\n")` (Python).

## 2. Mensagens do PC

### CPU

```json
{"target":"CPU","usage":45.5,"temp":62.0,"clock":3600}
```

### GPU

```json
{"target":"GPU","usage":80.0,"temp":71.0,"vram_used":6.2,"vram_total":8.0}
```

## 3. Respostas do Embarcado

### ACK

```json
{"status":"ACK","msg":"Dados recebidos"}
```

### NACK

```json
{"status":"NACK","msg":"JSON invalido"}
```

## 4. Implementação

### Python (envio)

```python
import json

data = {"target": "CPU", "usage": 45.5, "temp": 62.0, "clock": 3600}
serial_port.write(json.dumps(data).encode("utf-8") + b"\n")
```

### C# (envio)

```csharp
using System.Text.Json;

var dados = new SensorData { CT = 62, CU = 45, GT = 71, GU = 80 };
string jsonString = JsonSerializer.Serialize(dados);
portaSerial.WriteLine(jsonString);
```

### C/Embarcado (recepção)

- Byte-by-byte accumulation.
- Delimitador: `\n`.
- Parser: cJSON.
