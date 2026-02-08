include(FetchContent)

FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/v1.14.0.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

FetchContent_MakeAvailable(googletest)

enable_testing()

# Link to the main library (need to separate main() from pffdtd.cpp first? 
# or just test independent modules for now. 
# pffdtd.cpp currently contains main() so it can't be linked directly into another executable defining main)
# We will test modules like constants, utils, etc.

# Add unit tests executable
add_executable(unit_tests
  unit/test_constants.cpp
  # Add other test files here
)

target_include_directories(unit_tests PRIVATE ${CMAKE_SOURCE_DIR}/src)

target_link_libraries(unit_tests GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(unit_tests)
