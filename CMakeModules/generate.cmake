#  This tiny script is used to run the py++ script that generates python
#  bindings for a module.  It only exists so that PYTHONPATH can be set prior
#  to running python. Using a 'sub-cmake' appears to be the only way to
#  achieve this. Per the CMake FAQ:
#
#      ... environment variables set in the CMakeLists.txt only take effect
#      for cmake itself, so you cannot use this method to set an environment
#      variable that a custom command might need.
#
#  Thus, setting PYTHONPATH before calling add_custom_command() in the main
#  CMakeLists.txt file doesn't work.  However, we can do an end-run around
#  this limitation by having the custom command 'shell out' to this script
#  using 'cmake -P'.
#
#  Two '-D' arguments should be passed to this script:
#
#    PY_MODULE_DIR: the directory containing our custom cmake.py module
#      PYPP_SCRIPT: the py++ generator script to be run
#
#  The syntax for adding this script as the COMMAND block for
#  add_custom_command() should look something like this:
#
#          COMMAND
#             ${CMAKE_COMMAND} -DPY_MODULE_DIR=${CMAKE_BINARY_DIR}
#             -DPYPP_SCRIPT=${CMAKE_CURRENT_SOURCE_DIR}/generate.py
#             -P ${CMAKE_SOURCE_DIR}/generate.cmake
#
#  Note that the '-P' argument must come *after* the '-D' args.
#
#  You may have noticed that the name of the generator script is *always*
#  'generate.py', regardless of which module we're binding, and that cmake.py
#  is *always* in CMAKE_BINARY_DIR.  Why, then, pass arguments to this script
#  at all?  The reason is that CMAKE_CURRENT_SOURCE_DIR and CMAKE_BINARY_DIR
#  behave differently when in a 'sub-cmake'; they both have the same value
#  that CMAKE_CURRENT_BINARY_DIR would have in the top-level cmake file.
#
find_package(PythonInterp REQUIRED)
set(ENV{PYTHONPATH} ${PY_MODULE_DIR})
execute_process(COMMAND ${PYTHON_EXECUTABLE} ${PYPP_SCRIPT})
