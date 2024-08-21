file(GLOB HEADER_FILES "${CMAKE_SOURCE_DIR}/cpp/include/${LIB_NAME}/*.hpp")
file(GLOB SOURCE_FILES "${CMAKE_SOURCE_DIR}/cpp/src/*.cpp")

add_library(${LIB_NAME} STATIC ${SOURCE_FILES} ${HEADER_FILES})

target_include_directories(${LIB_NAME} PUBLIC "${CMAKE_SOURCE_DIR}/cpp/include/")

# allow linking static library with python module
set_target_properties(${LIB_NAME} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
