import xml.etree.ElementTree as ET

from fprime_gds.common.pipeline.dictionaries import Dictionaries
from fprime_gds.executables.cli import ParserBase, StandardPipelineParser
import json

class EnumIngester:
    """
    The Enum Ingester class intends to take the F-Prime Topology App Dictionary XML and generate Enum Definitions in the OpenMCT Format
    It includes the following data members:

    1. root -> Contains root(top level) of Topology App XML Tree
    2. types -> One level lower from the root. Contains type information stored in the Topology App XML
    3. enums -> Defines enumeration types from the Topology App XML
    """
    def __init__(self, root):
        self.__int_type_list = ['U64', 'U32', 'U16', 'U8', 'I64', 'I32', 'I16', 'I8']
        self.__float_type_list = ['F64', 'F32']
        self._serializables_type_list = ['']
        self._root = root
        self._types = self.traverseLevel(self._root)
        self._enums = self.formulateEnum(self.traverseLevel(self._types[0]))
        self._init_serializables = {}
        self._serializables = self.formulateSerializable(self.traverseLevel(self._types[1]))



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
    
    def formulateSerializable(self, serializables):
        serializable_entries = []
        for serializable in serializables:
            self._serializables_type_list.append(serializable.attrib['type'])
            for members in serializable:
                for member in members:
                    serializable_entry = {}
                    #print((member.tag, member.attrib))
                    serializable_entry['name'] = serializable.attrib['type'] #serializable.attrib['type'][serializable.attrib['type'].find('::'):].replace('::', '') + '.' + member.attrib['name']
                    serializable_entry['key'] = member.attrib['name']
                    serializable_entry['values'] = [{}, {}]
                    serializable_entry['values'][0]['key'] = "value" #channel_obj.id
                    serializable_entry['values'][0]['name'] = "Value" #channel_obj.name
                    if(member.attrib['type'] in self.__float_type_list):
                        serializable_entry['values'][0]['format'] = 'float'
                        self._init_serializables[serializable_entry['name']] = 0.0
                    elif(member.attrib['type'] in self.__int_type_list):
                        serializable_entry['values'][0]['format'] = 'integer'
                        self._init_serializables[serializable_entry['name']] = 0
                    else:
                        serializable_entry['values'][0]['format'] = 'enum'

                    if(serializable_entry['values'][0]['format'] == 'enum'):
                        for enum_vals in self._enums:
                            if(enum_vals['type'] == member.attrib['type']):
                                serializable_entry['values'][0]['enumerations'] = enum_vals['val']
                                self._init_serializables[serializable_entry['name']] = enum_vals['val'][0]['string']

                    serializable_entry['values'][0]['hints'] = {}
                    serializable_entry['values'][0]['hints']['range'] = 1

                    serializable_entry['values'][1]['key'] = 'utc'
                    serializable_entry['values'][1]['source'] = 'timestamp'
                    serializable_entry['values'][1]['name'] = 'Timestamp'
                    serializable_entry['values'][1]['format'] = 'utc'
                    serializable_entry['values'][1]['hints'] = {}
                    serializable_entry['values'][1]['hints']['domain'] = 1

                    serializable_entries.append(serializable_entry)


        return serializable_entries

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
    8. openmct_telem_dict -> OpenMCT-formatted Dictionary of F-Prime Telemetry Channel Information

    """
    def __init__(self, xml_path='MPPTDeploymentTopologyAppDictionary.xml'):
        self.__int_type_list = ['U64Type', 'U32Type', 'U16Type', 'U8Type', 'I64Type', 'I32Type', 'I16Type', 'I8Type']
        self.__float_type_list = ['F64Type', 'F32Type']
        self.__framework_list = ['::FRAMEWORK_VERSIONString']
        self.__measurement_list = []

        self.__init_states = {}

        #Formulate dict from XML Tree to get enum decomposition
        tree = ET.parse(xml_path)
        root = tree.getroot()
        self.__dict_xml = EnumIngester(root)

        self.__serializable_list = self.__dict_xml._serializables_type_list

        self.__dict_test = Dictionaries()
        self.__dict_test.load_dictionaries(xml_path, packet_spec=None)
        self.__channel_list  = self.__dict_test.channel_id

        #Populate the measurement list  
        self.loadEntries()

        self.__openmct_telem_dict = {}
        self.__openmct_telem_dict['name'] = xml_path.replace('.xml', '')
        self.__openmct_telem_dict['key'] = xml_path.replace('.xml', '')
        self.__openmct_telem_dict['measurements'] = self.__measurement_list

    # Load Telemetry Channel List and format it to be in the OpenMCT Dictionary Format
    def loadEntries(self):

        for channel_num, channel_obj in self.__channel_list.items():
            measurement_entry = {}
            measurement_entry['values'] = [{}, {}]

            measurement_entry['name'] = channel_obj.name
            measurement_entry['key'] = channel_obj.comp_name + '.' + channel_obj.name 
            measurement_entry['values'][0]['key'] = "value" #channel_obj.id
            measurement_entry['values'][0]['name'] = "Value" #channel_obj.name
            measurement_entry['values'][0]['hints'] = {}
            measurement_entry['values'][0]['hints']['range'] = 1

            measurement_entry['values'][1]['key'] = 'utc'
            measurement_entry['values'][1]['source'] = 'timestamp'
            measurement_entry['values'][1]['name'] = 'Timestamp'
            measurement_entry['values'][1]['format'] = 'utc'
            measurement_entry['values'][1]['hints'] = {}
            measurement_entry['values'][1]['hints']['domain'] = 1

            if(channel_obj.ch_type_obj.__name__ in self.__float_type_list):
                measurement_entry['values'][0]['format'] = 'float'
                self.__init_states[measurement_entry['key']] = 0.0
            elif(channel_obj.ch_type_obj.__name__ in self.__int_type_list):
                measurement_entry['values'][0]['format'] = 'integer'
                self.__init_states[measurement_entry['key']] = 0
            elif (channel_obj.ch_type_obj.__name__ in self.__framework_list):
                continue
            elif (channel_obj.ch_type_obj.__name__ in self.__serializable_list):
                for struct_entry in self.__dict_xml._serializables:
                    if struct_entry['name'] == channel_obj.ch_type_obj.__name__:
                        new_entry = {}
                        new_entry['name'] = measurement_entry['key'] + '.' + struct_entry['name'][struct_entry['name'].find('::'):].replace('::', '') + '.' + struct_entry['key']
                        new_entry['key'] = new_entry['name']
                        new_entry['values'] = measurement_entry['values']
                        self.__init_states[new_entry['name']] = 0
                        self.__measurement_list.append(new_entry) 
      
                continue
            else:
                measurement_entry['values'][0]['format'] = 'enum'

            
            if(measurement_entry['values'][0]['format'] == 'enum'):
                for enum_vals in self.__dict_xml._enums:
                    if(enum_vals['type'] == channel_obj.ch_type_obj.__name__):
                        measurement_entry['values'][0]['enumerations'] = enum_vals['val']
                        self.__init_states[measurement_entry['key']] = enum_vals['val'][0]['string']




            self.__measurement_list.append(measurement_entry)   

        self.__init_states = {**self.__init_states, **self.__dict_xml._init_serializables}

    #Write OpenMCT dictionary to a JSON file
    def writeOpenMCTJSON(self, fname, fpath='../'):
        openmct_json = json.dumps(self.__openmct_telem_dict, indent=4)
        with open(fpath + fname + ".json", "w") as outfile:
            outfile.write(openmct_json)

    def writeInitialStatesJSON(self, fname, fpath='../'):
        initialstates_json = json.dumps(self.__init_states, indent=4)
        with open(fpath + fname + ".json", "w") as outfile:
            outfile.write(initialstates_json)     


#Set up and Process Command Line Arguments
arguments, _ = ParserBase.parse_args([StandardPipelineParser],
                                             description="Topology App Dictionary XML to OpenMCT JSON Parser",
                                             client=True  # This is a client script, thus client=True must be specified
                                             )

#Convert Topology App Dictionary XML file to an OpenMCT JSON 
top_dict = TopologyAppDictionaryJSONifier(arguments.dictionary)
top_dict.writeOpenMCTJSON('FPrimeDeploymentTopologyAppDictionary', '../')
top_dict.writeInitialStatesJSON('initial_states', '../')



