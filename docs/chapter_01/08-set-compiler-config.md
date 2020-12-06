## 设置编译器选项


CMake为调整或扩展编译器标志提供了很大的灵活性， 您可以选择下面两种方法:

- CMake将编译选项视为目标属性。 因此， 可以根据每个目标设置编译选项， 而不需要覆盖CMake默认值。
- 可以使用 -D CLI标志直接修改 CMAKE_<LANG>_FLAGS_<CONFIG> 变量。 这将影响项目中的所有目标， 并覆盖或扩展CMake默认值。

### 准备

编写一个示例程序，计算不同几何形状的面积，computer_area.cpp，及其他文件可参考源代码目录


CMakeLists.txt
```cmake
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

```

### 如何工作
警告标志有 -Wall 、 -Wextra 和 -Wpedantic ， 将这些标示添加到 geometry 目标的编译选项中； compute-areas 和 geometry 目标都将使用 -fPIC 标志。 编译选项可以添加三个级别的可见性： INTERFACE 、 PUBLIC 和 PRIVATE

可见性的含义如下:

- PRIVATE， 编译选项会应用于给定的目标， 不会传递给与目标相关的目标。 我们的示例中， 即使 compute-areas 将链接到 geometry 库， compute-areas 也不会继承 geometry 目标上设置的编译器选项。
- INTERFACE， 给定的编译选项将只应用于指定目标， 并传递给与目标相关的目标。
- PUBLIC， 编译选项将应用于指定目标和使用它的目标。

目标属性的可见性CMake的核心， 我们将在本书中经常讨论这个话题。 以这种方式添加编译选项， 不会影响全局CMake变量 CMAKE_<LANG>_FLAGS_<CONFIG> ， 并能更细粒度控制在哪些目标上使用哪些选项


如何确定项目在CMake构建时， 实际使用了哪些编译标志？ 一种方法是， 使用CMake将额外的参数传递给本地构建工具。 本例中会
设置环境变量 VERBOSE=1 

```sh
cmake -p build
cd build
cmake ..
cmake --build . -- VERBOSE=1

...
[ 14%] Building CXX object CMakeFiles/geometry.dir/geometry_circle.cpp.o
/usr/bin/c++   -fPIC -Wall -Wextra -Wpedantic -o CMakeFiles/geometry.dir/geometry_circle.cpp.o -c /opt/shared/vscode_projects/cmake_cookbook/src/chapter_01/recipe-08/geometry_circle.cpp
[ 28%] Building CXX object CMakeFiles/geometry.dir/geometry_polygon.cpp.o
/usr/bin/c++   -fPIC -Wall -Wextra -Wpedantic -o CMakeFiles/geometry.dir/geometry_polygon.cpp.o -c /opt/shared/vscode_projects/cmake_cookbook/src/chapter_01/recipe-08/geometry_polygon.cpp
[ 42%] Building CXX object CMakeFiles/geometry.dir/geometry_rhombus.cpp.o
/usr/bin/c++   -fPIC -Wall -Wextra -Wpedantic -o CMakeFiles/geometry.dir/geometry_rhombus.cpp.o -c /opt/shared/vscode_projects/cmake_cookbook/src/chapter_01/recipe-08/geometry_rhombus.cpp
[ 57%] Building CXX object CMakeFiles/geometry.dir/geometry_square.cpp.o
/usr/bin/c++   -fPIC -Wall -Wextra -Wpedantic -o CMakeFiles/geometry.dir/geometry_square.cpp.o -c /opt/shared/vscode_projects/cmake_cookbook/src/chapter_01/recipe-08/geometry_square.cpp

...
[ 85%] Building CXX object CMakeFiles/compute-areas.dir/compute-areas.cpp.o
/usr/bin/c++   -fPIC -o CMakeFiles/compute-areas.dir/compute-areas.cpp.o -c /opt/shared/vscode_projects/cmake_cookbook/src/chapter_01/recipe-08/compute-areas.cpp

```
控制编译器标志的第二种方法， 不用对 CMakeLists.txt 进行修改。 如果想在这个项目中修改 geometry 和 compute-areas 目标的编译器选项， 可以使用CMake参数进行配置

```sh
cmake -D CMAKE_CXX_FLAGS="-fno-exceptions -fno-rtti" ..
```

这个命令将编译项目， 禁用异常和运行时类型标识(RTTI)。
也可以使用全局标志， 可以使用 CMakeLists.txt 运行以下命令
```sh
cmake -D CMAKE_CXX_FLAGS="-fno-exceptions -fno-rtti" ..
```
这将使用 -fno-rtti - fpic - wall - Wextra - wpedantic 配置 geometry 目标， 同时使用 -fno exception -fno-rtti - fpic 配置 compute-areas

### 更多
最典型的方法是将所需编译器标志列表附加到每个配置类型CMake变量 CMAKE_<LANG>_FLAGS_<CONFIG> 。 标志确定设置为给定编译器有效的标志， 因此将包含在 ifendif 子句中， 用于检查 CMAKE_<LANG>_COMPILER_ID 变量

```cmake
if(CMAKE_CXX_COMPILER_ID MATCHES GNU)
list(APPEND CMAKE_CXX_FLAGS "-fno-rtti" "-fno-exceptions")

list(APPEND CMAKE_CXX_FLAGS_DEBUG "-Wsuggest-final-types" "-Wsuggest-finalmethods" "-Wsuggest-override")
list(APPEND CMAKE_CXX_FLAGS_RELEASE "-O3" "-Wno-unused")
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES Clang)

list(APPEND CMAKE_CXX_FLAGS "-fno-rtti" "-fno-exceptions" "-Qunusedarguments" "-fcolor-diagnostics")
list(APPEND CMAKE_CXX_FLAGS_DEBUG "-Wdocumentation")
list(APPEND CMAKE_CXX_FLAGS_RELEASE "-O3" "-Wno-unused")
endif()
```
更细粒度的方法是， 不修改 CMAKE_<LANG>_FLAGS_<CONFIG> 变量， 而是定义特定的标志列表

```cmake
set(COMPILER_FLAGS)
set(COMPILER_FLAGS_DEBUG)
set(COMPILER_FLAGS_RELEASE)

if(CMAKE_CXX_COMPILER_ID MATCHES GNU)
list(APPEND CXX_FLAGS "-fno-rtti" "-fno-exceptions")

list(APPEND CXX_FLAGS_DEBUG "-Wsuggest-final-types" "-Wsuggest-final-methods" "-Wsuggest-override")
list(APPEND CXX_FLAGS_RELEASE "-O3" "-Wno-unused")
endif()

if(CMAKE_CXX_COMPILER_ID MATCHES Clang)

list(APPEND CXX_FLAGS "-fno-rtti" "-fno-exceptions" "-Qunused-arguments" "-fcolor-diagnostics")
list(APPEND CXX_FLAGS_DEBUG "-Wdocumentation")
list(APPEND CXX_FLAGS_RELEASE "-O3" "-Wno-unused")
endif()
```
稍后， 使用生成器表达式来设置编译器标志的基础上， 为每个配置和每个目标生成构建系统
```cmake
target_compile_option(compute-areas
PRIVATE
${CXX_FLAGS}
"$<$<CONFIG:Debug>:${CXX_FLAGS_DEBUG}>"
"$<$<CONFIG:Release>:${CXX_FLAGS_RELEASE}>"
)
```

两种方法都有效， 并在许多项目中得到广泛应用。 不过， 每种方式都有缺点。 CMAKE_<LANG>_COMPILER_ID 不能保证为所有编译器都定义。 此外， 一些标志可能会被弃用， 或者在编译器的较晚版本中引入。 与 CMAKE_<LANG>_COMPILER_ID 类似， CMAKE_<LANG>_COMPILER_VERSION 变量不能保证为所有语言和供应商都提供定义。 尽管检查这些变量的方式非常流行， 但我们认为更健壮的替代方法是检查所需的标志集是否与给定的编译器一起工作， 这样项目中实际上只使用有效的标志。 结合特定于项目的变量、 target_compile_options 和生成器表达式， 会让解决方案变得非常强大。 我们将在第7章的第3节中展示， 如何使用 check-andset 模式


