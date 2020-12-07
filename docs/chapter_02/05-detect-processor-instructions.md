## 检测处理器指令集

### 准备
processor-info.cpp内容如下:
```cpp
#include "config.h"

#include <cstdlib>
#include <iostream>

using namespace std;

int main() {
  cout << "Number of logical cores: " << NUMBER_OF_LOGICAL_CORES << endl;
  cout << "Number of physical cores: " << NUMBER_OF_PHYSICAL_CORES << endl;

  cout << "Total virtual memory in megabytes: " << TOTAL_VIRTUAL_MEMORY
            << endl;
  cout << "Available virtual memory in megabytes: " << AVAILABLE_VIRTUAL_MEMORY
            << endl;
  cout << "Total physical memory in megabytes: " << TOTAL_PHYSICAL_MEMORY
            << endl;
  cout << "Available physical memory in megabytes: "
            << AVAILABLE_PHYSICAL_MEMORY << endl;

  cout << "Processor is 64Bit: " << IS_64BIT << endl;
  cout << "Processor has floating point unit: " << HAS_FPU << endl;
  cout << "Processor supports MMX instructions: " << HAS_MMX << endl;
  cout << "Processor supports Ext. MMX instructions: " << HAS_MMX_PLUS
            << endl;
  cout << "Processor supports SSE instructions: " << HAS_SSE << endl;
  cout << "Processor supports SSE2 instructions: " << HAS_SSE2 << endl;
  cout << "Processor supports SSE FP instructions: " << HAS_SSE_FP << endl;
  cout << "Processor supports SSE MMX instructions: " << HAS_SSE_MMX
            << endl;
  cout << "Processor supports 3DNow instructions: " << HAS_AMD_3DNOW
            << endl;
  cout << "Processor supports 3DNow+ instructions: " << HAS_AMD_3DNOW_PLUS
            << endl;
  cout << "IA64 processor emulating x86 : " << HAS_IA64 << endl;

  cout << "OS name: " << OS_NAME << endl;
  cout << "OS sub-type: " << OS_RELEASE << endl;
  cout << "OS build ID: " << OS_VERSION << endl;
  cout << "OS platform: " << OS_PLATFORM << endl;

  return EXIT_SUCCESS;
}
```
config.h文件我们将使用config.h.in来生成，config.h.in的内容如下：
```hpp
#pragma once

#define NUMBER_OF_LOGICAL_CORES   @_NUMBER_OF_LOGICAL_CORES@
#define NUMBER_OF_PHYSICAL_CORES  @_NUMBER_OF_PHYSICAL_CORES@
#define TOTAL_VIRTUAL_MEMORY      @_TOTAL_VIRTUAL_MEMORY@
#define AVAILABLE_VIRTUAL_MEMORY  @_AVAILABLE_VIRTUAL_MEMORY@
#define TOTAL_PHYSICAL_MEMORY     @_TOTAL_PHYSICAL_MEMORY@
#define AVAILABLE_PHYSICAL_MEMORY @_AVAILABLE_PHYSICAL_MEMORY@
#define IS_64BIT                  @_IS_64BIT@
#define HAS_FPU                   @_HAS_FPU@
#define HAS_MMX                   @_HAS_MMX@
#define HAS_MMX_PLUS              @_HAS_MMX_PLUS@
#define HAS_SSE                   @_HAS_SSE@
#define HAS_SSE2                  @_HAS_SSE2@
#define HAS_SSE_FP                @_HAS_SSE_FP@
#define HAS_SSE_MMX               @_HAS_SSE_MMX@
#define HAS_AMD_3DNOW             @_HAS_AMD_3DNOW@
#define HAS_AMD_3DNOW_PLUS        @_HAS_AMD_3DNOW_PLUS@
#define HAS_IA64                  @_HAS_IA64@
#define OS_NAME                  "@_OS_NAME@"
#define OS_RELEASE               "@_OS_RELEASE@"
#define OS_VERSION               "@_OS_VERSION@"
#define OS_PLATFORM              "@_OS_PLATFORM@"

```

### 实现

CMakeLists.txt内容如下:
```cmake
# set minimum cmake version
cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

# project name and language
project(recipe-05 LANGUAGES CXX)

# define executable
add_executable(processor-info "")

# and its source file
target_sources(processor-info
  PRIVATE
    processor-info.cpp
  )

# and its include directories
target_include_directories(processor-info
  PRIVATE
    ${PROJECT_BINARY_DIR}
  )

# 查询主机系统的信息
foreach(key
  IN ITEMS
    NUMBER_OF_LOGICAL_CORES
    NUMBER_OF_PHYSICAL_CORES
    TOTAL_VIRTUAL_MEMORY
    AVAILABLE_VIRTUAL_MEMORY
    TOTAL_PHYSICAL_MEMORY
    AVAILABLE_PHYSICAL_MEMORY
    IS_64BIT
    HAS_FPU
    HAS_MMX
    HAS_MMX_PLUS
    HAS_SSE
    HAS_SSE2
    HAS_SSE_FP
    HAS_SSE_MMX
    HAS_AMD_3DNOW
    HAS_AMD_3DNOW_PLUS
    HAS_IA64
    OS_NAME
    OS_RELEASE
    OS_VERSION
    OS_PLATFORM
  )
  cmake_host_system_information(RESULT _${key} QUERY ${key})
endforeach()

# 定义了相应的变量后，配置config.h
configure_file(config.h.in config.h @ONLY)

```

### 工作原理
CMakeLists.txt中的foreach循环会查询多个键值，并定义相应的变量。cmake_host_system_information查询运行CMake的主机
系统的系统信息。此配置使用configure_file命令将config.h.in中的占位符配置成相应的键值，并生成config.h文件。

### 更多




