## 将单个源码文件编译为可执行文件

### 准备
创建一个项目目录
```sh
mkdir recipe-01
cd recipe-01
# 创建源文件和cmake构建文件
touch helloworld.cpp
touch CMakeLists.txt
```

源程序helloworld.cpp内容如下：
```cpp
#include <cstdlib>
#include <iostream>
#include <string>

std::string say_hello() {
    return std::string("Hello, CMake world!");
}

int main()
{
    std::cout << say_hello() << std::endl;
    return EXIT_SUCCESS;
}

```

CMakeLists.txt文件内容如下：
```txt
# 首先，设置cmake所需的最低版本，如果使用CMake版本低于该版本，则会发出致命错误
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)


# 第二行，声明项目的名称和支持的编程语言
project(recipe-01 LANGUAGES CXX)

# 指示CMake创建一个新目标：可执行文件 hello-world，这个可执行文件
# 是通过编译和链接源文件helloworld.cpp生成，cmake使用编译器默认配置，自动生成
add_executable(hello-world helloworld.cpp)

```

> 这里需要将源文件helloworld.cpp放在相同的目录中。

## 编译
现在可以通过创建build目录，在build目录下来配置项目：

```sh
mkdir -p build
cd build
cmake ..

-- The CXX compiler identification is GNU 10.2.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /opt/shared/vscode_projects/cmake_cookbook/src/chapter_01/recipe-01/build

```

如果一切顺利，项目的配置已经在build目录中生成，我们可以编译可执行文件

```sh
cmake --build .

-- Configuring done
-- Generating done
-- Build files have been written to: /opt/shared/vscode_projects/cmake_cookbook/src/chapter_01/recipe-01/build
Scanning dependencies of target hello-world
[ 50%] Building CXX object CMakeFiles/hello-world.dir/helloworld.cpp.o
[100%] Linking CXX executable hello-world
[100%] Built target hello-world
```

## 工作原理

> cmake语言不区分大小写，但是参数区分大小写

> cmake中，c++是默认的编程语言。不过，我们还是建议使用LANGUAGES 选项在project命令中显式地声明项目的语言。

要配置项目并生成构建器， 我们必须通过命令行界面(CLI)运行CMake。 CMake CLI提供了许多选项， cmake -help 将输出以显示列出所有可用选项的完整帮助信息， 我们将在书中对这些选项进行更多地了解。 正如您将从 cmake -help 的输出中显示的内容， 它们中的大多数选项会让你您访问CMake手册， 查看详细信息。 通过下列命令生成构建器

```sh
mkdir -p build
cd build
cmake ..
```
这里创建的build目录，通过指定CMakeLists.txt文件的位置来调用cmake，可以使用以下命令来实现相同的效果：

```sh
cmake -H. -Bbuild
```
该命令是跨平台，-H表示当前目录中搜索根CMakeLists.txt文件。
-Bbuild告诉CMake在一个名为build的目录中生成所有的文件。

CMake是一个构建系统生成器。 将描述构建系统(如： Unix Makefile、 Ninja、 Visual Studio等)应当如何操作才能编译代码。 然后， CMake为所选的构建系统生成相应的指令。 默认情况下， 在GNU/Linux和macOS系统上， CMake使用Unix Makefile生成器。 Windows上， Visual Studio是默认的生成器。

GNU/Linux上，CMake默认生成unix Makefile来构建项目：

- Makefile: make 将运行指令来构建项目
- CMakefile: 包含临时文件的目录，CMake用于检测操作系统、编译器等，此外根据所选的生成器，它还包含特定的文件
- cmake_install.cmake：处理安装规则的cmake脚本，在项目安装时使用
- CMakeCache.txt：如文件名，CMake缓存，cmake在重新运行配置时使用这个文件

cmake不强制指定构建目录执行名称或位置，可以把它放在项目路径之外，如：
```sh
mkdir -p /tmp/someplace
cd /tmp/someplace
cmake /path/to/source
cmake --build .
```


```sh
cmake --build . --target help
```
上述命令生成的目标将包含目标文件.o和.s，.i等文件

- all 时默认目标，将在项目中构建所有目标
- clean，删除所有生成的文件
- rebuild_cache，将调用cmake为源文件生成依赖
- edit_cache，这个目标允许直接编辑缓存

对于更复杂的项目，通过测试阶段和安装规则，cmake将生成额外的目标：

- test，将在CTest的帮助下运行测试套件。
- install，将执行项目安装规则
- package，此目标将调用CPack为项目生成可分发的包。

