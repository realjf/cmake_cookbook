## 准备

main.cpp

```cpp
#include "sum_integers.hpp"
#include "gtest/gtest.h"

#include <vector>

int main(int argc, char** argv){
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

TEST(example, sum_zero) {
    auto integers = {1, -1, 2, -2, 3, -3};
    auto result = sum_integers(integers);
    ASSERT_EQ(result, 0);
}

TEST(example, sum_five) {
    auto integers = {1, 2, 3, 4, 5};
    auto result = sum_integers(integers);
    ASSERT_EQ(result, 15);
}



```

sum_integers.cpp

```cpp

```

sum_integers.hpp

test.cpp

```cpp

```

CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.11 FATAL_ERROR)

project(recipe-03 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

add_library(sum_integers sum_integers.cpp)

add_executable(sum_up)
```
