# Top-level CMakeLists.txt file for PyOSG++
#
# I typically configure with a command similar to the following:
#
#  c:\d\PyOSG++\build>cmake -DCMAKE_INCLUDE_PATH=c:\pt\externals\include \
#   -DCMAKE_LIBRARY_PATH=c:\pt\externals\lib \
#   -DCMAKE_PREFIX_PATH="C:\Program Files (x86)\gccxml 0.9\bin" ..
#
cmake_minimum_required(VERSION 2.6)

project(PyOSG++)

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
find_package(Boost 1.36.0 REQUIRED COMPONENTS python)
find_package(GCCXML REQUIRED)
find_package(OpenSceneGraph REQUIRED)
find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)

if(WIN32)
  # Set a few platform conditionals needed by OSG
  # (TODO: Check what, if anything, is required on Linux)
  set(GCCXML_DEFINES "'_MSCVER', 'WIN32'")

  # Tell gccxml which version of Visual Studio to simulate
  if(MSVC80)
    set(GCCXML_COMPILER "msvc8")
  elseif(MSVC71)
    set(GCCXML_COMPILER "msvc71")
  else()
    set(GCCXML_COMPILER "\"\"")
  endif()
else()
    set(GCCXML_COMPILER "g++")
endif()

include_directories(${PYTHON_INCLUDE_PATH}
                    ${Boost_INCLUDE_DIR}
                    ${OSG_INCLUDE_DIR})

link_directories(${Boost_LIBRARY_DIRS})

add_subdirectory(osg)
#add_subdirectory(osgDB)
#add_subdirectory(osgFX)
# etc., etc.
