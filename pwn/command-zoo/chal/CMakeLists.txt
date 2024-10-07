cmake_minimum_required(VERSION 3.29)
project(CommandZoo C)

set(CMAKE_C_STANDARD 11)

add_executable(CommandZoo main.c)

set(CMAKE_EXE_LINKER_FLAGS "-static")
