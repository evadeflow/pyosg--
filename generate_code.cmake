find_package(PythonInterp REQUIRED)

# [TODO: prepend, don't overwrite]
set(ENV{PYTHONPATH} ${CMAKE_PY_MODULE_DIR})

execute_process(COMMAND
                 ${PYTHON_EXECUTABLE}
                   ${GENERATOR_PY_SCRIPT})
