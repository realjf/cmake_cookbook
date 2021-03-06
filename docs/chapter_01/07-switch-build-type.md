## 切换构建类型

CMake可以配置构建类型， 例如： Debug、 Release等。 配置时， 可以为Debug或Release构建设置相关的选项或属性， 例如： 编译器和链接器标志。 控制生成构建系统使用的配置变量是 CMAKE_BUILD_TYPE 。 该变量默认为空， CMake识别的值为

1. Debug： 用于在没有优化的情况下， 使用带有调试符号构建库或可执行文件。
2. Release： 用于构建的优化的库或可执行文件， 不包含调试符号。
3. RelWithDebInfo： 用于构建较少的优化库或可执行文件， 包含调试符号。
4. MinSizeRel： 用于不增加目标代码大小的优化方式， 来构建库或可执行文件。

### 准备
首先定义最低cmake版本、项目名称和支持的语言
```cmake
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
project(recipe-07 LANGUAGES C CXX)
```

然后，设置一个默认的构建类型，并打印一条消息。
```cmake
if(NOT CMAKE_BUILD_TYPE)
set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
```
最后，打印出cmake设置的相应编译标志：
```cmake
message(STATUS "C flags, Debug configuration: ${CMAKE_C_FLAGS_DEBUG}")
message(STATUS "C flags, Release configuration: ${CMAKE_C_FLAGS_RELEASE}")

message(STATUS "C flags, Release configuration with Debug info: ${CMAKE_C_FLAGS_RELWITHDEBINFO}")

message(STATUS "C flags, minimal Release configuration: ${CMAKE_C_FLAGS_MINSIZEREL}")

message(STATUS "C++ flags, Debug configuration: ${CMAKE_CXX_FLAGS_DEBUG}")

message(STATUS "C++ flags, Release configuration: ${CMAKE_CXX_FLAGS_RELEASE}")

message(STATUS "C++ flags, Release configuration with Debug info: ${CMAKE_CXX_FLAGS_RELWITHDEBINFO}")

message(STATUS "C++ flags, minimal Release configuration: ${CMAKE_CXX_FLAGS_MINSIZEREL}")
```
验证配置的输出
```sh
mkdir -p build
cd build
cmake ..
```
切换构建类型
```sh
cmake -D CMAKE_BUILD_TYPE=Debug ..
```

### 更多信息

对于单配置生成器， 如UnixMakefile、 MSYS Makefile或Ninja， 因为要对项目重新配置， 这里需要运行CMake两次。 不过，
CMake也支持复合配置生成器。 这些通常是集成开发环境提供的项目文件， 最显著的是Visual Studio和Xcode， 它们可以同时处理多个配置。 可以使用 CMAKE_CONFIGURATION_TYPES 变量可以对这些生成器的可用配置类型进行调整， 该变量将接受一个值列表


```sh
mkdir -p build
cd build

cmake .. -G"Visual Studio 12 2017 Win64" -D CMAKE_CONFIGURATION_TYPES="Release;Debug"
```
将为Release和Debug配置生成一个构建树。 然后， 您可以使 --config 标志来决定构建这两个中的哪一个
```sh
cmake --build . --config Release
```
