## 为Eigen库使能向量化


### 准备
我们用Eigen C++模板库， 用来进行线性代数计算， 并展示如何设置编译器标志来启用向量化。 这个示
例的源代码 linear-algebra.cpp 文件

```cpp
#include <chrono>
#include <iostream>

#include <Eigen/Dense>

EIGEN_DONT_INLINE
double simple_function(Eigen::VectorXd &va, Eigen::VectorXd &vb) {
  // this simple function computes the dot product of two vectors
  // of course it could be expressed more compactly
  double d = va.dot(vb);
  return d;
}

int main() {
  int len = 1000000;
  int num_repetitions = 100;

  // generate two random vectors
  Eigen::VectorXd va = Eigen::VectorXd::Random(len);
  Eigen::VectorXd vb = Eigen::VectorXd::Random(len);

  double result;
  auto start = std::chrono::system_clock::now();
  for (auto i = 0; i < num_repetitions; i++) {
    result = simple_function(va, vb);
  }
  auto end = std::chrono::system_clock::now();
  auto elapsed_seconds = std::chrono::duration_cast<std::chrono::microseconds>(end-start);

  std::cout << "result: " << result << std::endl;
  std::cout << "elapsed seconds: " << elapsed_seconds.count()/1000000.0 << std::endl;
}

```
### 实现
CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(recipe-06 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 使用Eigen库，我们需要在系统上找到它的头文件
find_package(Eigen3 3.3 REQUIRED CONFIG)

# CheckCXXCompilerFlag.cmake标准模板文件
include(CheckCXXCompilerFlag)

# 检查-march=native编译器标志是否工作
check_cxx_compiler_flag("-march=native" _march_native_works)
check_cxx_compiler_flag("-xHost" _xhost_works)

# 设置了一个空变量 _CXX_FLAGS ， 来保存刚才检查的两个编译器中找到的编译器标志。 如果看
# 到 _march_native_works ， 我们将 _CXX_FLAGS 设置为 -march=native 。 如果看
# 到 _xhost_works ， 我们将 _CXX_FLAGS 设置为 -xHost 。 如果它们都不起作
# 用， _CXX_FLAGS 将为空， 并禁用矢量化
set(_CXX_FLAGS)
if(_march_native_works)
  message(STATUS "Using processor's vector instructions (-march=native compiler flag set)")
  set(_CXX_FLAGS "-march=native")
elseif(_xhost_works)
  message(STATUS "Using processor's vector instructions (-xHost compiler flag set)")
  set(_CXX_FLAGS "-xHost")
else()
  message(STATUS "No suitable compiler flag found for vectorization")
endif()

# 为未优化的版本定义了一个可执行目标， 不使用优化标志
add_executable(linear-algebra-unoptimized linear-algebra.cpp)

target_link_libraries(linear-algebra-unoptimized
  PRIVATE
    Eigen3::Eigen
  )

# 我们定义了一个优化版本
add_executable(linear-algebra linear-algebra.cpp)

target_compile_options(linear-algebra
  PRIVATE
    ${_CXX_FLAGS}
  )

target_link_libraries(linear-algebra
  PRIVATE
    Eigen3::Eigen
  )

```

### 工作原理
由于线性代数运算可以从Eigen库中获得很好的加速， 所以在使用Eigen库时， 就要考虑向量化。 我们所要做的就是， 指示编译器为我们检查处理器， 并为当前体系结构生成本机指令。 不同的编译器供应商会使用不同的标志来实现这一点： GNU编译器使用 -march=native 标志来实现这一点， 而Intel编译器使用 -xHost 标志。使用 CheckCXXCompilerFlag.cmake 模块提供的 check_cxx_compiler_flag 函数进行编译器标志的检查:

check_cxx_compiler_flag("-march=native" _march_native_works)

这个函数接受两个参数
- 第一个是要检查的编译器标志。
- 第二个是用来存储检查结果(true或false)的变量。 如果检查为真， 我们将工作标志添加到 _CXX_FLAGS 变量中， 该变量将用于为可执行目标设置编译器标志。

### 更多信息
可以使用 cmake_host_system_information 查询处理器功能


