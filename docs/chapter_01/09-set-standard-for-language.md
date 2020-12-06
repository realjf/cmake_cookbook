## 为语言设定标准


为目标设置 <LANG>_STANDARD 属性

### 准备

对于下面的示例， 需要一个符合 C++14 标准或更高版本的 C++ 编译器。 此示例代码定义了动物的多态， 我们使用 std::unique_ptr 作为结构中的基类
```cpp
std::unique_ptr<Animal> cat = Cat("Simon");
std::unique_ptr<Animal> dog = Dog("Marlowe);
```
没有为各种子类型显式地使用构造函数， 而是使用工厂方法的实现。 工厂方法使用 C++11 的可变参数模板实现。 它包含继承层次结构中每个对象的创建函数映射
```cpp
typedef std::function<std::unique_ptr<Animal>(const std::string &)> CreateAnimal;
```

基于预先分配的标签来分派它们， 创建对象

```cpp
std::unique_ptr<Animal> simon = farm.create("CAT", "Simon");
std::unique_ptr<Animal> marlowe = farm.create("DOG", "Marlowe");
```
标签和创建功能在工厂使用前已注册
```cpp
Factory<CreateAnimal> farm;
farm.subscribe("CAT", [](const std::string & n) { return std::make_unique<Cat>(n); });

```
使用 C++11 Lambda 函数定义创建函数， 使用 std::make_unique 来避免引入裸指针的操作。 这个工厂函数是在 C++14 中引入

### 具体实现

CMakeLists.txt如下：


```cmake
# set minimum cmake version
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

# project name and language
project(recipe-09 LANGUAGES CXX)

# 要求在Windows上导出所有库符号
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

# 需要为库添加一个目标， 这将编译源代码为一个动态库
add_library(animals
  SHARED
    Animal.cpp
    Animal.hpp
    Cat.cpp
    Cat.hpp
    Dog.cpp
    Dog.hpp
    Factory.hpp
  )

# 现在， 为目标设置了 CXX_STANDARD 、 CXX_EXTENSIONS 和 CXX_STANDARD_REQUIRED 属性。 
# 还设置了 position_independent ent_code 属性， 以避免在使用一些编译器构建DSO时出现问题
set_target_properties(animals
  PROPERTIES
    CXX_STANDARD 14
    CXX_EXTENSIONS OFF
    CXX_STANDARD_REQUIRED ON
    POSITION_INDEPENDENT_CODE 1
  )

# 然后， 为”动物农场”的可执行文件添加一个新目标， 并设置它的属性
add_executable(animal-farm animal-farm.cpp)

set_target_properties(animal-farm
  PROPERTIES
    CXX_STANDARD 14
    CXX_EXTENSIONS OFF
    CXX_STANDARD_REQUIRED ON
  )

# 将可执行文件链接到库
target_link_libraries(animal-farm animals)

```

### 工作原理

我们为动物和动物农场目标设置了一些属性:
- CXX_STANDARD会设置我们想要的标准。
- CXX_EXTENSIONS告诉CMake， 只启用 ISO C++ 标准的编译器标志， 而不使用特定编译器的扩展。
- CXX_STANDARD_REQUIRED指定所选标准的版本。 如果这个版本不可用， CMake将停止配置并出现错误。 当这个属性被设置为 OFF 时， CMake将寻找下一个标准的最新版本， 直到一个合适的标志。 这意味着， 首先查找 C++14 ， 然后是 C++11 ， 然后是 C++98 。 （ 译者注： 目前会从 C++20 或 C++17 开始查找）


> 如果语言标准是所有目标共享的全局属性， 那么可以将 CMAKE_<LANG>_STANDARD 、 CMAKE_<LANG>_EXTENSIONS 和 CMAKE_<LANG>_STANDARD_REQUIRED 变量设置为相应的值。 所有目标上的对应属性都将使用这些设置

### 更多
通过引入编译特性， CMake对语言标准提供了更精细的控制。 这些是语言标准引入的特性， 比如 C++11 中的可变参数模板和 Lambda 表达式， 以及 C++14 中的自动返回类型推断。 可以使用 target_compile_features() 命令要求为特定的目标提供特定的特性， CMake将自动为标准设置正确的编译器标志。 也可以让CMake为可选编译器特性， 生成兼容头文件

