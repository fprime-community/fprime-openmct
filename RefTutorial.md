# Running the F-Prime to OpenMCT Pipeline on the Ref Deployment
In this tutorial we explore how to generate real time telemetry in OpenMCT on the Ref Deployment, which is a basic deployment present in F-Prime that is used to test basic functionality. 

This tutorial assumes the user has installed OpenMCT, the F-Prime OpenMCT pipeline, as well as `fprime_gds` and `fprime_tools`, as detailed in `README.md`. 

## Basic Setup
First, we clone the devel branch of F-Prime.
```
git clone https://github.com/nasa/fprime.git
```
Navigate to the Ref Directory, and generate a build directory using `fprime-util`.
```
cd Ref
fprime-util generate 
```
To build the `Ref` application's code, we use the `build` subcommand.
```
fprime-util build
```
The `Ref` Deployment binary has now been generated and is present under `build-artifacts/Darwin/bin`. The deployment dictionary defining commands, events, channels, and parameters is present under `build-artifacts/Darwin/dict` as `RefTopologyAppDictionary.xml`. This is the dictionary we will use in the F-Prime GDS to OpenMCT pipeline to process all of our telemetry. 

## Running the Ref Deployment and F-Prime GDS 
Navigate to the `Ref` directory. Run the following command:
```
fprime-gds
```
This will launch a web browser with the GDS, as well as the Ref deployment locally. You should see a green dot at the top right of the GDS webpage.

## Generating the OpenMCT JSON Telemetry Definitions and initial states
To generate our telemetry definitions and initial states in OpenMCT, we will need to use the `RefTopologyAppDictionary.xml` generated from our deployment build. 
```
cd fprime-openmct/fprime_scripts # Navigate to the directory where fprime-openmct is installed
python TopAppDictXMLtoOpenMCTJSON.py --dictionary {path to F-Prime Topology App Dictionary XML}
cd ..
npm start  #Start the OpenMCT Server
```

## Subscribing and Publishing FPrime Telemetry via F-Prime GDS 
To poll for realtime telemetry, we must run `fprime_telem_poller.py`. 
```
cd fprime_scripts
python fprime_telem_poller.py --dictionary {path to F-Prime Topology App Dictionary XML} 
```
Going to `localhost:8080` on a browser will show the F-Prime Telemetry Channels registered in the framework, outputting real time telemetry recieved. 



