project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/cmake_paths.cmake)

find_package(RocksDB CONFIG REQUIRED)

add_executable(rocks_sample rocksdb.cpp)
target_link_libraries(rocks_sample RocksDB::rocksdb)
