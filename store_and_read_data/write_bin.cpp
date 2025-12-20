#include <fstream>
#include <cstdint>

#pragma pack(push, 1)
struct DroneTelemetry {
    uint32_t drone_id;
    double lat;
    double lon;
    double alt;
    float vx;
    float vy;
    float vz;
};
#pragma pack(pop)

int main() {
    DroneTelemetry d {
        1,
        32.05,
        34.78,
        120.5,
        3.1f,
        -1.2f,
        0.4f
    };

    std::ofstream out("drone.bin", std::ios::binary);
    out.write(reinterpret_cast<char*>(&d), sizeof(d));
}
