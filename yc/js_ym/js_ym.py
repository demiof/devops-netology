#!/bin/env python3


from decimal import InvalidContext
from pydoc import doc
from pyexpat.errors import messages
import sys
import os.path
from os.path import abspath
from typing import final
from xml.dom.minidom import Document
import yaml
import yaml.scanner
from yaml import Dumper, Loader, SafeLoader, StreamEndEvent, YAMLError, serialize, serialize_all
import json

class js_ym(yaml.YAMLObject):

    yaml_loader = SafeLoader
    yaml_dumper = Dumper
    
    
    trans_count = 0
    params = sys.argv
    file_to_check = ''
    file_to_transform = 'converted_to_json.json'
    YAML_event_structure = dict()
    YAML_token_structure = dict()
    JSON_structure = dict()
    YAML_structure = dict()

    message = ("I'm an js_ym class!",
    "\nNO Arguments given! Need remote name\nType -h,--help for help...\n",
    "\nWrong parametr type, no str!\n",
    "\nFile to convert exists!\n",
    "\nFile to convert does not exist!\n",
    f'''
    \n To much params!
    Please use: {abspath(__file__)} <path to file to convert, includes JSON or YAML structure inside>
    \n
    ''',
    f'''
    \n
    Please use: {abspath(__file__)} <path to file to convert, includes JSON or YAML structure inside>
    \n''',
    "\nUnknown params error!\n",
    )
    
    def __init__(self) -> None:
        js_ym.trans_count += 1

    
    def exclaim(self) -> None:
        print(self.message[0])
    
    def checkFExists(path) -> bool:
        if os.path.exists(path):
            return True
        else:
            return False


    @classmethod
    def checkArgs(cls) -> bool:

        if len(cls.params) <= 1:
            print(cls.message[2])
            return False
        
        elif len(cls.params) > 2:
            print(cls.message[5])
            return False
            
        elif cls.params[1]=='-h' or cls.params[1]=='--help':
            print(cls.message[6])
            return False
            
        elif type(cls.params[1])==str:
            
            if cls.checkFExists(cls.params[1]):
                print(cls.message[3])
                cls.file_to_check=cls.params[1]
                return True
            else:
                print(cls.message[4])
                return False

        else:
            print(cls.message[7])
            return False

    @classmethod
    def IfFileJson(cls, file_to_check) -> bool:
        
        try:
            with open(file_to_check,'r') as stream:
                cls.JSON_structure = json.load(stream)
        except ValueError as e:
            print('Invalid JSON!')
            return False
        else:
            print('Valid JSON!')
            return True
        finally:
            stream.close()

    @classmethod
    def IfFileYaml(cls, file_to_check) -> bool:
        
        try:
            with open(file_to_check, 'r') as stream:
                data_all = yaml.safe_load_all(stream)
                parsed_stream = yaml.parse(stream)
                scaned_stream = yaml.scan(stream, Loader=cls.yaml_loader)
                composed_stream =  yaml.compose(stream)
                #print('=====================')
                #print(stream)
                #print('=========Vgenerator_refV============')
                #print(scaned_stream)
                print('==========Vparsed eventsV============')
                for event in parsed_stream:
                    #if cls.yaml_loader.check_event(event):
                        print(event)
                    #else: 
                        #print('invalid event! -> '.event)
                print('==========Vscaned tokensV============')
                for token in scaned_stream:
                    print(token)
                print('==========Vcomposed streamV==========') 
                print(composed_stream)   
                print('=====================================')
        except ValueError as e:
            print('\nInvalid YAML\n')
            stream.close()
            sys.exit()
        except yaml.scanner.ScannerError:
            print('\nFailed while read pystream\n')
            #print(ge)
            return False
        else:
            print('\nRead pystream ok!\n')
            #cls.YAML_event_structure = parsed_stream
            cls.YAML_token_structure = scaned_stream
            return True
        finally:
            stream.close()

    @classmethod
    def TransYamlJson(cls, file_to_check, file_to_transform):
        
        try:
            with open(file_to_check, 'r') as fr:
                with open(file_to_transform, 'w') as fw:
                    cls.JSON_structure = json.dumps(yaml.load(fr,Loader=cls.yaml_loader))
                    json.dump(cls.JSON_structure,fw)
                    print("==============Vfile to transform nameV=============")
                    print(file_to_transform)
                    print("==============VTransformed JSON structureV=========")
                    print(cls.JSON_structure)
                    print("===================================================")
        except:
            print('\nFailed to transform file\n',file_to_check,'to',file_to_transform)
        else:
            print('\nTransformation succesfully!\n')
        finally:
            fw.close()
            fr.close()
    
    @classmethod
    def usage(cls):
        print("Class js_ym made ", cls.trans_count, " transformations.")


###########################################################################

if __name__ == "__main__":

    Converter = js_ym()

    if Converter.checkArgs():
        Converter.usage()
        if Converter.IfFileYaml(Converter.file_to_check):
            print('\nValid YAML!\n')
            Converter.JSON_structure = Converter.TransYamlJson(Converter.file_to_check,Converter.file_to_transform)
        elif Converter.IfFileJson(Converter.file_to_check):
            print('\nInvalid YAML!\n')
            Converter.JSON_structure = Converter.TransYamlJson(Converter.file_to_check,Converter.file_to_transform)
        else:
            print('\nUnknown file type: neither YAML, nor JSON!\n')
    else:
        print('\nBad args!\n')

 