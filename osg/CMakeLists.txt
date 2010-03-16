ADD_PYTHON_WRAPPER(osg ${CMAKE_CURRENT_SOURCE_DIR}/generate_code.py)

target_link_libraries(osg
                        ${PYTHON_LIBRARIES}
                        ${OPENSCENEGRAPH_LIBRARIES}
                        ${Boost_LIBRARIES})
