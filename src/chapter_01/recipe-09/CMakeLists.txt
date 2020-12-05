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
