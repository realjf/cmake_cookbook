## 指定编译器



CMake将语言的编译器存储在 CMAKE_<LANG>_COMPILER 变量中， 其中 <LANG> 是受支持的任何一种语言， 对
于我们的目的是 CXX 、 C 或 Fortran 。 用户可以通过以下两种方式之一设置此变量：

1. 使用CLI中的-D选项，
```sh
cmake -D CMAKE_CXX_COMPILER=clang++ ..
```
2. 通过导出环境变量 CXX (C++编译器)、 CC (C编译器)和 FC (Fortran编译器)。 例如，使用这个命令使用 clang++ 作为 C++ 编译器
```sh
env CXX=clang++ cmake ..
```

> CMake了解运行环境， 可以通过其CLI的 -D 开关或环境变量设置许多选项。 前一种机制覆盖后一种机制， 但是我们建议使用 -D 显式设置选项。 显式优于隐式， 因为环境变量可能被设置为不适合(当前项目)的值


> 我们建议使用 -D CMAKE_<LANG>_COMPILER CLI选项设置编译器， 而不是导出 CXX 、 CC 和 FC 。 这是确保跨平台并与非POSIX兼容的唯一方法。 为了避免变量污染环境，这些变量可能会影响与项目一起构建的外部库环境

### 更多
CMake提供 --systeminformation 标志， 它将把关于系统的所有信息转储到屏幕或文件中。 要查看这个信息， 请尝试以下
操作

```sh
cmake --system-information information.txt
```
可以看到 CMAKE_CXX_COMPILER 、 CMAKE_C_COMPILER 和 CMAKE_Fortran_COMPILER 的默认值， 以及默认标志。 我们将在下一个示例中看到相关的标志

CMake提供了额外的变量来与编译器交互:
- CMAKE_<LANG>_COMPILER_LOADED :如果为项目启用了语言 <LANG> ， 则将设置为 TRUE 。
- CMAKE_<LANG>_COMPILER_ID :编译器标识字符串， 编译器供应商所特有。 例如， GCC 用于GNU编译器集合， AppleClang 用于macOS上的Clang, MSVC 用于Microsoft Visual Studio编译器。 注意， 不能保证为所有编译器或语言定义此变量。
- CMAKE_COMPILER_IS_GNU<LANG> :如果语言 <LANG> 是GNU编译器集合的一部分， 则将此逻辑变量设置为 TRUE 。 注意变量名的 <LANG> 部分遵循GNU约定： C语言为 CC , C++语言为 CXX , Fortran语言为 G77 。
- CMAKE_<LANG>_COMPILER_VERSION :此变量包含一个字符串， 该字符串给定语言的编译器版本。 版本信息在 major[.minor[.patch[.tweak]]] 中给出。 但是， 对于 CMAKE_<LANG>_COMPILER_ID ， 不能保证所有编译器或语言都定义了此变量

