/** @file protocol.c
 *
 * @brief Protocolo de comunicacao JSON via USB Serial (CDC).
 *
 * @par
 * Implementacao do parsing de pacotes JSON recebidos pela
 * USB Serial, utilizando a biblioteca cJSON. Responde com
 * ACK ou NACK conforme o resultado do parse.
 */

#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "protocol.h"
#include "system.h"
#include "cJSON.h"

/* ------------------------------------------------------------------ */
/*  Constantes Internas                                                */
/* ------------------------------------------------------------------ */

#define PROTOCOL_BUF_SIZE    256u
#define PROTOCOL_TARGET_CPU  "CPU"
#define PROTOCOL_TARGET_GPU  "GPU"

/* ------------------------------------------------------------------ */
/*  Variaveis Globais de Arquivo                                       */
/* ------------------------------------------------------------------ */

static uint8_t  g_rx_buf[PROTOCOL_BUF_SIZE];
static uint16_t g_rx_len;

/* ------------------------------------------------------------------ */
/*  Prototipos de Funcoes Privadas                                     */
/* ------------------------------------------------------------------ */

static void protocol_parse_json(void);

/* ------------------------------------------------------------------ */
/*  Funcoes Privadas                                                   */
/* ------------------------------------------------------------------ */

/*!
 * @brief Faz o parse do buffer interno como JSON e
 *        atualiza o modulo System conforme o target.
 */
static void
protocol_parse_json(void)
{
    const cJSON *p_root     = NULL;
    const cJSON *p_target   = NULL;
    const cJSON *p_usage    = NULL;
    const cJSON *p_temp     = NULL;
    const cJSON *p_clock    = NULL;
    const cJSON *p_vram_use = NULL;
    const cJSON *p_vram_tot = NULL;
    const char  *p_str      = NULL;

    // Garante terminacao nula do buffer.
    g_rx_buf[g_rx_len] = '\0';

    p_root = cJSON_Parse((const char *)g_rx_buf);
    if (NULL == p_root)
    {
        protocol_send_nack("JSON parse error");
        return;
    }

    p_target = cJSON_GetObjectItem(p_root, "target");
    if (NULL == p_target)
    {
        protocol_send_nack("Missing target field");
        cJSON_Delete((cJSON *)p_root);
        return;
    }

    p_str = p_target->valuestring;
    if (NULL == p_str)
    {
        protocol_send_nack("Target is not a string");
        cJSON_Delete((cJSON *)p_root);
        return;
    }

    if (0u == strcmp(p_str, PROTOCOL_TARGET_CPU))
    {
        p_usage = cJSON_GetObjectItem(p_root, "usage");
        p_temp  = cJSON_GetObjectItem(p_root, "temp");
        p_clock = cJSON_GetObjectItem(p_root, "clock");

        if ((NULL == p_usage) || (NULL == p_temp)
            || (NULL == p_clock))
        {
            protocol_send_nack("Missing CPU fields");
            cJSON_Delete((cJSON *)p_root);
            return;
        }

        system_set_cpu_data(
            (float)p_usage->valuedouble,
            (float)p_temp->valuedouble,
            (uint32_t)p_clock->valueint);

        protocol_send_ack("CPU data updated");
    }
    else if (0u == strcmp(p_str, PROTOCOL_TARGET_GPU))
    {
        p_usage    = cJSON_GetObjectItem(p_root, "usage");
        p_temp     = cJSON_GetObjectItem(p_root, "temp");
        p_vram_use = cJSON_GetObjectItem(p_root, "vram_used");
        p_vram_tot = cJSON_GetObjectItem(p_root, "vram_total");

        if ((NULL == p_usage) || (NULL == p_temp)
            || (NULL == p_vram_use) || (NULL == p_vram_tot))
        {
            protocol_send_nack("Missing GPU fields");
            cJSON_Delete((cJSON *)p_root);
            return;
        }

        system_set_gpu_data(
            (float)p_usage->valuedouble,
            (float)p_temp->valuedouble,
            (float)p_vram_use->valuedouble,
            (float)p_vram_tot->valuedouble);

        protocol_send_ack("GPU data updated");
    }
    else
    {
        protocol_send_nack("Unknown target");
    }

    cJSON_Delete((cJSON *)p_root);
}

/* ------------------------------------------------------------------ */
/*  Funcoes Publicas                                                   */
/* ------------------------------------------------------------------ */

void
protocol_init(void)
{
    memset(g_rx_buf, 0, sizeof(g_rx_buf));
    g_rx_len = 0u;
}

void
protocol_process_byte(uint8_t byte)
{
    if (g_rx_len >= (PROTOCOL_BUF_SIZE - 1u))
    {
        // Buffer cheio: descarta e reseta.
        protocol_send_nack("Buffer overflow");
        g_rx_len = 0u;
        return;
    }

    if ('\n' == (char)byte)
    {
        // Fim do pacote: parseia e reseta o buffer.
        protocol_parse_json();
        g_rx_len = 0u;
        return;
    }

    g_rx_buf[g_rx_len] = byte;
    g_rx_len++;
}

void
protocol_send_ack(const char *p_msg)
{
    cJSON *p_root  = NULL;
    char  *p_str   = NULL;

    if (NULL == p_msg)
    {
        return;
    }

    p_root = cJSON_CreateObject();
    if (NULL == p_root)
    {
        return;
    }

    cJSON_AddStringToObject(p_root, "status", "ACK");
    cJSON_AddStringToObject(p_root, "msg", p_msg);

    p_str = cJSON_PrintUnformatted(p_root);
    if (NULL != p_str)
    {
        printf("%s\n", p_str);
        cJSON_free(p_str);
    }

    cJSON_Delete(p_root);
}

void
protocol_send_nack(const char *p_msg)
{
    cJSON *p_root = NULL;
    char  *p_str  = NULL;

    if (NULL == p_msg)
    {
        return;
    }

    p_root = cJSON_CreateObject();
    if (NULL == p_root)
    {
        return;
    }

    cJSON_AddStringToObject(p_root, "status", "NACK");
    cJSON_AddStringToObject(p_root, "msg", p_msg);

    p_str = cJSON_PrintUnformatted(p_root);
    if (NULL != p_str)
    {
        printf("%s\n", p_str);
        cJSON_free(p_str);
    }

    cJSON_Delete(p_root);
}

/*** end of file ***/
