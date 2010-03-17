# Top-level CMakeLists.txt file for pyosg++
#
# I typically configure with a command similar to the following:
#
#  c:\d\pyosg++\build>cmake -DCMAKE_INCLUDE_PATH=c:\pt\externals\include \
#   -DCMAKE_LIBRARY_PATH=c:\pt\externals\lib \
#   -DCMAKE_PREFIX_PATH="C:\pt\externals\bin" ..
#
cmake_minimum_required(VERSION 2.6)

project(pyosg++)

# Put all libs and executables in a 'bin' subdir
set(LIBRARY_OUTPUT_PATH
    ${PROJECT_BINARY_DIR}/bin
    CACHE PATH
    "Single directory for all libraries.")

set(EXECUTABLE_OUTPUT_PATH
    ${PROJECT_BINARY_DIR}/bin
    CACHE PATH
    "Single directory for all executables.")

mark_as_advanced(LIBRARY_OUTPUT_PATH)
mark_as_advanced(EXECUTABLE_OUTPUT_PATH)

# Every wrapped lib needs these, so just find 'em here
find_package(OpenSceneGraph REQUIRED)
find_package(Boost REQUIRED COMPONENTS python)
find_package(GCCXML REQUIRED)
find_package(OpenSceneGraph REQUIRED)
find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)

# Include custom functions
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMakeModules;${CMAKE_MODULE_PATH}")
include(custom_functions)

# Invoke custom function to create a cmake.py settings module
create_cmake_py_module()

include_directories(${PYTHON_INCLUDE_PATH}
                    ${Boost_INCLUDE_DIR}
                    ${OSG_INCLUDE_DIR})

link_directories(${Boost_LIBRARY_DIRS})

# Don't prepend 'lib' to the names of modules built
set(CMAKE_SHARED_MODULE_PREFIX "")


add_subdirectory(osg)
#add_subdirectory(osgDB)
#add_subdirectory(osgFX)
# etc., etc.
