project(CBB_CP_TEST)

file(GLOB_RECURSE all_files
*.cpp
*.cc
*.c++
*.c
*.C)

add_executable(CBB_CP_TEST ${all_files})