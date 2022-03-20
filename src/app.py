"""
Main file of the program
- Generate the file(s) in json/xml/txt format for each table(s)
:function read_input: read the input csv file(s)
:function get_table_list: get the table list
:function get_plugin_list: get the plugin list
:function get_config: get the configuration value(s)
"""

import os, sys
import pandas as pd
from plugin.plugin import Plugin
import importlib
import configparser
import common.config as cfg
import common.common as cmn
from datetime import datetime


def read_input(input_path=cfg.CONFIG_PATH):
    """
    Read the input csv file(s)
    :parameter input_path: input file path
    :type input_path: str
    :return: input_df
    :rtype: dict
    """
    input_df = {}
    for file in os.listdir(input_path):
        if file.endswith(".csv"):
            src_data = pd.read_csv(input_path + "\\" + file)
            input_df[
                os.path.basename(file).upper().split(".")[0]
            ] = src_data

    return input_df

def get_table_list(table_list_filename):
    """
    Get the table list
    :parameter table_list_filename: filename consist of table list
    :type table_list: str
    :return: table_list
    :rtype: list
    """
    FILE_FOUND = True
    table_list = []
    for file in os.listdir(cfg.CONFIG_PATH):
        if file == table_list_filename:
            FILE_FOUND = False
            with open(cfg.CONFIG_PATH + "\\" + file, "r") as inFile:
                for line in inFile:
                    table_list.append(line.rstrip())
    if FILE_FOUND:
        raise Exception("ERROR::{}:: table list not found '{}'".format(datetime.now(), table_list_filename))

    return table_list

def get_plugin_list(plugin_list_str):
    """
    Get the plugin dict
    :parameter plugin_list_str: plugin
    :type plugin_list_str: str
    :return: plugin_obj_dict
    :rtype: dict
    """
    if "," in plugin_list_str:
        plugin_list = [plugin.strip() for plugin in plugin_list_str.split(",") if plugin.strip() != ""]
    else:
        plugin_list = [plugin_list_str]

    plugin_obj_dict = {}
    for plugin in plugin_list:
        plugin_pkg = importlib.import_module("plugin.{}".format(plugin))
        plugin_obj = eval("plugin_pkg.{} ()".format(plugin))
        plugin_obj_dict[plugin.upper()] = plugin_obj

    return plugin_obj_dict

def get_config(config_path=cfg.PARAMETER_VALUE_PATH):
    """
    Get the configuration value(s)
    :parameter config_path: configuration file path
    :type config_path: str
    :return: config
    :rtype: dict
    """
    config_parser = configparser.ConfigParser()
    config_parser.read(config_path)
    config = {}
    config["DEFAULT"] = {}

    if len(config_parser.sections()) != 0:
        for sec in config_parser.sections():
            config[sec] = {}
    
    for sec in config:
        for key in config_parser[sec]:
            config[sec][key.upper()] = config_parser[sec][key]

    return config

if __name__ == "__main__":

    args = sys.argv[1:]
    table_list_filename = args[0]
    plugin_list_str = args[1]

    try:
        input_df = read_input(cfg.CONFIG_PATH)
    except:
        raise Exception("ERROR::{}:: Failed to read the input file at '{}'".format(datetime.now(), cfg.CONFIG_PATH))

    try:
        table_list = get_table_list(table_list_filename)
    except:
        raise Exception("ERROR::{}:: Failed to get the table list from '{}'".format(datetime.now(), table_list_filename))
    
    try:
        plugin_obj_dict = get_plugin_list(plugin_list_str)
    except:
        raise Exception("ERROR::{}:: Failed to get the plugin list from '{}'".format(datetime.now(), plugin_list_str))

    try:
        config = get_config(cfg.PARAMETER_VALUE_PATH)
    except:
        raise Exception("ERROR::{}:: Failed to get the parameter value at '{}'".format(cfg.PARAMETER_VALUE_PATH))

    try:    
        cmn.check_create_dir(plugin_list_str)
    except:
        raise Exception("ERROR::{}:: Failed to create the output folder at '{}'".format(datetime.now(), cfg.OUTPUT_PATH))

    for table in table_list:
        for plugin_key in plugin_obj_dict:
            try:
                print("INFO::{}:: Generate table '{}' for '{}'".format(datetime.now(), table, plugin_key))
                if not isinstance(plugin_obj_dict[plugin_key], Plugin):
                    raise Exception("ERROR: Invalid plugin object: {}".format(plugin_key))

                plugin_obj_dict[plugin_key].gen_file_for_each_table(table, input_df, config)
            except:
                raise Exception("ERROR::{}:: Failed to generate file for '{}' of '{}'".format(datetime.now(), table, plugin_key))
