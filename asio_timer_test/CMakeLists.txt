cmake_minimum_required(VERSION 3.14)
project(asio_timer_test)

add_definitions(-DASIO_STANDALONE)
set(CMAKE_CXX_STANDARD 14)

add_executable(asio_timer_test main.cpp)