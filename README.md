# Handball task API

* **Usage**
+ Using docker
  -Clone git repository
  ```sh
  -cd handball && docker-compose up
  ```
  -runs app on http://localhost:8001/
+ Manually
  ```sh
  -git clone https://github.com/Vimdar/handball_task
  ```
  -ensure latest psql version is installed
  -create psql user/database from settings.conf or use init.sql file in repo
  -pip install requirements.txt
  -run django migrations
  -run django dev server
+ Sending results
  ```sh
curl -i -H "Content-Type: application/json" -X POST --data '{"data": "Denmark | Belgium | 0:0 | 1:1\nBelgium | Austria | 2:0 | 0:2\nLatvia | Monaco | 2:0 | 0:0\nBulgaria | Italy | 2:1 | 3:2\nstop"}' http://localhost:8001/results_endpoint/

curl -i -H "Content-Type: application/json" -X POST --data '{"data": "Montenegro | Cyprus | 0:0 | 1:1\nMontenegro | Bosnia | 0:0 | 1:1\nMontenegro | South Africa | 0:0 | 1:1\nstop"}' http://localhost:8001/results_endpoint/

curl -i -H "Content-Type: application/json" -X POST --data '{"data": "Brazil | Germany | 1:1 | 7:0\nstop"}' http://localhost:8001/results_endpoint/
```