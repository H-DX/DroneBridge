cmake_minimum_required(VERSION 3.3)
project(rc_gpio_map)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "-O3") ## Optimize

set(SOURCE_FILES rc_gpio_map.c)
if (EXISTS "../../common db_common")
    add_subdirectory(../../common db_common)
elseif(EXISTS "/root/dronebridge/common")
    add_subdirectory(/root/dronebridge/common db_common)
    add_compile_definitions(USE_PI_INSTALL_PATH)
endif ()

add_executable(rc_gpio_map ${SOURCE_FILES})
target_link_libraries(rc_gpio_map db_common wiringPi)
