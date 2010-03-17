add_python_wrapper(osg ${CMAKE_CURRENT_SOURCE_DIR}/generate.py)

target_link_libraries(osg
                        ${PYTHON_LIBRARIES}
                        ${OPENSCENEGRAPH_LIBRARIES}
                        ${Boost_LIBRARIES})
