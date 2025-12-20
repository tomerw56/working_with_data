# Demo for file saving
the cmake uses vcpgk
```
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
bootstrap-vcpkg.bat
vcpkg install nlohmann-json protobuf:x64-windows
vcpkg integrate install

```
to run the cmake use
```
rmdir /s /q build
cmake -S . -B build ^
  -G "Visual Studio 17 2022" ^
  -A x64 ^
  -DCMAKE_TOOLCHAIN_FILE=<vcpkg folder>/scripts/buildsystems/vcpkg.cmake
cmake --build build --config Release
```

the protoc is located on ```<vcpkg folder>\installed\x64-windows\tools\protobuf```
in order to genarte the proto files use 
```<protoc folder>\protoc.exe --python_out=. drone.proto```
```<protoc folder>\protoc.exe --cpp_out=. drone.proto```


