#!/bin/bash

set -e

# Install basic packages
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    git \
    ninja-build \
    python3 \
    python-is-python3

# Install clang-19
echo 'deb http://apt.llvm.org/noble/ llvm-toolchain-noble-19 main' > /etc/apt/sources.list.d/apt.llvm.org.list
wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key | tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc
apt-get update
apt-get install -y --no-install-recommends \
    clang-19 \
    llvm-19 \
    libclang-rt-19-dev \
    libc++-19-dev \
    libc++abi-19-dev \
    clang-tools-19
ln -s /usr/bin/clang-19 /usr/bin/clang
ln -s /usr/bin/clang++-19 /usr/bin/clang++

# Install CMake
cd
wget https://github.com/Kitware/CMake/releases/download/v3.31.3/cmake-3.31.3-linux-x86_64.tar.gz
tar -xf cmake-3.31.3-linux-x86_64.tar.gz
ln -s $(pwd)/cmake-3.31.3-linux-x86_64/bin/cmake /usr/bin/cmake
ln -s $(pwd)/cmake-3.31.3-linux-x86_64/bin/ctest /usr/bin/ctest
