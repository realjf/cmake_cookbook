## 使用控制流


已经使用过 if-else-endif 。 CMake还提供了创建循环的语言工具： foreach endforeach 和 while-endwhile 。 两者都可以与 break 结合使用， 以便尽早从循环中跳出。 本示例将展示如何使用 foreach ， 来循环源文件列表。 我们将应用这样的循环， 在引入新目标的前提下， 来为一组源文件进行优化降级


### 实现

CMakeLists.txt内容如下：

```text
# set minimum cmake version
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

# project name and language
project(recipe-10 LANGUAGES CXX)

add_library(geometry
  STATIC
    geometry_circle.cpp
    geometry_circle.hpp
    geometry_polygon.cpp
    geometry_polygon.hpp
    geometry_rhombus.cpp
    geometry_rhombus.hpp
    geometry_square.cpp
    geometry_square.hpp
  )

# we wish to compile the library with the optimization flag: -O3
# 使用 -O3 编译器优化级别编译库， 对目标设置一个私有编译器选项
target_compile_options(geometry
  PRIVATE
    -O3
  )

# 然后， 生成一个源文件列表， 以较低的优化选项进行编译
list(
  APPEND sources_with_lower_optimization
    geometry_circle.cpp
    geometry_rhombus.cpp
  )

# we use the IN LISTS foreach syntax to set source properties
# 循环这些源文件， 将它们的优化级别调到 -O2 。 使用它们的源文件属性完成
message(STATUS "Setting source properties using IN LISTS syntax:")
foreach(_source IN LISTS sources_with_lower_optimization)
  set_source_files_properties(${_source} PROPERTIES COMPILE_FLAGS -O2)
  message(STATUS "Appending -O2 flag for ${_source}")
endforeach()

# we demonstrate the plain foreach syntax to query source properties
# which requires to expand the contents of the variable
# 为了确保设置属性， 再次循环并在打印每个源文件的 COMPILE_FLAGS 属性
message(STATUS "Querying sources properties using plain syntax:")
foreach(_source ${sources_with_lower_optimization})
  get_source_file_property(_flags ${_source} COMPILE_FLAGS)
  message(STATUS "Source ${_source} has the following extra COMPILE_FLAGS: ${_flags}")
endforeach()

# 添加 compute-areas 可执行目标， 并将 geometry 库连接上去
add_executable(compute-areas compute-areas.cpp)

target_link_libraries(compute-areas geometry)

```

```sh
mkdir -p build
cd build
cmake ..
```

最后， 还使用 VERBOSE=1 检查构建步骤。 将看到 -O2 标志添加在 -O3 标志之后， 但是最
后一个优化级别标志(在本例中是 -O2 )不同
```sh
cmake --build . -- VERBOSE=1
```

### 工作原理
foreach-endforeach 语法可用于在变量列表上， 表示重复特定任务。 本示例中， 使用它来操作、 设
置和获取项目中特定文件的编译器标志。 CMake代码片段中引入了另外两个新命令

- set_source_files_properties(file PROPERTIES property value) ， 它将属性设置为给定文件的传递值。 与目标非常相似， 文件在CMake中也有属性， 允许对构建系统进行非常细粒度的控制。 
- get_source_file_property(VAR file property) ， 检索给定文件所需属性的值， 并将其存储在CMake VAR 变量中

> CMake中， 列表是用分号分隔的字符串组。 列表可以由 list 或 set 命令创建。 例如， set(var a b c d e) 和 list(APPEND a b c d e) 都创建了列表 a;b;c;d;e


### 更多
foreach() 的四种使用方式

- foreach(loop_var arg1 arg2 ...) : 其中提供循环变量和显式项列表。 当为 sources_with_lower_optimization 中的项打印编译器标志集时， 使用此表单。 注意， 如果项目列表位于变量中， 则必须显式展开它； 也就是说， ${sources_with_lower_optimization} 必须作为参数传递。
- 通过指定一个范围， 可以对整数进行循环， 例如： foreach(loop_var range total) 或 foreach(loop_var range start stop [step])
- 对列表值变量的循环， 例如： foreach(loop_var IN LISTS [list1[...]]) 。 参数解释为列表， 其内容就会自动展开。
- 对变量的循环， 例如： foreach(loop_var IN ITEMS [item1 [...]]) 。 参数的内容没有展
开

