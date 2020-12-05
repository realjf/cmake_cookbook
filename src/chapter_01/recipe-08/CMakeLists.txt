cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(recipe-08 LANGUAGES CXX)

# 打印当前编译器标志
message("C++ compiler flags: ${CMAKE_CXX_FLAGS}")

# 准备了标志列表
list(APPEND flags "-fPIC" "-Wall")
if(NOT WIN32)
    list(APPEND flags "-Wextra" "-Wpedantic")
endif()

# 添加一个新的目标 geometry库，并列出它的源依赖关系
add_library(geometry STATIC
    geometry_circle.cpp
    geometry_circle.hpp
    geometry_polygon.cpp
    geometry_polygon.hpp
    geometry_rhombus.cpp
    geometry_rhombus.hpp
    geometry_square.cpp
    geometry_square.hpp
)

# 为这个库目标设置编译选项
target_compile_options(geometry PRIVATE ${flags})

# 生成compute-areas可执行文件作为一个目标
add_executable(compute-areas compute-areas.cpp)


# 还为可执行目标设置了编译选项
target_compile_options(compute-areas PRIVATE "-fPIC")

# 将可执行文件链接到geometry库
target_link_libraries(compute-areas geometry)
