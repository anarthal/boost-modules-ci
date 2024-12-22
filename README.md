# C++20 modules for Boost

This repository is part of a prototype to check the viability of building and distributing Boost as C++20 modules. This is a work-in-progress.

Work is being done in the following repositories and branches:

- Boost.CMake: https://github.com/anarthal/boost-cmake/tree/feature/cxx20-modules
- Boost.Config: https://github.com/anarthal/config/tree/feature/cxx20-modules
- Boost.Assert: https://github.com/anarthal/assert/tree/feature/cxx20-modules
- Boost.ThrowException: https://github.com/anarthal/throw_exception/tree/feature/cxx20-modules
- Boost.Mp11: https://github.com/anarthal/mp11/tree/feature/cxx20-modules
- Boost.Core: https://github.com/anarthal/core/tree/feature/cxx20-modules

The intention is to build each library as a module, and support `import std`, only.
Modules can be consumed using `FetchContent` with the Boost super-project
or by building, installing and finding Boost with `find_package` (using CMake in both cases).

This repository contains CI files to verify that everything build with both clang and MSVC.
CI files will be moved to individual repositories in the future.

The scope of this initiative is to modularize a small part of Boost, including tests,
as a proof-of-concept.
