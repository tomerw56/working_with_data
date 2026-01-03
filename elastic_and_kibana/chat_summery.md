
# Filebeat + Elasticsearch + Kibana (End-to-End Log Analysis Demo)

This document shows a **clean, working Filebeat integration** based on the **official Elastic documentation**, adapted for a **Docker Compose demo**.  
It is suitable for teams that want to **analyze application logs** without deep database or Elastic internals knowledge.

---

## Architecture Overview

[ Application Logs ]
|
v
Filebeat
|
v
Elasticsearch ---> Kibana

yaml
Copy code

- **Filebeat** tails log files and ships events
- **Elasticsearch** stores and indexes logs
- **Kibana** provides search, visualization, dashboards

---

## Docker Compose Setup

### `docker-compose.yml`

```yaml
services:

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.3
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    ports:
      - "9200:9200"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.3
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.3
    user: root
    command: ["--strict.perms=false", "-e", "-c", "/usr/share/filebeat/filebeat.yml"]
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml
      - ./logs/app.log:/var/log/app.log
    depends_on:
      - elasticsearch
Why these settings?
xpack.security.enabled=false → simplifies local demo

--strict.perms=false → required on Windows / Git-mounted files

Explicit config path → avoids Filebeat auto-discovery issues

Filebeat Configuration
filebeat.yml
yaml
Copy code
filebeat.inputs:
  - type: filestream
    enabled: true
    paths:
      - /var/log/app.log
    parsers:
      - multiline:
          pattern: '^[[:space:]]'
          match: after

filebeat.config.modules:
  path: ${path.config}/modules.d/*.yml
  reload.enabled: false

output.elasticsearch:
  hosts: ["http://elasticsearch:9200"]

logging:
  level: info
  to_files: true
  files:
    path: /var/log/filebeat
    name: filebeat
    keepfiles: 7
    permissions: 0644
What this does
filestream input
Recommended by Elastic (replaces log input)

Multiline parsing
Correctly captures stack traces and multi-line errors

Direct Elasticsearch output
No Logstash required for simple demos

Persistent Filebeat logs
Useful for troubleshooting container exits

Running the Stack
bash
Copy code
docker compose up -d
Verify containers:

bash
Copy code
docker compose ps -a
Expected:

mathematica
Copy code
elasticsearch   Up
kibana          Up
filebeat        Up
If Filebeat exits:

bash
Copy code
docker logs filebeat
Viewing Logs in Kibana
Open Kibana
http://localhost:5601

Go to
Stack Management → Data Views

Create a Data View:

Name: filebeat-*

Time field: @timestamp

Open Discover
You should now see log events from app.log


Optional: Structured (JSON) Logs
If your application logs JSON, add this to filebeat.yml:

processors:
  - decode_json_fields:
      fields: ["message"]
      target: ""
      overwrite_keys: true