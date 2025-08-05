# Verilog CP
A python Flask based platform to conduct Verilog contests
****NOTE: use linux based enironment***

##  Prerequisites
 - Python
 - Redis
 use the one of the below commands to isntall iverilog
 ```bash
sudo apt install iverilog 
```
or
```bash
sudo pacman -S iverilog
```
or
```bash
sudo dnf -y install iverilog
 ```

## Setting Up
run the script setup.sh in scripts folder
```bash
source ./scripts/setup.sh
```

## Running App
run the script run_flask.sh and run_celery.sh in scripts folder
```bash
source ./scripts/run_flask.sh
```
celery is not necessary for smaller design and test benches, and hence not used. in case it is needed minor changes has to be made in controller.py and worker.py
```bash
source ./scripts/run_celery.sh
```
**Run each  script concurrently in separate terminals**
**add the url to server url to the CORS (application.py line 45) and change the server in swagger (line 7 in .yaml) to use the swagger interface**

View API docs at [API docs](http://localhost:5000/api/docs/) (for testing) or at [https://<yourserver>/api/docs](https://<yourserver>/api/docs)
## Cleaning
****NOTE: This removes all data***
run the script clean.sh in scripts folder
```bash
source ./scripts/clean.sh
```

