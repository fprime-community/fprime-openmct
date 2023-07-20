# fprime-openmct
Scripts to connect the F Prime ground system to OpenMCT

## Installation Instructions.
OpenMCT runs a server using Node JS, so Node must be installed. Node Version 18.17.0 works and is stable with OpenMCT.
### Install NVM (Node Version Manager)
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```
### Install Node 
```
nvm install v18.17.0
nvm alias default v18.17.0 # Make v18.17.0 default if you have multiple Node Versions on your system
```
### Install F-Prime OpenMCT Dependencies and OpenMCT from Source
```
npm install # from the root of the repository
```

## Running the F Prime OpenMCT Pipeline

### Starting the OpenMCT Server
```
npm start # from the root of the repository
```
### Subscribing and Publishing FPrime Telemetry via FPrime-GDS 
```
cd fprime_scripts
python fprime_telem_poller.py -d {path to F-Prime Topology App Dictionary XML} -l {Desired Path to Log Directory} -r 0.5
```
Going to localhost:8080 on a browser will show the F-Prime Telemetry Channels registered in the framework. 
