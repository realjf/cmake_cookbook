#!/bin/sh

mkdir -p build
cd build
cmake ..
cmake --build .

./linear-algebra-unoptimized

