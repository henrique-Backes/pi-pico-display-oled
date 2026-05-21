# Módulo: Protocolo

## 1. Responsabilidade

Ler a USB Serial (CDC) byte a byte, identificar o fim de pacote (`\n`), parsear o JSON usando cJSON e disparar o envio de ACK/NACK.

## 2. Interface (protocol.h)

```c
#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <stdint.h>

void Protocol_Init(void);
void Protocol_ProcessByte(uint8_t byte);
void Protocol_SendACK(const char *msg);
void Protocol_SendNACK(const char *msg);

#endif /* PROTOCOL_H */
```

## 3. Guia de Desenvolvimento

- **`Protocol_ProcessByte()`**: Acumula os caracteres em um buffer estático interno até encontrar `\n`. Ao encontrar, adiciona `\0`, chama a função de parsing e reseta o buffer.
- **Parsing**: Usar `cJSON_Parse()`. Se retornar `NULL`, chamar `Protocol_SendNACK("JSON parse error")`.
- **Extração**: Usar `cJSON_GetObjectItem()`. Se o campo `"target"` for `"CPU"`, extrair os dados e chamar `System_SetCPUData()`. Se for `"GPU"`, chamar `System_SetGPUData()`.
- **Resposta**: Montar o JSON de ACK/NACK usando `cJSON_CreateObject()`, imprimir em string com `cJSON_PrintUnformatted()`, enviar via `printf()` (que vai para a USB CDC) e liberar memória com `cJSON_Delete()` e `cJSON_Free()`.
