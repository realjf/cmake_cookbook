# 首先，设置cmake所需的最低版本，如果使用CMake版本低于该版本，则会发出致命错误
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)


# 第二行，声明项目的名称和支持的编程语言
project(recipe-03 LANGUAGES CXX)

# 创建目标——静态库
add_library(message STATIC Message.hpp Message.cpp)

# 指示CMake创建一个新目标：可执行文件 hello-world
add_executable(hello-world helloworld.cpp)

# 链接静态库到可执行目标
target_link_libraries(hello-world message)




