cmake_minimum_required(VERSION 3.21)
project(XOR_based_DNA_encoding)

set(CMAKE_CXX_STANDARD 23)

# Windows shared library fix. Only apply if output dirs haven't been set elsewhere (otherwise python bindings don't work).
# see: https://cmake.org/cmake/help/latest/guide/tutorial/Selecting%20Static%20or%20Shared%20Libraries.html
# and: https://cmake.org/pipermail/cmake/2016-April/063337.html
if (NOT CMAKE_RUNTIME_OUTPUT_DIRECTORY)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/bin")
endif ()
if (NOT CMAKE_LIBRARY_OUTPUT_DIRECTORY)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/lib")
endif ()
if (NOT CMAKE_ARCHIVE_OUTPUT_DIRECTORY)
    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/lib")
endif ()

set(LIB_NAME xor_code)
set(LIB_TESTS_NAME xor_code_tests)
set(LIB_EXAMPLE_NAME xor_code_run)

set(PYTHON_NAME xor_code_python)

add_subdirectory(cpp)
add_subdirectory(python)
