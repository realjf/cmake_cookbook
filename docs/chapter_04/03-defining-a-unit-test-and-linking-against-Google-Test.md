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

add_executable(sum_up main.cpp)
target_link_libraries(sum_up sum_integers)

# 检查 ENABLE_UNIT_TESTS，默认为ON，但有时需要设置为OFF，以免在没有网络连接时，也能使用Google Test
option(ENABLE_UNIT_TESTS "Enable unit tests" ON)
message(STATUS "Enable testing: ${ENABLE_UNIT_TESTS}")

if(ENABLE_UNIT_TESTS)
    include(FetchContent)
    # 声明要获取的新内容，并查询其属性
    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG release-1.8.0
    )
    FetchContent_GetProperties(googletest)

    # 如果没有获取到，尝试获取并配置它
    if(NOT googletest_POPULATED)
        FetchContent_Populate(googletest)

        # 防止googletest修改编译器/链接器配置项
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
        # 防止使用pthreads
        set(gtest_disable_pthreads ON CACHE BOOL "" FORCE)

        # 添加targets: gtest,gtest_main,gmock,gmock_main
        add_subdirectory(
            ${googletest_SOURCE_DIR}
            ${googletest_BINARY_DIR}
        )

        # 静默 MSVC警告
        if(MSVC)
            foreach(_tgt gtest gtest_main gmock gmock_main)
                target_compile_definitions(${_tgt}
                PRIVATE
                "_SILENCE_TR1_NAMESPACE_DEPRECATION_WARNING"
                )
            endforeach()
        endif()
    endif()

    add_executable(cpp_test "")
    target_sources(cpp_test
        PRIVATE
        test.cpp
        )
    target_link_libraries(cpp_test PRIVATE sum_integers gtest_main)

    enable_testing()

    add_test(
        NAME google_test
        COMMAND $<TARGET_FILE:cpp_test>
    )
endif()


```

准备构建

```bash
mkdir -p build
cd build
cmake ..
cmake --build .
ctest

./cpp_test
```

## 工作原理
