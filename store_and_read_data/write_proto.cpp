#include <fstream>
#include "drone.pb.h"

int main() {
    DroneTelemetry d;
    d.set_drone_id(1);
    d.set_lat(32.05);
    d.set_lon(34.78);
    d.set_alt(120.5);
    d.set_vx(3.1f);
    d.set_vy(-1.2f);
    d.set_vz(0.4f);

    std::ofstream out("drone.pb", std::ios::binary);
    d.SerializeToOstream(&out);
}
