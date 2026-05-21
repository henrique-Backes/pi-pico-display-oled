# Protocolo de Comunicação JSON

A comunicação utiliza JSON para facilitar o parsing e a expansão futura. Cada mensagem terminará com `\n` (newline) para delimitar o fim do pacote na serial.

## 1. Envio: Info da CPU (PC -> Pico)

```json
{
  "target": "CPU",
  "usage": 45.5,
  "temp": 62.0,
  "clock": 3600
}
```

- **target** (string): `"CPU"`
- **usage** (float): Porcentagem de uso (0.0 a 100.0)
- **temp** (float): Temperatura em Celsius
- **clock** (int): Clock atual em MHz

## 2. Envio: Info da GPU (PC -> Pico)

```json
{
  "target": "GPU",
  "usage": 80.0,
  "temp": 71.0,
  "vram_used": 6.2,
  "vram_total": 8.0
}
```

- **target** (string): `"GPU"`
- **usage** (float): Porcentagem de uso (0.0 a 100.0)
- **temp** (float): Temperatura em Celsius
- **vram_used** (float): VRAM utilizada em GB
- **vram_total** (float): VRAM total em GB

## 3. Resposta (Pico -> PC)

O Pico responde automaticamente a cada pacote recebido.

**ACK (Sucesso)**

```json
{
  "status": "ACK",
  "msg": "CPU data updated"
}
```

**NACK (Falha)**

```json
{
  "status": "NACK",
  "msg": "JSON parse error"
}
```
