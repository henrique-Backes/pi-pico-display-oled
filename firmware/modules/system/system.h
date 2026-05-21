/** @file system.h
 *
 * @brief Modulo de orquestracao do sistema PC Monitor.
 *
 * @par
 * Controla a alternancia de tela (CPU/GPU a cada 3s),
 * armazena os dados recebidos e coordena Display e Protocol.
 */

#ifndef SYSTEM_H
#define SYSTEM_H

#include <stdint.h>
#include <stdbool.h>

/**
 * @brief Armazena os dados de CPU recebidos via protocolo.
 *
 * @param[in] usage  Porcentagem de uso da CPU (0.0 a 100.0).
 * @param[in] temp   Temperatura da CPU em Celsius.
 * @param[in] clock  Clock atual da CPU em MHz.
 */
void
system_set_cpu_data(float usage, float temp, uint32_t clock);

/**
 * @brief Armazena os dados de GPU recebidos via protocolo.
 *
 * @param[in] usage      Porcentagem de uso da GPU (0.0 a 100.0).
 * @param[in] temp       Temperatura da GPU em Celsius.
 * @param[in] vram_used  VRAM utilizada em GB.
 * @param[in] vram_total VRAM total em GB.
 */
void
system_set_gpu_data(float usage, float temp,
                    float vram_used, float vram_total);

/**
 * @brief Executa o ciclo de alternancia de tela.
 *
 * Deve ser chamada no loop principal. Verifica se
 * passaram-se 3 segundos desde a ultima troca e,
 * se sim, inverte a tela entre CPU e GPU.
 */
void
system_run(void);

#endif /* SYSTEM_H */

/*** end of file ***/
