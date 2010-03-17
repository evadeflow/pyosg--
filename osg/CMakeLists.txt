add_python_wrapper(osg generate.py)

target_link_libraries(osg
                        ${PYTHON_LIBRARIES}
                        ${OPENSCENEGRAPH_LIBRARIES}
                        ${Boost_LIBRARIES})
