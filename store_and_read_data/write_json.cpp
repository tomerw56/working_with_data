#include <fstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
    json j = {
        {"drone_id", 1},
        {"lat", 32.05},
        {"lon", 34.78},
        {"alt", 120.5},
        {"vx", 3.1},
        {"vy", -1.2},
        {"vz", 0.4}
    };

    std::ofstream out("drone.json");
    out << j.dump(2);
}
