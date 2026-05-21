/** @file protocol.h
 *
 * @brief Protocolo de comunicacao JSON via USB Serial (CDC).
 *
 * @par
 * Le a USB Serial byte a byte, identifica o fim de pacote (\n),
 * parseia o JSON via cJSON e envia ACK/NACK de resposta.
 */

#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <stdint.h>
#include <stdbool.h>

/**
 * @brief Inicializa o modulo de protocolo (zera buffer interno).
 */
void
protocol_init(void);

/**
 * @brief Processa um byte recebido da USB Serial.
 *
 * Acumula os caracteres em um buffer estatico interno
 * ate encontrar o delimitador '\n'. Ao encontrar, faz
 * o parse do JSON e atualiza o modulo System.
 *
 * @param[in] byte Byte recebido da serial.
 */
void
protocol_process_byte(uint8_t byte);

/**
 * @brief Envia uma mensagem de ACK via USB Serial.
 *
 * @param[in] p_msg Mensagem descritiva do sucesso.
 */
void
protocol_send_ack(const char *p_msg);

/**
 * @brief Envia uma mensagem de NACK via USB Serial.
 *
 * @param[in] p_msg Mensagem descritiva do erro.
 */
void
protocol_send_nack(const char *p_msg);

#endif /* PROTOCOL_H */

/*** end of file ***/
