/** @file display.h
 *
 * @brief Driver para o display OLED SSD1306 via I2C.
 *
 * @par
 * Controle e renderizacao de dados no display OLED 128x64.
 * Interface I2C0 nos GPIOs 16 (SDA) e 17 (SCL) a 400kHz.
 */

#ifndef DISPLAY_H
#define DISPLAY_H

#include <stdint.h>
#include <stdbool.h>

/**
 * @brief Inicializa o hardware I2C e o display OLED SSD1306.
 *
 * Configura I2C0 nos GPIOs 16 (SDA) e 17 (SCL) a 400kHz,
 * e envia a sequencia de inicializacao do SSD1306.
 */
void
display_init(void);

/**
 * @brief Limpa todo o conteudo do display OLED.
 */
void
display_clear(void);

/**
 * @brief Exibe os dados de CPU no display OLED.
 *
 * @param[in] usage  Porcentagem de uso da CPU (0.0 a 100.0).
 * @param[in] temp   Temperatura da CPU em Celsius.
 * @param[in] clock  Clock atual da CPU em MHz.
 */
void
display_show_cpu(float usage, float temp, uint32_t clock);

/**
 * @brief Exibe os dados de GPU no display OLED.
 *
 * @param[in] usage      Porcentagem de uso da GPU (0.0 a 100.0).
 * @param[in] temp       Temperatura da GPU em Celsius.
 * @param[in] vram_used  VRAM utilizada em GB.
 * @param[in] vram_total VRAM total em GB.
 */
void
display_show_gpu(float usage, float temp, float vram_used,
                 float vram_total);

#endif /* DISPLAY_H */

/*** end of file ***/
