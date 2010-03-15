# FIXME: Move all this into a top-level macro so that this file only
# contains:
#
# ADD_WRAPPER(osg)
#
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/generate_code.py.in
               ${CMAKE_CURRENT_BINARY_DIR}/generate_code.py
               @ONLY)

add_library(osg MODULE ${CMAKE_CURRENT_BINARY_DIR}/generated.cpp)

set_source_files_properties(${CMAKE_CURRENT_BINARY_DIR}/generated.cpp
                             PROPERTIES
                               GENERATED
                                 TRUE)
if(WIN32)
  set_target_properties(osg
                          PROPERTIES
                            SUFFIX
                              ".pyd")
endif()

target_link_libraries(osg ${PYTHON_LIBRARIES} ${OPENSCENEGRAPH_LIBRARIES})

add_custom_command(
        OUTPUT
          ${CMAKE_CURRENT_BINARY_DIR}/generated.cpp
        COMMAND
          ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/generate_code.py
        DEPENDS
          generate_code.py.in)
