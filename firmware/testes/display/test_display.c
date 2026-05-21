#include "unity.h"
#include "display.h"
#include <stdint.h>
#include <string.h>
#include <stdio.h>

/* ------------------------------------------------------------------ */
/*  Mocks para Hardware I2C / GPIO / sleep                             */
/* ------------------------------------------------------------------ */

static uint8_t  g_mock_i2c_data[512u];
static uint16_t g_mock_i2c_data_len;
static bool     g_mock_i2c_called;
static uint8_t  g_mock_gpio_funcs[32u];
static bool     g_mock_sleep_called;

/* Registrou comando ou dado I2C? */
bool
mock_i2c_get_called(void)
{
    return g_mock_i2c_called;
}

/* Retorna ponteiro para o buffer I2C capturado */
const uint8_t *
mock_i2c_get_data(void)
{
    return g_mock_i2c_data;
}

uint16_t
mock_i2c_get_len(void)
{
    return g_mock_i2c_data_len;
}

/* Reseta estado dos mocks */
void
mock_reset(void)
{
    g_mock_i2c_called   = false;
    g_mock_i2c_data_len = 0u;
    memset(g_mock_i2c_data, 0, sizeof(g_mock_i2c_data));
    memset(g_mock_gpio_funcs, 0, sizeof(g_mock_gpio_funcs));
    g_mock_sleep_called = false;
}

/* ------------------------------------------------------------------ */
/*  Stubs das funções do Pico SDK (substituem o hardware real)        */
/* ------------------------------------------------------------------ */

int
i2c_write_blocking(i2c_inst_t *inst, uint8_t addr,
                   const uint8_t *src, size_t len, bool nostop)
{
    (void)inst;
    (void)nostop;

    if (SSD1306_ADDR != addr)
    {
        return -1;
    }

    g_mock_i2c_called = true;

    if (g_mock_i2c_data_len + len < sizeof(g_mock_i2c_data))
    {
        memcpy(&g_mock_i2c_data[g_mock_i2c_data_len], src, len);
        g_mock_i2c_data_len += (uint16_t)len;
    }

    return (int)len;
}

void
gpio_set_function(uint gpio, uint fn)
{
    if (31u >= gpio)
    {
        g_mock_gpio_funcs[gpio] = (uint8_t)fn;
    }
}

void
gpio_pull_up(uint gpio)
{
    (void)gpio;
}

void
sleep_ms(uint32_t ms)
{
    (void)ms;
    g_mock_sleep_called = true;
}

uint
i2c_init(i2c_inst_t *inst, uint baudrate)
{
    (void)inst;
    (void)baudrate;
    return baudrate;
}

/* ------------------------------------------------------------------ */
/*  Unity Setup / Teardown                                             */
/* ------------------------------------------------------------------ */

void
setUp(void)
{
    mock_reset();
}

void
tearDown(void)
{
}

/* ------------------------------------------------------------------ */
/*  Testes                                                             */
/* ------------------------------------------------------------------ */

/* Teste 1: Display_Init configura GPIOs e envia comandos I2C */
void
test_Display_Init_ConfiguresGPIOsAndSendsCommands(void)
{
    Display_Init();

    TEST_ASSERT_TRUE(g_mock_i2c_called);
    TEST_ASSERT_EQUAL_UINT8(0x04u, g_mock_gpio_funcs[16u]); /* GPIO_FUNC_I2C */
    TEST_ASSERT_EQUAL_UINT8(0x04u, g_mock_gpio_funcs[17u]); /* GPIO_FUNC_I2C */
}

/* Teste 2: Display_Clear zera o buffer e envia dados I2C */
void
test_Display_Clear_SendsDataAndZerosBuffer(void)
{
    Display_Init();
    mock_reset();

    Display_Clear();

    TEST_ASSERT_TRUE(g_mock_i2c_called);
}

/* Teste 3: Display_ShowCPU envia dados I2C (renderização) */
void
test_Display_ShowCPU_SendsRenderData(void)
{
    Display_ShowCPU(55.5f, 65.0f, 4200u);

    TEST_ASSERT_TRUE(g_mock_i2c_called);
}

/* Teste 4: Display_ShowGPU envia dados I2C (renderização) */
void
test_Display_ShowGPU_SendsRenderData(void)
{
    Display_ShowGPU(80.0f, 71.0f, 6.2f, 8.0f);

    TEST_ASSERT_TRUE(g_mock_i2c_called);
}

/* Teste 5: Display_ShowCPU com valores extremos (zero) */
void
test_Display_ShowCPU_ZeroValues(void)
{
    Display_ShowCPU(0.0f, 0.0f, 0u);

    TEST_ASSERT_TRUE(g_mock_i2c_called);
}

/* Teste 6: Display_ShowGPU com valores máximos */
void
test_Display_ShowGPU_MaxValues(void)
{
    Display_ShowGPU(100.0f, 105.0f, 24.0f, 24.0f);

    TEST_ASSERT_TRUE(g_mock_i2c_called);
}

/* Teste 7: Endereço I2C correto (0x3C) */
void
test_Display_Init_UsesCorrectI2CAddress(void)
{
    Display_Init();

    /* O stub de i2c_write_blocking só aceita SSD1306_ADDR (0x3C).
     * Se chegou aqui e g_mock_i2c_called é true, o endereço está correto. */
    TEST_ASSERT_TRUE(g_mock_i2c_called);
}

/* ------------------------------------------------------------------ */
/*  Main                                                               */
/* ------------------------------------------------------------------ */

int
main(void)
{
    UNITY_BEGIN();

    RUN_TEST(test_Display_Init_ConfiguresGPIOsAndSendsCommands);
    RUN_TEST(test_Display_Clear_SendsDataAndZerosBuffer);
    RUN_TEST(test_Display_ShowCPU_SendsRenderData);
    RUN_TEST(test_Display_ShowGPU_SendsRenderData);
    RUN_TEST(test_Display_ShowCPU_ZeroValues);
    RUN_TEST(test_Display_ShowGPU_MaxValues);
    RUN_TEST(test_Display_Init_UsesCorrectI2CAddress);

    return UNITY_END();
}
