### how to run

1. install requirments via pip 
2. docker up ```docker compose up -d```
3. docker down ```docker compose down -v```
4. python the log activation creation -update the path i suggest

i suggest reading the chat readme for finding how to use the kilbana
but if all works ont the docker side 

Open Kibana

http://localhost:5601

Go to

Stack Management → Data Views

Create a data view matching:

filebeat-*


Choose the @timestamp field.

add your dashbord