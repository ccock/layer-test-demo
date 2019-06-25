project(CBB_DP_TEST)

file(GLOB_RECURSE all_files
*.cpp
*.cc
*.c++
*.c
*.C)

add_executable(CBB_DP_TEST ${all_files})