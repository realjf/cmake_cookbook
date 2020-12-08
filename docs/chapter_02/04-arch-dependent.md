## 检测处理器体系架构


### 准备
arch-dependent.cpp代码示例如下：
```cpp
#include <cstdlib>
#include <iostream>
#include <string>

#define STRINGIFY(x) #x
#define TOSTRING(x) STRINGIFY(x)

std::string say_hello()
{
    std::string arch_info(TOSTRING(ARCHITECTURE));
    arch_info += std::string(" architecture. ");
#ifdef IS_32_BIT_ARCH
    return arch_info + std::string("Compiled on a 32 bit host processor.");
#elif IS_64_BIT_ARCH
    return arch_info + std::string("Compiled on a 64 bit host processor.");
#else
    return arch_info + std::string("Neither 32 nor 64 bit, puzzling ...");
#endif
}

int main()
{
    std::cout << say_hello() << std::endl;
    return EXIT_SUCCESS;
}


```
### 实现
CMakeLists.txt内容如下：
```cmake
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

```

最后构建并执行代码
```sh
mkdir -p build
cd build
cmake ..
cmake --build .
./arch-dependent
```
### 工作原理
CMake定义了CMAKE_HOST_SYSTEM_PROCESSOR变量，以包含当前运行的处理器的名称。可以设置为“i386,i686,x86_64,AMD64”等，
CMAKE_SIZEOF_VOID_P为void指针的大小。

> 使用CMAKE_SIZEOF_VOID_P是检查当前CPU是否具有32位或64位架构的唯一真正可移植的方法。

### 更多
除了CMAKE_HOST_SYSTEM_PROCESSOR外，CMake还定义了CMAKE_SYSTEM_PROCESSOR变量。前者包含当前运行的cpu在cmake的名称，
而后者将包含当前正在为其构建的cpu的名称。这是一个细微的差别，在交叉编译时起着非常重要的作用。


```cpp
#if defined(__i386) || defined(__i386__) || defined(_M_IX86)
#error cmake_arch i386
#elif defined(__x86_64) || defined(__x86_64__) || defined(__amd64) ||
defined(_M_X64)
#error cmake_arch x86_64
#endif
```
这种策略也是检测目标处理器体系结构的推荐策略， 因为CMake似乎没有提供可移植的内在解决方案。
另一种选择， 将只使用CMake， 完全不使用预处理器， 代价是为每种情况设置不同的源文件， 然后使
用 target_source 命令将其设置为可执行目标 arch-dependent 依赖的源文件

```cmake
add_executable(arch-dependent "")

if(CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "i386")
message(STATUS "i386 architecture detected")
target_sources(arch-dependent
PRIVATE
arch-dependent-i386.cpp
)
elseif(CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "i686")
message(STATUS "i686 architecture detected")
target_sources(arch-dependent
PRIVATE
arch-dependent-i686.cpp
)
elseif(CMAKE_HOST_SYSTEM_PROCESSOR MATCHES "x86_64")
message(STATUS "x86_64 architecture detected")
target_sources(arch-dependent
PRIVATE
arch-dependent-x86_64.cpp
)
else()
message(STATUS "host processor architecture is unknown")
endif()
```


