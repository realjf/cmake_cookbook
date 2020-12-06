## 处理与平台相关的源代码


### 准备
helloworld.cpp如下：
```cpp
#include <cstdlib>
#include <iostream>
#include <string>

std::string say_hello(){
    #ifdef IS_WINDOWS
    return std::string("Hello from Windows!");
    #elif IS_LINUX
    return std::string("Hello from Linux!");
    #elif IS_MACOS
    return std::string("Hello from macOS!");
    #else
    return std::string("Hello from an unknown system!");
    #endif
}

int main() {
    std::cout << say_hello() << std::endl;
    return EXIT_SUCCESS;
}

```
 ## 实现
 CMakeLists.txt内容如下：

 ```cmake
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)


project(recipe-02 LANGUAGES CXX)

add_executable(hello-world helloworld.cpp)


if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    target_compile_definitions(hello-world PUBLIC "IS_LINUX")
endif()

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    target_compile_definitions(hello-world PUBLIC "IS_MACOS")
endif()
if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    target_compile_definitions(hello-world PUBLIC "IS_WINDOWS")
endif()


 ```

### 工作原理

这些定义在CMakeLists.txt中配置时定义， 通过使用 target_compile_definition 在预处理阶段使用。 可以不重复 if-endif 语句， 以更紧凑的表达式实现， 我们将在下一个示例中演示这种重构方式。 也可以把 if-endif 语句加入到一个 if-else-else-endif 语句中。 这个阶段， 可以使用 add_definitions(-DIS_LINUX) 来设置定义(当然， 可以根据平台调整定义)， 而不是使用 target_compile_definition 。 使用 add_definitions 的缺点是， 会修改编译整个项目的定义， 而 target_compile_definitions 给我们机会， 将定义限制于一个特定的目标， 以及通过 PRIVATE|PUBLIC|INTERFACE 限定符， 限制这些定义可见性


- PRIVATE， 编译定义将只应用于给定的目标， 而不应用于相关的其他目标。
- INTERFACE， 对给定目标的编译定义将只应用于使用它的目标。
- PUBLIC， 编译定义将应用于给定的目标和使用它的所有其他目标



