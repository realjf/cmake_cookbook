cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

project(recipe-01 LANGUAGES NONE)

# 使用find_package命令找到python解释器
find_package(PythonInterp RQUIRED)

# 执行python命令并捕获它的输出和返回值
execute_process(COMMAND ${PYTHON_EXECUTABLE} "-c" "print('Hello, world!')"
    RESULT_VARIABLE _status
    OUTPUT_VARIABLE _hello_world
    ERROR_QUIET
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# 打印python命令的返回值和输出：
message(STATUS "RESULT_VARIABLE is: ${_status}")
message(STATUS "OUTPUT_VARIABLE is: ${_hello_world}")

