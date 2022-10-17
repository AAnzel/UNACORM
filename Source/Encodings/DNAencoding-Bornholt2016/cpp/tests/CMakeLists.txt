include(${CMAKE_SOURCE_DIR}/cmake/googletest.cmake)

file(GLOB TEST_FILES "*.cpp")

add_executable(${LIB_TESTS_NAME} ${TEST_FILES})

target_link_libraries(${LIB_TESTS_NAME} ${LIB_NAME} gtest gtest_main)
