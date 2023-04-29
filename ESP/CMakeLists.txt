cmake_minimum_required(VERSION 3.0)

project(my_project)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(HTTP_in_C HTTP_in_C.c)

target_include_directories(HTTP_in_C PRIVATE ${PROJECT_SOURCE_DIR}/include)
target_link_libraries(HTTP_in_C PRIVATE curl)