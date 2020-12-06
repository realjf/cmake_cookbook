
## 用条件句控制编译

本节中， 我们将探索条件结构 if-else- else-endif 的使用


### 准备
基于第3小节代码，我们作如下修改


1. 将Message.hpp和Message.cpp构建成一个库（静态或动态），然后将生成库链接到hello-world可执行文件中。
2. 将Message.hpp，Message.cpp和hello-world.cpp构建成一个可执行文件，但不生成任何一个库

CMakeLists.txt文件内容如下：

```cmake

# 首先定义cmake最低版本、项目名称和支持语言
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(recipe-04 LANGUAGES CXX)


# 引入新变量USE_LIBRARY，这是一个逻辑变量，值为OFF，我们还打印了它的值
set(USE_LIBRARY OFF)

message(STATUS "Compile sources into a library? ${USE_LIBRARY}")

# CMake中定义BUILD_SHARED_LIBS全局变量，并设置为OFF，调用add_library并省略第二个参数，将构建一个静态库
set(BUILD_SHARED_LIBS OFF)

# 然后，引入一个变量_sources，包括Message.hpp和Message.cpp：
list(APPEND _sources Message.hpp Message.cpp)

# 然后，引入一个基于USE_LIBRARY值的if-else语句，如果逻辑为真，则Message.hpp和Message.cpp将打包成一个库：
if(USE_LIBRARY)
    # add_library will create a static library
    # since BUILD_SHARED_LIBS is OFF
    add_library(message ${_sources})
    add_executable(hello-world helloworld.cpp)
    target_link_libraries(hello-world message)
else()
    add_executable(hello-world helloworld.cpp ${_sources})
endif()

# 由于USE_LIBRARY为OFF，hello-world可执行文件将使用所有源文件来编译。可通过objdump -x命令进行验证

```

### 工作原理

我们介绍了两个变量： USE_LIBRARY 和 BUILD_SHARED_LIBS 。 这两个变量都设置为 OFF 。 如CMake语言文档中描述， 逻辑真或假可以用多种方式表示


- 如果将逻辑变量设置为以下任意一种： 1 、 ON 、 YES 、 true 、 Y 或非零数， 则逻辑变量为 true 。
- 如果将逻辑变量设置为以下任意一种： 0 、 OFF 、 NO 、 false 、 N 、 IGNORE、
NOTFOUND 、 空字符串， 或者以 -NOTFOUND 为后缀， 则逻辑变量为 false 

USE_LIBRARY 变量将在第一个和第二个行为之间切换。 BUILD_SHARED_LIBS 是CMake的一个全局标志。 因为CMake内部要查询 BUILD_SHARED_LIBS 全局变量， 所以 add_library 命令可以在不传递 STATIC/SHARED/OBJECT 参数的情况下调用； 如果为 false 或未定义， 将生成一个静态库


> else() 和 endif() 中的 () ， 可能会让刚开始学习CMake代码的同学感到惊讶。 其历史
原因是， 因为其能够指出指令的作用范围。 例如， 可以使用 if(USE_LIBRARY)…else(USE_LIBRARY)…endif(USE_LIBIRAY) 。 这个格式并不唯一， 可以根据个人喜好来决定使用哪种格式

> _sources 变量是一个局部变量， 不应该在当前范围之外使用， 可以在名称前加下划线。

