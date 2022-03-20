"""
Plugin file
- Base class for the plugin object
:class Plugin: base class
"""

class Plugin(object):
    """
    Base class
    :method gen_file_for_each_table: generate file(s)
    """
    def __init__(self):
        pass

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

        pass