"""
Common function file
- To define the common function(s)
:function check_create_dir: create the folder of plugin
:function remove_old_dir: remove the existing output files
"""

import os, re
import common.config as cfg
from datetime import datetime

def check_create_dir(plugin_list_str):
    """
    Create the folder of plugin
    :parameter plugin_list_str: plugin 
    :type plugin_list_str: str
    :return: none 
    """
    if "," in plugin_list_str:
        plugin_list = [plugin.strip() for plugin in plugin_list_str.split(",") if plugin.strip() != ""]
    else:
        plugin_list = [plugin_list_str]

    remove_old_dir(cfg.OUTPUT_PATH)

    for plugin in plugin_list:
        path = cfg.OUTPUT_PATH + "\\" + plugin
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print("INFO::{}:: Create folder '{}' at '{}'".format(datetime.now(), plugin, cfg.OUTPUT_PATH))
            except OSError as e:
                raise Exception(e)


def remove_old_dir(output_path=cfg.OUTPUT_PATH):
    """
    Remove the existing output files
    :parameter output_path: output path
    :type output_path: str
    :return: none
    """
    print("INFO::{}:: Start removing all folder(s)/file(s) at '{}'".format(datetime.now(), cfg.OUTPUT_PATH))

    for dirs in os.listdir(output_path):
        match = re.search(".txt$|.xml$|.json$", dirs)
        if match == None:
            remove_old_dir(os.path.join(output_path, dirs))
        else:
            os.remove(os.path.join(output_path, dirs))
    
    if output_path is not cfg.OUTPUT_PATH:
        os.rmdir(output_path)
    
    print("INFO::{}:: End removing all folder(s)/file(s) at '{}'".format(datetime.now(), cfg.OUTPUT_PATH))