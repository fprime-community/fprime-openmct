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
![alt text](https://github.com/mohitsingh999/fprime-openmct/blob/devel/images/RefDeploymentGDS.png)

## Generating the OpenMCT JSON Telemetry Definitions and initial states
To generate our telemetry definitions and initial states in OpenMCT, we will need to use the `RefTopologyAppDictionary.xml` generated from our deployment build. 
```
cd fprime-openmct/telem_definition_generator # Navigate to the directory where fprime-openmct is installed
python TopAppDictXMLtoOpenMCTJSON.py --dictionary {path to F-Prime Topology App Dictionary XML}
cd ..
npm start  #Start the OpenMCT Server
```

## Subscribing and Publishing FPrime Telemetry via F-Prime GDS 
To poll for realtime telemetry, we must run `fprime_telem_poller.py`. 
```
cd telem_poller
python fprime_telem_poller.py --dictionary {path to F-Prime Topology App Dictionary XML} 
```
Going to `localhost:8080` on a browser will show the F-Prime Telemetry Channels registered in the framework, outputting real time telemetry recieved. 
![alt text](https://github.com/mohitsingh999/fprime-openmct/blob/devel/images/RefDeploymentOpenMCTTelemChannels.png)

## Viewing OpenMCT Telemetry
Click on the BD_Cycles Telemetry icon to see an example of telemetry. You should see the following display. 
![alt text](https://github.com/mohitsingh999/fprime-openmct/blob/devel/images/RefDeploymentOpenMCTTelemBDCycles.png)
The default time mode is OpenMCT is `Fixed Timespan`, does not have the x axis of the plots moving along with the data coming in. To get Real Time Telemetry and have the time axis on the telemetry plots be constantly updated, click on the `Fixed Timestamp` Icon on the bottom left of the plot and switch to `Local Clock`. The x axis will now move with respect to time. In addition, changing the `History` icon to be `1 Minute` instead of the default `1 hour` can allow users to see the most up to date telemetry. Here is an example of `BD_Cycle` telemetry using `Local Clock` with a `History` of `1 Minute`. 
![alt text](https://github.com/mohitsingh999/fprime-openmct/blob/devel/images/RefDeploymentOpenMCTTelemRealTime1MinBDCycles.png)
OpenMCT also gives users access to a wide variety of ways of viewing Telemetry, in addition to the standard plots as a function of time. Using the create plot on the top right, users can create layouts and add widgets such as Gauges, Bar Graphs, Stacked/Overlay Plots, and Tables.


![alt text](https://github.com/mohitsingh999/fprime-openmct/blob/devel/images/RefDeploymentOpenMCTTelemPlugins.png)





