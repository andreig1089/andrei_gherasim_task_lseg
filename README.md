# Solution
## Prerequisites and setup

The following will describe the prerequisites needed to deploy the code and the installation steps.
Since this was developed and tested in a linux environment, here are the installation steps for Ubuntu with Python3.10:

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

sudo apt install python3.10 python3-pip python3-venv
```
run the following to set up the environment
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
```

> ⚠ **Note:** If the installation of the venv fails, remove the versions from the requirements file.

## Server

This will start a flask app that has 2 endpoints
To run it (in bg):

```sh
nohup python server.py > logs/server.log &
```

## CLI app

This script makes it easier to access the api:

```sh
python cli.py
```
and then follow the menu.  
It should display this:
```sh
Select an option:
1. Get the 10 consecutive values.
2. Predict the next 3 values.
d. describe
q. quit
```
Options 1 and 2 will prompt the number of files to export as an input.  
Finally, if you wish, the output can be saved to the provided path.  
If successful, a run will save the result to the outputs directory.
If not, the results of the old run will remain in the outputs directory.

## Outputs

All the prediction results will be stored in the outputs directory.

## Cleanup

```sh
# assuming is the only python process
pkill python 

deactivate
rm -rf venv
```

# Notes

- This is not ready for production.
- Logs of the app are stored in the logs folder. Some of the warnings may appear in the log file.
- In this solution, I tried to use native python modules as much as possible. Using pandas and numpy would have helped.
