"""
Plugin file for xml format
- To generate file(s) in xml format
- Can modify the structures of xml
:class FILE_XML: 
"""

import os
import common.config as cfg
import pandas as pd
from xml.dom import minidom
from plugin.plugin import Plugin
import xml.etree.cElementTree as ET
from datetime import datetime 

PROJECT_NAME = "PROJECT_FALCON"
WF_NAME = "WF_FALCON"
MP_NAME = "WF_FALCON"

OUTPUT_PATH = os.path.join(cfg.OUTPUT_PATH, "FILE_XML")

pd.set_option("display.max_colwidth", None)

class FILE_XML(Plugin):
    """
    Class FILE_XML
    :method gen_file_for_each_table: generate file(s)
    """

    def __init__(self):
        super().__init__()

    def gen_file_for_each_table(
        self, 
        table_name, 
        input_data, 
        config
    ):
        """
        Generate file(s)
        :parameter table_name: table name
        :type table_name: str
        :parameter input_data: source input data
        :type input_data: DataFrame
        :parameter config: parameter value
        :type config: dict
        :return: none
        """
        input_df = input_data["FILE_XML"]
        table_df = input_df[
            input_df["SRC_TABLE"] == table_name
        ]

        root = ET.Element("root", xmlns="http://www.informatica.com/Parameterization/1.0")
        root.attrib["version"] = "2.0"
        root.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema"

        doc = ET.SubElement(root, "project", name=PROJECT_NAME)
        workflow = ET.SubElement(doc, "workflow", name=WF_NAME)
        mapping = ET.SubElement(doc, "mapping", name=MP_NAME)

        src_conn_list = table_df["SRC_CONN"].tolist()
        tgt_conn_list = table_df["TGT_CONN"].tolist()
        src_db_list = table_df["SRC_DB"].tolist()
        tgt_db_list = table_df["TGT_DB"].tolist()
        tgt_table_list = table_df["TGT_TABLE"].tolist()
        col_list = table_df["COLUMN_NAME"].tolist()

        ET.SubElement(workflow, "parameter", name="SRC_CONN").text = src_conn_list[0]
        ET.SubElement(workflow, "parameter", name="TGT_CONN").text = tgt_conn_list[0]
        ET.SubElement(workflow, "parameter", name="SRC_DB").text = src_db_list[0]
        ET.SubElement(workflow, "parameter", name="TGT_DB").text = tgt_db_list[0]
        ET.SubElement(workflow, "parameter", name="SRC_TABLE").text = table_name
        ET.SubElement(workflow, "parameter", name="TGT_TABLE").text = tgt_table_list[0]
        ET.SubElement(workflow, "parameter", name="KEY").text = config["DEFAULT"]["KEY"]
        ET.SubElement(workflow, "parameter", name="EMAIL_ADDRESS").text = config["DEFAULT"]["EMAIL_ADDRESS"]
        ET.SubElement(mapping, "parameter", name="COLUMNS").text = ", ".join(col_list)

        xmlstr = minidom.parseString(ET.tostring(root)) \
                .toprettyxml(indent="   ", encoding="UTF-8")

        try:
            output_file = os.path.join(OUTPUT_PATH, table_name + ".xml")
            with open(output_file, "wb") as outfile:
                outfile.write(xmlstr)
        except:
            raise Exception("ERROR::{}:: Failed to write file of '{}'".format(datetime.now(), table_name))

        try:
            with open(output_file, "r+") as infile:
                row = infile.readlines()
                all_text = ""
                for line in row:
                    if line.find("xml version=\"1.0\" encoding=\"UTF-8\"") != -1:
                        line = line.replace("xml version=\"1.0\" encoding=\"UTF-8\"", "xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"")
                    all_text += line

            with open(output_file, "w+") as outfile:
                outfile.write(all_text)
        except:
            raise Exception("ERROR::{}:: Failed to modify xml of '{}'".format(datetime.now(), table_name))

if __name__ == "__main__":
    plugin_obj = FILE_XML()