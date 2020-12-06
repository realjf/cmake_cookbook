## 构建和链接静态库和动态库

### 准备

```sh
mkdir -p recipe-03

```
在项目根目录下创建源程序helloworld.cpp和CMakeLists.txt文件，还有一个Message.hpp头文件及Message.cpp文件

helloworld.cpp文件内容如下：
```cpp
#include "Message.hpp"
#include <cstdlib>
#include <iostream>

int main()
{
    Message say_hello("Hello, CMake World!");
    std::cout << say_hello << std::endl;

    Message say_goodbye("Goodbye, CMake World");
    std::cout << say_goodbye << std::endl;

    return EXIT_SUCCESS;
}

```

Message.hpp文件内容如下：
```cpp
#pragma once

#include <iosfwd>
#include <string>

class Message {
public:
    Message(const std::string &m) : message_(m) {}
    friend std::ostream &operator<<(std::ostream &os, Message &obj){
        return obj.printObject(os);
    }
private:
    std::string message_;
    std::ostream &printObject(std::ostream &os);
};


```
Message.cpp文件内容如下：

```cpp
#include "Message.hpp"

#include <iostream>
#include <string>

std::ostream &Message::printObject(std::ostream &os){
    os <<"This is my very nice message: " << std::endl;
    os << message_;
    return os;
}
```

CMakeLists.txt文件内容如下：
```cmake
# 首先，设置cmake所需的最低版本，如果使用CMake版本低于该版本，则会发出致命错误
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)


# 第二行，声明项目的名称和支持的编程语言
project(recipe-01 LANGUAGES CXX)

# 创建目标——静态库
add_library(message STATIC Message.hpp Message.cpp)

# 指示CMake创建一个新目标：可执行文件 hello-world
add_executable(hello-world helloworld.cpp)

# 链接静态库到可执行目标
target_link_libraries(hello-world message)
```

这里在第2小节基础上作了修改，创建了静态库message，并在最后链接到可执行目标hello-world中

### 构建
```sh
mkdir -p build
cd build
cmake ..
cmake --build .

Scanning dependencies of target message
[ 25%] Building CXX object CMakeFiles/message.dir/Message.cpp.o
[ 50%] Linking CXX static library libmessage.a
[ 50%] Built target message
Scanning dependencies of target hello-world
[ 75%] Building CXX object CMakeFiles/hello-world.dir/helloworld.cpp.o
[100%] Linking CXX executable hello-world
[100%] Built target hello-world
```

### 工作原理
本节引入两个新命令

- add_library(message STATIC Message.hpp Message.cpp) ： 生成必要的构建指令， 将指定的源码编译到库中。 add_library 的第一个参数是目标名。 整个 CMakeLists.txt 中， 可使用相同的名称来引用库。 生成的库的实际名称将由CMake通过在前面添加前缀 lib 和适当的扩展名作为后缀来形成。 生成库是根据第二个参数( STATIC 或 SHARED )和操作系统确定的。
- target_link_libraries(hello-world message) : 将库链接到可执行文件。 此命令还确保 hello-world 可执行文件可以正确地依赖于消息库。 因此， 在消息库链接到 hello-world 可执行文件之前， 需要完成消息库的构建


编译成功后，构建目录包含libmessage.a一个静态库和hello-world可执行文件

cmake接受其他值作为add_library的第二个参数的有效值，如：

- STATIC： 用于创建静态库， 即编译文件的打包存档， 以便在链接其他目标时使用， 例如： 可执行文件。
- SHARED： 用于创建动态库， 即可以动态链接， 并在运行时加载的库。 可以
在 CMakeLists.txt 中使用 add_library(message SHARED Message.hpp Message.cpp) 从静态库切换到动态共享对象(DSO)。
- OBJECT： 可将给定 add_library 的列表中的源码编译到目标文件， 不将它们归档到静态库中，也不能将它们链接到共享对象中。 如果需要一次性创建静态库和动态库， 那么使用对象库尤其有用。 我们将在本示例中演示。
- MODULE： 又为DSO组。 与 SHARED 库不同， 它们不链接到项目中的任何目标， 不过可以进行动态加载。 该参数可以用于构建运行时插件

CMake还能够生成特殊类型的库， 这不会在构建系统中产生输出， 但是对于组织目标之间的依赖关系，
和构建需求非常有用：

- IMPORTED： 此类库目标表示位于项目外部的库。 此类库的主要用途是， 对现有依赖项进行构建。因此， IMPORTED 库将被视为不可变的。 我们将在本书的其他章节演示使用 IMPORTED 库的示例。 参见:
https://cmake.org/cmake/help/latest/manual/cmakebuildsystem.7.html#impo
rted-targets
- INTERFACE： 与 IMPORTED 库类似。 不过， 该类型库可变， 没有位置信息。 它主要用于项目之外的目标构建使用。 我们将在本章第5节中演示 INTERFACE 库的示例。 参见:
https://cmake.org/cmake/help/latest/manual/cmakebuildsystem.7.html#interface-libraries
- ALIAS： 顾名思义， 这种库为项目中已存在的库目标定义别名。 不过， 不能为 IMPORTED 库选择别名。 参见: https://cmake.org/cmake/help/latest/manual/cmakebuildsystem.7.html#alias-libraries


本例中， 我们使用 add_library 直接集合了源代码。 后面的章节中， 我们将使
用 target_sources 汇集源码， 特别是在第7章



### 更多

OBJECT库的使用，修改CMakeLists.txt，如下：

```cmake
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
project(recipe-03 LANGUAGES CXX)

add_library(message-objs
OBJECT
Message.hpp
Message.cpp
)

# this is only needed for older compilers
# but doesn't hurt either to have it
set_target_properties(message-objs
PROPERTIES
POSITION_INDEPENDENT_CODE 1
)

add_library(message-shared
SHARED
$<TARGET_OBJECTS:message-objs>
)

add_library(message-static
STATIC
$<TARGET_OBJECTS:message-objs>
)

add_executable(hello-world hello-world.cpp)

target_link_libraries(hello-world message-static)
```

首先， add_library 改为 add_library(Message-objs OBJECT Message.hpp Message.cpp) 。此外， 需要保证编译的目标文件与生成位置无关。 可以通过使用 set_target_properties 命令， 设置 message-objs 目标的相应属性来实现

> 可能在某些平台和/或使用较老的编译器上， 需要显式地为目标设置 POSITION_INDEPENDENT_CODE 属性

现在， 可以使用这个对象库来获取静态库( message-static )和动态库( message-shared )。 要注意引用对象库的生成器表达式语法: $<TARGET_OBJECTS:message-objs> 。 生成器表达式是CMake在生成时(即配置之后)构造， 用于生成特定于配置的构建输出。 

最后， 将 hello-world 可执行文件链接到消息库的静态版本。

是否可以让CMake生成同名的两个库？ 换句话说， 它们都可以被称为 message ， 而不是 message-static 和 message-share d吗？ 我们需要修改这两个目标的属性：

```cmake
add_library(message-shared SHARED $<TARGET_OBJECTS:message-objs>)

set_target_properties(message-shared PROPERTIES OUTPUT_NAME "message")

add_library(message-static STATIC $<TARGET_OBJECTS:message-objs>)

set_target_properties(message-static PROPERTIES OUTPUT_NAME "message")

```




