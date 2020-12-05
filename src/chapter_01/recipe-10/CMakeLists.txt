# set minimum cmake version
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

# project name and language
project(recipe-10 LANGUAGES CXX)

add_library(geometry
  STATIC
    geometry_circle.cpp
    geometry_circle.hpp
    geometry_polygon.cpp
    geometry_polygon.hpp
    geometry_rhombus.cpp
    geometry_rhombus.hpp
    geometry_square.cpp
    geometry_square.hpp
  )

# we wish to compile the library with the optimization flag: -O3
# 使用 -O3 编译器优化级别编译库， 对目标设置一个私有编译器选项
target_compile_options(geometry
  PRIVATE
    -O3
  )

# 然后， 生成一个源文件列表， 以较低的优化选项进行编译
list(
  APPEND sources_with_lower_optimization
    geometry_circle.cpp
    geometry_rhombus.cpp
  )

# we use the IN LISTS foreach syntax to set source properties
# 循环这些源文件， 将它们的优化级别调到 -O2 。 使用它们的源文件属性完成
message(STATUS "Setting source properties using IN LISTS syntax:")
foreach(_source IN LISTS sources_with_lower_optimization)
  set_source_files_properties(${_source} PROPERTIES COMPILE_FLAGS -O2)
  message(STATUS "Appending -O2 flag for ${_source}")
endforeach()

# we demonstrate the plain foreach syntax to query source properties
# which requires to expand the contents of the variable
# 为了确保设置属性， 再次循环并在打印每个源文件的 COMPILE_FLAGS 属性
message(STATUS "Querying sources properties using plain syntax:")
foreach(_source ${sources_with_lower_optimization})
  get_source_file_property(_flags ${_source} COMPILE_FLAGS)
  message(STATUS "Source ${_source} has the following extra COMPILE_FLAGS: ${_flags}")
endforeach()

# 添加 compute-areas 可执行目标， 并将 geometry 库连接上去
add_executable(compute-areas compute-areas.cpp)

target_link_libraries(compute-areas geometry)

