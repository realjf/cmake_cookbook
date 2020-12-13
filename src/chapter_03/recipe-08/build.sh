#!/bin/sh

mkdir -p build
cd build

cmake ..
# 当然也可以手动指定boost安装目录
# cmake -D BOOST_ROOT=/usr/include/boost ..
# 或者传递BOOST_INCLUDEDIR和BOOST_LIBRARYDIR目录
cmake --build .

