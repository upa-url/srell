cmake_minimum_required(VERSION 3.7...3.13)

# Require C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Project settings
project(test-srell LANGUAGES CXX)

add_executable(conftest srell-src/misc/conftest.cpp)

# Testing
enable_testing()

foreach(test_arg utf8 utf16 utf32 utf8c)
  add_test(NAME conftest-${test_arg}
    COMMAND ${CMAKE_CURRENT_BINARY_DIR}/conftest ${test_arg})
endforeach()
