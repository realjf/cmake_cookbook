## 检测python解释器

### 实现

CMakeLists.txt内容如下：

```cmake
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(recipe-01 LANGUAGES NONE)

# 使用find_package命令找到python解释器
find_package(PythonInterp RQUIRED)

# 执行python命令并捕获它的输出和返回值
execute_process(COMMAND ${PYTHON_EXECUTABLE} "-c" "print('Hello, world!')"
    RESULT_VARIABLE _status
    OUTPUT_VARIABLE _hello_world
    ERROR_QUIET
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# 打印python命令的返回值和输出：
message(STATUS "RESULT_VARIABLE is: ${_status}")
message(STATUS "OUTPUT_VARIABLE is: ${_hello_world}")


```

### 工作原理
find_package 是用于发现和设置包的CMake模块的命令。 这些模块包含CMake命令， 用于标识系统
标准位置中的包。 CMake模块文件称为 Find<name>.cmake ， 当调用 find_package(<name>) 时，
模块中的命令将会运行。

除了在系统上实际查找包模块之外， 查找模块还会设置了一些有用的变量， 反映实际找到了什么， 也可
以在自己的 CMakeLists.txt 中使用这些变量。 对于Python解释器， 相关模块
为 FindPythonInterp.cmake 附带的设置了一些CMake变量:

- PYTHONINTERP_FOUND：是否找到解释器
- PYTHON_EXECUTABLE:python解释器到可执行文件的路径
- PYTHON_VERSION_STRING: python解释器的完整版本信息
- PYTHON_VERSION_MAJOR: python解释器的主要版本号
- PYTHON_VERSION_MINOR: python解释器的次要版本
- PYTHON_VERSION_PATCH: python解释器的补丁版本号

可以强制CMake， 查找特定版本的包。 例如， 要求Python解释器的版本大于或等于
```cmake
find_package(PythonInterp 2.7)
```
可以强制满足依赖关系：
```cmake 
find_package(PythonInterp REQUIRED)
```
如果在查找位置中没有找到适合Python解释器的可执行文件， CMake将中止配置。

### 更多信息
用户可以使用CLI的 -D 参数传递相应的
选项， 告诉CMake查看特定的位置。 Python解释器可以使用以下配置:
```cmake
cmake -D PYTHON_EXECUTABLE=/custom/location/python ..
```
这将指定非标准 /custom/location/pytho 安装目录中的Python可执行文件。

> 每个包都是不同的， Find<package>.cmake 模块试图提供统一的检测接口。 当CMake无法找到模块包时， 我们建议您阅读相应检测模块的文档， 以了解如何正确地使用CMake模块。 可以在终端中直接浏览文档， 本例中可使用 cmake --help-module FindPythonInterp 查看。

除了检测包之外， 我们还想提到一个便于打印变量的helper模块。 本示例中， 我们使用了以下方法:
```cmake
message(STATUS "RESULT_VARIABLE is: ${_status}")
message(STATUS "OUTPUT_VARIABLE is: ${_hello_world}")
```

使用如下工具进行调试：
```cmake
include(CMakePrintHelpers)
cmake_print_variables(_status _hello_world)
```
将产生以下输出:
```
-- _status="0" ; _hello_world="Hello, world!"
```
