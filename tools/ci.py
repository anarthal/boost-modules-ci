#!/usr/bin/python3

import subprocess
from typing import List
import os
from pathlib import Path
import argparse


BOOST_ROOT = Path(os.path.expanduser('~')).joinpath('boost-modules-root')


def run(args: List[str]) -> None:
    print('+ ', args, flush=True)
    subprocess.run(args, check=True)


def mkdir_and_cd(path: Path) -> None:
    os.makedirs(str(path), exist_ok=True)
    os.chdir(str(path))


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Boost modules CI")
    parser.add_argument(
        '--toolset', 
        choices=['clang', 'msvc'],
        required=True,
        help="The toolset to use to build the code"
    )

    # Parse the arguments
    args = parser.parse_args()
    toolset = args.toolset

    # Clone Boost
    run(['git', 'clone', '-b', 'develop', '--depth', '1', 'https://github.com/boostorg/boost.git', str(BOOST_ROOT)])
    os.chdir(str(BOOST_ROOT))

    # Clone the relevant modules
    submodules = [
        ('tools/cmake',         'https://github.com/anarthal/boost-cmake',    'feature/cxx20-modules'),
        ('libs/config',         'https://github.com/anarthal/config',         'feature/cxx20-modules'),
        ('libs/assert',         'https://github.com/anarthal/assert',         'feature/cxx20-modules'),
        ('libs/mp11',           'https://github.com/anarthal/mp11',           'feature/cxx20-modules'),
        ('libs/core',           'https://github.com/anarthal/core',           'feature/cxx20-modules'),
        ('libs/throw_exception','https://github.com/anarthal/throw_exception','feature/cxx20-modules'),
        ('libs/static_assert',  'https://github.com/boostorg/static_assert',  'develop'),
    ]
    for submodule, url, branch in submodules:
        run(["git", "clone", url, "--depth", "1", "-b", branch, submodule])
    
    # Run the mp11 tests
    os.environ['CMAKE_BUILD_PARALLEL_LEVEL'] = '8'
    mkdir_and_cd(BOOST_ROOT.joinpath('__build__'))
    run([
        'cmake',
        '-DBOOST_INCLUDE_LIBRARIES=mp11',
        '-DBUILD_TESTING=ON',
        '-DBOOST_CXX20_MODULE=ON',
        '-DCMAKE_EXPERIMENTAL_CXX_IMPORT_STD=0e5b6991-d74f-4b3d-a41c-cf096e0b2508',
    ] + ([
        '-DCMAKE_CXX_FLAGS=-stdlib=libc++',
        '-DCMAKE_EXE_LINKER_FLAGS=-stdlib=libc++',
    ] if toolset == 'clang' else []) + [
        '-DCMAKE_CXX_STANDARD=23',
        '-G',
        'Ninja',
        '..'
    ])
    run(['cmake', '--build', '.', '--target', 'tests'])
    run(['ctest', '--output-on-failure', '--no-tests=error'])


if __name__ == '__main__':
    main()
