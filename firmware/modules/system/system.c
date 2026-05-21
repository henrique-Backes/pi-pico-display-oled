/** @file system.c
 *
 * @brief Modulo de orquestracao do sistema PC Monitor.
 *
 * @par
 * Implementacao da alternancia de tela (CPU/GPU a cada 3s),
 * armazenamento dos dados recebidos e coordenacao entre
 * os modulos Display e Protocol.
 */

#include <stdint.h>
#include <stdbool.h>
#include "system.h"
#include "display.h"
#include "pico/stdlib.h"

/* ------------------------------------------------------------------ */
/*  Constantes Internas                                                */
/* ------------------------------------------------------------------ */

#define SYSTEM_SCREEN_TOGGLE_MS  3000u

/* ------------------------------------------------------------------ */
/*  Tipos Internos                                                     */
/* ------------------------------------------------------------------ */

typedef struct
{
    float    usage;
    float    temp;
    uint32_t clock;
} cpu_data_t;

typedef struct
{
    float usage;
    float temp;
    float vram_used;
    float vram_total;
} gpu_data_t;

/* ------------------------------------------------------------------ */
/*  Variaveis Globais de Arquivo                                       */
/* ------------------------------------------------------------------ */

static cpu_data_t g_cpu;
static gpu_data_t g_gpu;
static bool       g_b_screen_is_cpu;
static uint32_t   g_last_toggle_ms;

/* ------------------------------------------------------------------ */
/*  Funcoes Publicas                                                   */
/* ------------------------------------------------------------------ */

void
system_set_cpu_data(float usage, float temp, uint32_t clock)
{
    g_cpu.usage = usage;
    g_cpu.temp  = temp;
    g_cpu.clock = clock;
}

void
system_set_gpu_data(float usage, float temp,
                    float vram_used, float vram_total)
{
    g_gpu.usage      = usage;
    g_gpu.temp       = temp;
    g_gpu.vram_used  = vram_used;
    g_gpu.vram_total = vram_total;
}

void
system_run(void)
{
    uint32_t now_ms;
    uint32_t elapsed_ms;

    now_ms = to_ms_since_boot(get_absolute_time());
    elapsed_ms = now_ms - g_last_toggle_ms;

    if (elapsed_ms < SYSTEM_SCREEN_TOGGLE_MS)
    {
        return;
    }

    g_last_toggle_ms = now_ms;

    if (g_b_screen_is_cpu)
    {
        display_show_cpu(g_cpu.usage, g_cpu.temp, g_cpu.clock);
    }
    else
    {
        display_show_gpu(g_gpu.usage, g_gpu.temp,
                         g_gpu.vram_used, g_gpu.vram_total);
    }

    g_b_screen_is_cpu = !g_b_screen_is_cpu;
}

/*** end of file ***/
