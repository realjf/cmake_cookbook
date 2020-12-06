## 向用户显示选项

推荐在 CMakeLists.txt 中使用 option() 命令， 以选项的形式显示逻辑开关， 用于外部设置， 从而切换构建系统的生成行为。 本节的示例将向您展示， 如何使用这个命令


### 准备
与其硬编码 USE_LIBRARY 为 ON 或 OFF ， 现在为其设置一个默认值， 同时也可以从外部进行更改：

- 用一个选项替换上一个示例的 set(USE_LIBRARY OFF) 命令。 该选项将修改 USE_LIBRARY 的值， 并设置其默认值为 OFF ：
    - option(USE_LIBRARY "Compile sources into a library" OFF)
- 现在， 可以通过CMake的 -D CLI选项， 将信息传递给CMake来切换库的行为

```sh
mkdir -p build
cd build
cmake -D USE_LIBRARY=ON ..

```
-D 开关用于为CMake设置任何类型的变量： 逻辑变量、 路径等等

### 工作原理
- option 可接受三个参数：

option(<option_variable> "help string" [initial value])
- <option_variable> 表示该选项的变量的名称。
- "help string" 记录选项的字符串， 在CMake的终端或图形用户界面中可见。
- [initial value] 选项的默认值， 可以是 ON 或 OFF

### 更多
有时选项之间会有依赖的情况。 示例中， 我们提供生成静态库或动态库的选项。 但是， 如果没有将 USE_LIBRARY 逻辑设置为 ON ， 则此选项没有任何意义。 CMake提供 cmake_dependent_option() 命令用来定义依赖于其他选项的选项

```cmake
include(CMakeDependentOption)

# second option depends on the value of the first
cmake_dependent_option(
MAKE_STATIC_LIBRARY "Compile sources into a static library" OFF
"USE_LIBRARY" ON
)

# third option depends on the value of the first
cmake_dependent_option(
MAKE_SHARED_LIBRARY "Compile sources into a shared library" ON
"USE_LIBRARY" ON
)

```
如果 USE_LIBRARY 为 ON ， MAKE_STATIC_LIBRARY 默认值为 OFF ， 否则 MAKE_SHARED_LIBRARY 默认值为 ON 。 可以这样运行

```sh
cmake -D USE_LIBRARY=OFF -D MAKE_SHARED_LIBRARY=ON ..
```


CMake有适当的机制， 通过包含模块来扩展其语法和功能， 这些模块要么是CMake自带的， 要么是定制的。 本例中， 包含了一个名为 CMakeDependentOption 的模块。 如果没有 include 这个模块， cmake_dependent_option() 命令将不可用。

