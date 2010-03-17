function(add_python_wrapper wrapper_name generator_name)
    set(bindings_file
        ${CMAKE_CURRENT_BINARY_DIR}/${wrapper_name}_bindings.cpp)

    add_library(${wrapper_name} MODULE ${bindings_file})

    set_source_files_properties(${bindings_file}
                                 PROPERTIES
                                   GENERATED
                                     TRUE)
    if(WIN32)
      set_target_properties(${wrapper_name}
                              PROPERTIES
                                SUFFIX
                                  ".pyd")
    endif()

    add_custom_command(
            OUTPUT
              ${bindings_file}
            COMMAND
              ${CMAKE_COMMAND} -DPY_MODULE_DIR=${CMAKE_BINARY_DIR}
              -DPYPP_SCRIPT=${CMAKE_CURRENT_SOURCE_DIR}/${generator_name}
              -P ${CMAKE_SOURCE_DIR}/CMakeModules/generate.cmake
            COMMENT
              Generating ${bindings_file}
            DEPENDS
              ${CMAKE_BINARY_DIR}/cmake.py)
endfunction()

function(create_cmake_py_module)
    if(WIN32)
      # Set a few platform conditionals needed by gccxml when parsing OSG headers
      set(GCCXML_DEFINES "_MSCVER WIN32")

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

    # Create the cmake.py file used by all generators
    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake.py.in
                   ${CMAKE_CURRENT_BINARY_DIR}/cmake.py
                   @ONLY)
endfunction()
