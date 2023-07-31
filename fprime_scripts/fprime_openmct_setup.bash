# Generate the OpenMCT from the Topology App Dictionary XML
python TopAppDictXMLtoOpenMCTJSON.py -f ../{FPrimeTopologyAppDictionary}.xml
sleep(3)

#Poll for F-Prime Telemetry continuously
python fprime_telem_poller.py -d ../{FPrimeTopologyAppDictionary}.xml
