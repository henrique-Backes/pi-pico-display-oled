/** @file display_oled.c
 *
 * @brief PC Monitor via Raspberry Pi Pico - Arquivo principal.
 *
 * @par
 * Ponto de entrada do firmware. Inicializa os modulos Display,
 * Protocol e System, e executa o loop principal que le bytes
 * da USB Serial (CDC) e alterna as telas de CPU/GPU.
 */

#include <stdint.h>
#include <stdbool.h>
#include "pico/stdlib.h"
#include "display.h"
#include "protocol.h"
#include "system.h"

/* ------------------------------------------------------------------ */
/*  Funcao Principal                                                   */
/* ------------------------------------------------------------------ */

int
main(void)
{
    int byte_in;

    stdio_init_all();

    display_init();
    protocol_init();

    display_show_cpu(0.0f, 0.0f, 0u);

    for (;;)
    {
        byte_in = getchar_timeout_us(0);

        if (PICO_ERROR_TIMEOUT != byte_in)
        {
            protocol_process_byte((uint8_t)byte_in);
        }

        system_run();
    }

    return 0;
}

/*** end of file ***/
