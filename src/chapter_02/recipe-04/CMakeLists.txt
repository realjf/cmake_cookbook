cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(recipe-04 LANGUAGES CXX)

add_executable(arch-dependent arch-dependent.cpp)

# 检查空指针类型的大小，CMAKE的CMAKE_SIZEOF_VOID_P变量会告诉我们CPU是32位还是64位
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    target_compile_definitions(arch-dependent PUBLIC "IS_64_BIT_ARCH")
    message(STATUS "Target is 64 bits")
else()
    target_compile_definitions(arch-dependent PUBLIC "IS_32_BIT_ARCH")
    message(STATUS "Target is 32 bits")
endif()

# 通过定义以下目标编译定义，让预处理器了解主机处理器架构，同时在配置过程中打印状态消息：
if(CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "i386")
    message(STATUS "i386 architecture detected")
elseif(CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "i686")
    message(STATUS "i686 architecture detected")
elseif(CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "x86_64")
    message(STATUS "x86_64 architecture detected")
else()
    message(STATUS "host processor architecture is unknown")
endif()
target_compile_definitions(arch-dependent PUBLIC "ARCHITECTURE=${CMAKE_HOST_SYSTEM_PROCESSOR}")



