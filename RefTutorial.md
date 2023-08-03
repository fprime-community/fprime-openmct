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




