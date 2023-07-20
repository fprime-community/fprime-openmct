import argparse

from fprime_gds.common.pipeline.standard import StandardPipeline
from fprime_gds.common.utils.config_manager import ConfigManager
from fprime_gds.common.history.chrono import ChronologicalHistory

import requests 
import time 

import json



class TelemPipeline(StandardPipeline):
    """
    The Telemetry Pipeline class inherits from the F-Prime GDS Standard Pipeline Object for Telemetry Polling.
    It includes the following data members:

    1. StandardPipeline member variables -> Includes Dictionaries, Coders, Object History, Filing, and Transport Info
    2. telem_chron_hist -> Chronological History Object that will request new telemetry
    3. telem_hist -> List where raw telemetry objects requested by telem_chron_hist will be stored
    4. telem_data -> Contains list of processed telemetry objects in the format that OpenMCT will accept
    5. telem_init_states -> Contains dictionary of telemetry object names and their immediate value. Used to initialize values and define the telemetry states to be processed by OpenMCT server 
    6. telem_init_json -> Contains JSON of telemetry object names and their value. Saved in OpenMCT directory and used by OpenMCT server to define initial telemetry states.
    7. max_state_count -> Used to keep count of the largest number telemetry objects recieved by the pipeline in a single telemetry request
    8. json_writeable -> Used to determine if heli_states contains telemetry information. If true, the data can be written to a JSON that OpenMCT will accept
    """
    def __init__(self, connection_ip="127.0.0.1", connection_port=50050, dict_path="", log_path=""):
        StandardPipeline.__init__(self)
        self.setup(ConfigManager(), dict_path, log_path)
        self.connect(connection_ip, connection_port)
        self.telem_chron_hist = ChronologicalHistory()
        self.coders.register_channel_consumer(self.telem_chron_hist)
        self.telem_hist = []
        self.telem_data = []
        self.telem_init_states = {}
        self.telem_init_json = {}
        self.max_state_count = 0
        self.json_writeable = False

    def get_telem_hist(self):
        return self.telem_hist

    def update_telem_hist(self):
        self.telem_hist = self.telem_chron_hist.retrieve_new()
        if (len(self.telem_hist) > self.max_state_count):
            self.max_state_count = len(self.telem_hist)

    def set_telem_json(self):
        self.telem_data = []
        for hist in self.telem_hist:
            hist_name = str(hist.template.comp_name) + '.' + str(hist.template.name)

            hist_data = {
                        'name': hist_name, 
                        'data': {
                                'id':hist.id,
                                'val':hist.get_val(),
                                'time':hist.time.to_readable()
                                }
                        }
            
            if not self.json_writeable:
                self.telem_init_states[hist_name] = hist.get_val()
                self.json_writeable = True

            self.telem_data.append(hist_data)

    def write_telem_json(self, fname="openmct/initial_states.json"):
        self.telem_init_json = json.dumps(self.telem_init_states, indent=4)
        with open(fname, "w") as outfile:
            outfile.write(self.telem_init_json)

    def post_telem(self, uri="http://127.0.0.1:4052/fprime_telem"):
        requests.post(uri, json={'name': 'heli', 'telem': self.telem_data}) 


#Set up and Process Command Line Arguments
parser = argparse.ArgumentParser('Post F-Prime Telemetry Captured from F-Prime GDS to a Server to be Read by OpenMCT')
parser.add_argument('-d', '--dict-path', dest='dict_path', type=str, required=True, help='Input file path to F-Prime Topology App Dictionary File')
parser.add_argument('-l', '--log-path', dest='log_path', type=str, required=True, help='Path to store F-Prime Telemetry logs')
parser.add_argument('--ip-address', dest='ip_address', type=str, required=False, default='127.0.0.1', help="IP Address of the F-Prime GDS TCP Socket Server")
parser.add_argument('--ip-port', dest='ip_port', type=int, required=False, default=50050, help='Port Number of the F-Prime GDS TCP Socket Server')
parser.add_argument('--openmct-uri', dest='openmct_uri', type=str, required=False, default="http://127.0.0.1:4052/fprime_telem", help="URI of the OpenMCT Server. The URI at which the F-Prime telemetry will be broadcasted.")
parser.add_argument('--openmct-dir', dest='openmct_dir', type=str, required=False, default='', help="Directory where the OpenMCT Server is located")
parser.add_argument('-r', '--telem-rate', dest='telem_rate', type=float, required=False, default=1, help="Rate(in Hz) at which we want to poll the Telemetry Pipeline for new telemetry")
args = parser.parse_args()



# instantiate the GDS and connect to the Deployment
telem_pipeline = TelemPipeline(connection_ip=args.ip_address, 
                               connection_port=args.ip_port,
                               dict_path=args.dict_path,
                               log_path=args.log_path)

# Continuously poll for telemetry from the F-Prime GDS Pipeline
write_json = True
while True:

    #Write initial states to initial_states.json and save it in the user-specified OpenMCT directory
    if telem_pipeline.json_writeable and write_json:
        telem_pipeline.write_telem_json(args.openmct_dir + "initial_states.json")
        write_json = False

    #Poll the F-Prime GDS Pipeline for telemetry, and update the latest telemetry JSON
    telem_pipeline.update_telem_hist() 
    telem_pipeline.set_telem_json()
    
    #Post Telemetry Information to the server address OpenMCT is listening on
    telem_pipeline.post_telem(args.openmct_uri)

    time.sleep(1/args.telem_rate)


