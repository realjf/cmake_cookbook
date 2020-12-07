#!/bin/sh

mkdir -p build
cd build
cmake ..
cmake --build .

./arch-dependent

