## 创建一个简单的单元测试

CTest是CMake的测试工具， 本示例中， 我们将使用CTest进行单元测试。

## 准备

sum_integs.cpp

```cpp
#include "sum_integers.hpp"

#include <vector>

int sum_integers(const std::vector<int> integers) {
  auto sum = 0;
  for (auto i : integers) {
    sum += i;
  }
  return sum;
}

```

sum_integs.hpp

```cpp
#pragma once

#include <vector>

int sum_integers(const std::vector<int> integers);

```

main.cpp

```cpp
#include "sum_integers.hpp"

#include <iostream>
#include <string>
#include <vector>

// we assume all arguments are integers and we sum them up
// for simplicity we do not verify the type of arguments
int main(int argc, char *argv[]) {

  std::vector<int> integers;
  for (auto i = 1; i < argc; i++) {
    integers.push_back(std::stoi(argv[i]));
  }
  auto sum = sum_integers(integers);

  std::cout << sum << std::endl;
}

```

test.cpp

```cpp
#include "sum_integers.hpp"

#include <vector>

int main() {
  auto integers = {1, 2, 3, 4, 5};
  if(sum_integers(integers) == 15) {
    return 0;
  }else{
    return 1;
  }
}
```

bash shell调用可执行文件

```bash
#!/usr/bin/env bash

EXECUTABLE=$1
OUTPUT=$($EXECUTABLE 1 2 3 4)

if [ "$OUTPUT" = "10" ]
then
  exit 0
else
  exit 1
fi
```

python脚本调用可执行文件(--executable命令参数传递)
```python

import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--executable', )
```


## 实现

```cmake
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(recipe-01 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(PythonInterp REQUIRED)
find_program(BASH_EXECUTABLE NAMES bash REQUIRED)


add_library(sum_integers sum_integers.cpp)

add_executable(sum_up main.cpp)
target_link_libraries(sum_up sum_integers)


# testing
add_executable(cpp_test test.cpp)
target_link_libraries(cpp_test sum_integers)

#
enable_testing()

add_test(
  NAME bash_test
  COMMAND ${BASH_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/test.sh $<TARGET_FILE:sum_up>
)

add_test(
  NAME cpp_test
  COMMAND $<TARGET_FILE:cpp_test>
)

add_test(
  NAME python_test_long
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/test.py --executable $<TARGET_FILE:sum_up>
)

add_test(
  NAME python_test_short
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/test.py --short --executable $<TARGET_FILE:sum_up>
)
```

执行构建命令

```bash
mkdir -p build
cd build
cmake ..
cmake --build .
./sum_up 1 2 3 4 5
```
