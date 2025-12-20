cmake_minimum_required(VERSION 3.21)
project(drone_serialization_demo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ---- Protobuf ----
find_package(Protobuf CONFIG REQUIRED)

protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS drone.proto)

# ---- Binary demo ----
add_executable(write_bin write_bin.cpp)
target_compile_features(write_bin PRIVATE cxx_std_17)

# ---- JSON demo ----
find_package(nlohmann_json CONFIG REQUIRED)

add_executable(write_json write_json.cpp)
target_link_libraries(write_json PRIVATE nlohmann_json::nlohmann_json)

# ---- Protobuf demo ----
add_executable(write_proto
    write_proto.cpp
    ${PROTO_SRCS}
    ${PROTO_HDRS}
)

target_link_libraries(write_proto PRIVATE protobuf::libprotobuf)
target_include_directories(write_proto PRIVATE ${Protobuf_INCLUDE_DIRS})
