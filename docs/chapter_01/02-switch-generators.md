## 切换生成器

```
cmake --help

...
Generators

The following generators are available on this platform (* marks default):
* Unix Makefiles               = Generates standard UNIX makefiles.
  Green Hills MULTI            = Generates Green Hills MULTI files
                                 (experimental, work-in-progress).
  Ninja                        = Generates build.ninja files.
  Ninja Multi-Config           = Generates build-<Config>.ninja files.
  Watcom WMake                 = Generates Watcom WMake makefiles.
  CodeBlocks - Ninja           = Generates CodeBlocks project files.
  CodeBlocks - Unix Makefiles  = Generates CodeBlocks project files.
  CodeLite - Ninja             = Generates CodeLite project files.
  CodeLite - Unix Makefiles    = Generates CodeLite project files.
  Sublime Text 2 - Ninja       = Generates Sublime Text 2 project files.
  Sublime Text 2 - Unix Makefiles
                               = Generates Sublime Text 2 project files.
  Kate - Ninja                 = Generates Kate project files.
  Kate - Unix Makefiles        = Generates Kate project files.
  Eclipse CDT4 - Ninja         = Generates Eclipse CDT 4.0 project files.
  Eclipse CDT4 - Unix Makefiles= Generates Eclipse CDT 4.0 project files.

```
可以查看支持的生成器

## 准备
使用前一节的源代码和CMakeLists.txt文件

## 构建
```sh
# 在项目根目录下
mkdir -p build
cd build
# 使用-G切换生成器
cmake -G Ninja ..

-- The CXX compiler identification is GNU 10.2.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /opt/shared/vscode_projects/cmake_cookbook/src/chapter_01/recipe-02/build

# 构建
cmake --build .

[2/2] Linking CXX executable hello-world
```

## 如何工作
与前一个配置相比， 每一步的输出没什么变化。 每个生成器都有自己的文件集， 所以编译步骤的输出和构建目录的内容是不同的：

- build.ninja 和 rules.ninja ： 包含Ninja的所有的构建语句和构建规则。
- CMakeCache.txt ： CMake会在这个文件中进行缓存， 与生成器无关。
- CMakeFiles ： 包含由CMake在配置期间生成的临时文件。
- cmake_install.cmake ： CMake脚本处理安装规则， 并在安装时使用。

cmake --build . 将ninja命令封装在一个跨平台的接口中




