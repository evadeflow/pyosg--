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

if(WIN32)
  # Set a few platform conditionals needed by gccxml when parsing OSG headers
  set(GCCXML_DEFINES "['_MSCVER', 'WIN32']")

  # Tell gccxml which version of Visual Studio to simulate
  if(MSVC80)
    set(GCCXML_COMPILER "msvc8")
  elseif(MSVC71)
    set(GCCXML_COMPILER "msvc71")
  else()
    set(GCCXML_COMPILER "\"\"")
  endif()
else()
    # Assume g++ if not WIN32
    set(GCCXML_COMPILER "g++")
endif()

include_directories(${PYTHON_INCLUDE_PATH}
                    ${Boost_INCLUDE_DIR}
                    ${OSG_INCLUDE_DIR})

link_directories(${Boost_LIBRARY_DIRS})

# Don't prepend 'lib' to the names of modules built
set(CMAKE_SHARED_MODULE_PREFIX "")

# Create the cmake.py file used by all generators
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake.py.in
               ${CMAKE_CURRENT_BINARY_DIR}/cmake.py
               @ONLY)

macro(ADD_PYTHON_WRAPPER name generator_py_script)
    message("Hi, Dave!")
    add_library(${name} MODULE ${CMAKE_CURRENT_BINARY_DIR}/generated.cpp)

    set_source_files_properties(${CMAKE_CURRENT_BINARY_DIR}/generated.cpp
                                 PROPERTIES
                                   GENERATED
                                     TRUE)
    if(WIN32)
      set_target_properties(${name}
                              PROPERTIES
                                SUFFIX
                                  ".pyd")
    endif()

    add_custom_command(
            OUTPUT
              ${CMAKE_CURRENT_BINARY_DIR}/generated.cpp
            COMMAND
              ${CMAKE_COMMAND} -DCMAKE_PY_MODULE_DIR=${CMAKE_BINARY_DIR} -DGENERATOR_PY_SCRIPT=${generator_py_script} -P ${CMAKE_SOURCE_DIR}/generate_code.cmake
            DEPENDS
              ${CMAKE_BINARY_DIR}/cmake.py)
endmacro()


add_subdirectory(osg)
#add_subdirectory(osgDB)
#add_subdirectory(osgFX)
# etc., etc.
