"""
Plugin file for json format
- To generate file(s) in json format
- Can modify the structures of json
:class FILE_JSON: 
"""

import os, json
import common.config as cfg
from plugin.plugin import Plugin
import pandas as pd
from datetime import datetime

OUTPUT_PATH = os.path.join(cfg.OUTPUT_PATH, "FILE_JSON")

pd.set_option("display.max_colwidth", None)

class FILE_JSON(Plugin):
    """
    Class FILE_JSON
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
        input_df = input_data["FILE_JSON"]
        table_df = input_df[
            input_df["SRC_TABLE"] == table_name
        ]

        col_list = table_df["COLUMN_NAME"].tolist()

        para_dict = {}
        para_dict["table_name"] = table_name 
        para_dict["column_list"] = ",".join(col_list)
        para_dict["base_path"] = "/base/main"
        para_dict["backup_path"] = "/base/backup" 
        para_dict["log_table"] = "DB.LOG_TABLE"
        para_dict["year"] = "*"
        para_dict["month"] = "*"
        para_dict["day"] = "*"
        para_dict["special_character"] = "\r"

        try:
            output_file = os.path.join(OUTPUT_PATH, table_name + ".json")
            with open(output_file, "w") as outfile:
                outfile.write(json.dumps(
                    para_dict,
                    indent=4,
                    separators=(",", ": ")
                ))
        except:
            raise Exception("ERROR::{}:: Failed to write file of '{}'".format(datetime.now(), table_name))

if __name__ == "__main__":
    plugin_obj = FILE_JSON()