
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


