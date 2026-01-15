cmake_minimum_required(VERSION 3.12)
project(SarahCoreBindings)

set(CMAKE_CXX_STANDARD 17)

find_package(pybind11 REQUIRED)

add_library(sarah_core_bindings MODULE sarah_core_bindings.cpp)
target_include_directories(sarah_core_bindings PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(sarah_core_bindings PRIVATE pybind11::module)

# Set the output file extension for Python module
set_target_properties(sarah_core_bindings PROPERTIES
    PREFIX ""
    SUFFIX ".pyd"
)
