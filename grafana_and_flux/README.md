# grafana_and_flux
1/ use via wsl or linux ```docker compose up````
2/build venv using ```requirments.txt```
3/ you can now access
Grafana: http://localhost:3000
 (admin / admin)

InfluxDB: http://localhost:8086

4/ you can access InfluxDB with:
      USERNAME: admin
      PASSWORD: admin123
	  
5/ you can query some data using the query 
```
from(bucket: "drone")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "drone_telemetry")
  |> filter(fn: (r) => r._field == "lat" or r._field == "lon")
```
6/ grafana is preaty straight forward 
Add InfluxDB data source

Type: InfluxDB

Query language: Flux

URL: http://influxdb:8086

Organization: demo-org

Token: demo-token

Default bucket: drone

7/