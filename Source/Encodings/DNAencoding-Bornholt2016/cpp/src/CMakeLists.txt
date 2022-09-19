file(GLOB HEADER_FILES "${CMAKE_SOURCE_DIR}/cpp/include/${LIB_NAME}/*.hpp")
file(GLOB SOURCE_FILES "${CMAKE_SOURCE_DIR}/cpp/src/*.cpp")

add_library(${LIB_NAME} SHARED ${SOURCE_FILES} ${HEADER_FILES})

target_include_directories(${LIB_NAME} PUBLIC "${CMAKE_SOURCE_DIR}/cpp/include/")
