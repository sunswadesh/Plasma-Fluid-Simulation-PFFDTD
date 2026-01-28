cmake_minimum_required(VERSION 3.10)
project(PFFDTD VERSION 1.8.2 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set default build type to Release
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# Cross-platform compiler detection
if(MSVC)
    message(STATUS "Using MSVC compiler (Windows)")
    add_compile_options(/W4)  # Warning level 4
    add_compile_options(/permissive-)  # Standards conformance
else()
    message(STATUS "Using GCC/Clang compiler (Unix-like)")
    add_compile_options(-Wall -Wextra -pedantic)
endif()

message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER}")
message(STATUS "C++ Version: ${CMAKE_CXX_STANDARD}")
message(STATUS "Platform: ${CMAKE_SYSTEM_NAME}")

# Source files
set(SOURCES
    pffdtd.cpp
)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Main executable - Debug
add_executable(pffdtd_debug ${SOURCES})
target_compile_options(pffdtd_debug PRIVATE
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-O0>        # No optimization (GCC/Clang)
    $<$<CXX_COMPILER_ID:MSVC>:/Od>               # No optimization (MSVC)
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-g>         # Debug symbols (GCC/Clang)
    $<$<CXX_COMPILER_ID:MSVC>:/Zi>               # Debug symbols (MSVC)
    -std=c++11
)
set_target_properties(pffdtd_debug PROPERTIES
    OUTPUT_NAME "pffdtd_debug"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin/debug"
)

# Main executable - Release
add_executable(pffdtd_release ${SOURCES})
target_compile_options(pffdtd_release PRIVATE
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-O3>        # Full optimization (GCC/Clang)
    $<$<CXX_COMPILER_ID:MSVC>:/O2>               # Full optimization (MSVC)
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-march=native> # Native architecture (GCC/Clang)
    $<$<CXX_COMPILER_ID:MSVC>:/arch:AVX2>       # AVX2 for MSVC
    -std=c++11
)
set_target_properties(pffdtd_release PROPERTIES
    OUTPUT_NAME "pffdtd_release"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin/release"
)

# Main executable - Profile (with gprof support on Unix, disabled on Windows)
add_executable(pffdtd_profile ${SOURCES})
if(NOT MSVC)
    target_compile_options(pffdtd_profile PRIVATE
        -O2           # Some optimization
        -g            # Debug symbols for profiling
        -pg           # gprof profiling
        -std=c++11
    )
    target_link_options(pffdtd_profile PRIVATE -pg)
else()
    target_compile_options(pffdtd_profile PRIVATE
        /O2           # Some optimization
        /Zi           # Debug symbols
    )
    message(STATUS "Profiling: Use Visual Studio profiler on Windows")
endif()
set_target_properties(pffdtd_profile PROPERTIES
    OUTPUT_NAME "pffdtd_profile"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin/profile"
)

# Main executable - OpenMP (Parallel)
find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    add_executable(pffdtd_parallel ${SOURCES})
    target_compile_options(pffdtd_parallel PRIVATE
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-O3>        # Full optimization (GCC/Clang)
        $<$<CXX_COMPILER_ID:MSVC>:/O2>               # Full optimization (MSVC)
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-fopenmp>   # OpenMP (GCC/Clang)
        $<$<CXX_COMPILER_ID:MSVC>:/openmp>           # OpenMP (MSVC)
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-march=native> # Native architecture (GCC/Clang)
        $<$<CXX_COMPILER_ID:MSVC>:/arch:AVX2>       # AVX2 for MSVC
        -std=c++11
    )
    target_link_libraries(pffdtd_parallel PRIVATE OpenMP::OpenMP_CXX)
    set_target_properties(pffdtd_parallel PROPERTIES
        OUTPUT_NAME "pffdtd_parallel"
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin/parallel"
    )
    message(STATUS "OpenMP found - parallel target enabled")
else()
    message(STATUS "OpenMP not found - parallel target disabled")
endif()

# Optional: GPU support (future)
# Uncomment when CUDA is available
# find_package(CUDA)
# if(CUDA_FOUND)
#     add_executable(pffdtd_gpu pffdtd_gpu.cu)
#     set_property(TARGET pffdtd_gpu PROPERTY CUDA_STANDARD 11)
#     message(STATUS "CUDA found - GPU target enabled")
# endif()

# Print configuration summary
message(STATUS "")
message(STATUS "=== PFFDTD Cross-Platform Build Configuration ===")
message(STATUS "Version: ${PROJECT_VERSION}")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Platform: ${CMAKE_SYSTEM_NAME}")
message(STATUS "Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "")
message(STATUS "Targets available:")
message(STATUS "  - pffdtd_debug    (Unoptimized, debug symbols, all warnings)")
message(STATUS "  - pffdtd_release  (Full optimization, production use)")
message(STATUS "  - pffdtd_profile  (Optimized with profiling support)")
if(OpenMP_CXX_FOUND)
message(STATUS "  - pffdtd_parallel (Multi-threaded with OpenMP)")
endif()
message(STATUS "")
message(STATUS "Build with: cmake --build . --config ${CMAKE_BUILD_TYPE}")
message(STATUS "Or use: cmake --build . --target pffdtd_debug")
message(STATUS "")

# Installation targets
install(TARGETS pffdtd_release
    RUNTIME DESTINATION bin
)

# Custom targets for convenience
add_custom_target(all_variants
    DEPENDS pffdtd_debug pffdtd_release pffdtd_profile
    COMMENT "Building all variants..."
)

if(OpenMP_CXX_FOUND)
    add_dependencies(all_variants pffdtd_parallel)
endif()

# Help target
add_custom_target(help
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_SOURCE_DIR}/cmake_help.txt 2>/dev/null || echo "CMake help: Run 'cmake --build . --target <target_name>'"
    COMMENT "Available targets:"
)
