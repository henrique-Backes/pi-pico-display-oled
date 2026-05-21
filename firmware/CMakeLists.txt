# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico
#  VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.2.0)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.2.0-a4)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
set(PICO_BOARD pico CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(display_oled C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# ------------------------------------------------------------------ #
#  cJSON (biblioteca de parsing JSON)                                 #
# ------------------------------------------------------------------ #

add_library(cJSON STATIC libs/cJSON/cJSON.c)
target_include_directories(cJSON PUBLIC libs/cJSON/)

# ------------------------------------------------------------------ #
#  Executavel principal                                               #
# ------------------------------------------------------------------ #

add_executable(display_oled display_oled.c)

target_sources(display_oled PRIVATE
    modules/display/display.c
    modules/protocol/protocol.c
    modules/system/system.c
)

target_include_directories(display_oled PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
    modules/display
    modules/protocol
    modules/system
)

target_link_libraries(display_oled
    pico_stdlib
    hardware_i2c
    cJSON
)

# USB CDC habilitado, UART desabilitado
pico_enable_stdio_usb(display_oled 1)
pico_enable_stdio_uart(display_oled 0)

pico_add_extra_outputs(display_oled)
