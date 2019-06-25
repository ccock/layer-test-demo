cmake_minimum_required(VERSION 2.8)

project(Test)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-invalid-offsetof -g -std=c++1y")

add_subdirectory(CBB_CP)
add_subdirectory(CBB_DP)