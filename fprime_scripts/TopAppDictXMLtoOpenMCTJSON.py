import argparse
import xml.etree.ElementTree as ET

from fprime_gds.common.pipeline.dictionaries import Dictionaries
import json

class DictionaryIngester:
    """
    The Dictionary Ingester class intends to take the F-Prime Topology App Dictionary XML and convert it to Python Dictionaries for commands, events, channels, and parameters
    It includes the following data members:

    1. root -> Contains root(top level) of Topology App XML Tree
    2. types -> One level lower from the root. Contains type information stored in the Topology App XML
    3. enums -> Defines enumeration types from the Topology App XML
    4. serializables -> Defines serializable types from the Topology App XML
    5. commands -> Defines commands from the Topology App XML
    6. events -> Defines events from the Topology App XML
    7. channels -> Defines channels from the Topology App XML
    8. parameters -> Defines parameters from the Topology App XML
    """
    def __init__(self, root):
        self._root = root
        self._types = self.traverseLevel(self._root)
        self._enums = self.formulateEnum(self.traverseLevel(self._types[0]))
        self._serializables = self.traverseLevel(self._types[1])
        self._commands = self.traverseLevel(self._types[3])
        self._events = self.traverseLevel(self._types[4])
        self._channels = self.traverseLevel(self._types[5])
        self._parameters = self.traverseLevel(self._types[6])

    def traverseLevel(self, level):
        sub_list = []
        for sublevel in level:
            sub_list.append(sublevel)
        return sub_list
    
    # Formulates the Enum dictionary based on the format specified by OpenMCT
    def formulateEnum(self, enums):
        enum_list = []
        for enum in enums:
            enum_entry = {}
            enum_entry['type'] = enum.attrib['type']
            #print((enum.tag, enum.attrib))
            enum_subentry_list = []
            for enu in enum:
                enum_subentry = {}
                enum_subentry['string'] = enu.attrib['name']
                enum_subentry['value'] = int(enu.attrib['value'])
                #print((enu.tag, enu.attrib))
                enum_subentry_list.append(enum_subentry)
            enum_entry['val'] = enum_subentry_list
            enum_list.append(enum_entry)
        return enum_list

class TopologyAppDictionaryJSONifier():
    """
    The Topology App Dictionary JSONifier class takes a python dictionary of F-Prime Telemetry Definitions and Converts it to the OpenMCT Definition
    It includes the following data members:

    1. int_type_list -> List of F-Prime Int Types
    2. float_type-list -> List of F-Prime Float Types
    3. framework_list -> List of F-Prime Framework Strings
    4. measurement_list -> List of F-Prime Telemetry Measurements
    5. dict_enum -> F-Prime Dictionary for F-Prime Enum Definitions
    6. dict_test -> F-Prime Dictionary for F-Prime Commands, Events, Telem Channels, and Parameters
    7. channel_list -> List of F-Prime Telemetry Channel Definitions
    8. heli_dict -> OpenMCT-formatted Dictionary of F-Prime Telemetry Channel Information

    """
    def __init__(self, xml_path='MPPTDeploymentTopologyAppDictionary.xml'):
        self.__int_type_list = ['U64Type', 'U32Type', 'U16Type', 'U8Type', 'I64Type', 'I32Type', 'I16Type', 'I8Type']
        self.__float_type_list = ['F64Type', 'F32Type']
        self.__framework_list = ['::FRAMEWORK_VERSIONString']
        self.__measurement_list = []

        #Formulate dict from XML Tree to get enum decomposition
        tree = ET.parse(xml_path)
        root = tree.getroot()
        self.__dict_enum = DictionaryIngester(root)

        self.__dict_test = Dictionaries()
        self.__dict_test.load_dictionaries(xml_path, packet_spec=None)
        self.__channel_list  = self.__dict_test.channel_id

        #Populate the measurement list  
        self.loadEntries()

        self.__heli_dict = {}
        self.__heli_dict['name'] = xml_path.replace('.xml', '')
        self.__heli_dict['key'] = xml_path.replace('.xml', '')
        self.__heli_dict['measurements'] = self.__measurement_list

    # Load Telemetry Channel List and format it to be in the OpenMCT Dictionary Format
    def loadEntries(self):
        for channel_num, channel_obj in self.__channel_list.items():
            measurement_entry = {}
            measurement_entry['values'] = [{}, {}]
            #print(channel_num, channel_obj)
            #if(isinstance())
            #print(channel_obj.ch_type_obj.__name__)
            measurement_entry['name'] = channel_obj.name
            measurement_entry['key'] = channel_obj.comp_name + '.' + channel_obj.name 
            measurement_entry['values'][0]['key'] = "value" #channel_obj.id
            measurement_entry['values'][0]['name'] = "Value" #channel_obj.name
            if(channel_obj.ch_type_obj.__name__ in self.__float_type_list):
                measurement_entry['values'][0]['format'] = 'float'
            elif(channel_obj.ch_type_obj.__name__ in self.__int_type_list):
                measurement_entry['values'][0]['format'] = 'integer'
            elif (channel_obj.ch_type_obj.__name__ in self.__framework_list):
                continue
            else:
                measurement_entry['values'][0]['format'] = 'enum'

            
            if(measurement_entry['values'][0]['format'] == 'enum'):
                for enum_vals in self.__dict_enum._enums:
                    if(enum_vals['type'] == channel_obj.ch_type_obj.__name__):
                        measurement_entry['values'][0]['enumerations'] = enum_vals['val']


            measurement_entry['values'][0]['hints'] = {}
            measurement_entry['values'][0]['hints']['range'] = 1

            measurement_entry['values'][1]['key'] = 'utc'
            measurement_entry['values'][1]['source'] = 'timestamp'
            measurement_entry['values'][1]['name'] = 'Timestamp'
            measurement_entry['values'][1]['format'] = 'utc'
            measurement_entry['values'][1]['hints'] = {}
            measurement_entry['values'][1]['hints']['domain'] = 1

            self.__measurement_list.append(measurement_entry)    

    #Write OpenMCT dictionary to a JSON file
    def writeJSON(self, fname):
        heli_json = json.dumps(self.__heli_dict, indent=4)
        with open(fname + ".json", "w") as outfile:
            outfile.write(heli_json)                 

#Set up and Process Command Line Arguments
parser = argparse.ArgumentParser('Convert F-Prime Topology App Dictionary XML to OpenMCT JSON Format')
parser.add_argument('-f', '--file', dest='file', type=str, required=False, default='FPrimeDeploymentTopologyAppDictionary.xml', help='Input file path to F-Prime Topology App Dictionary File')
parser.add_argument('-o', '--output-dir', dest='output_dir', required=False, default='', help='Output file directory to write JSON to')
args = parser.parse_args()

#Convert Topology App Dictionary XML file to an OpenMCT JSON 
top_dict = TopologyAppDictionaryJSONifier(args.file)
top_dict.writeJSON(args.file.replace('.xml', ''))


