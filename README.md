# File Generator Program Template

The *File Generator Program Template* is a template that utilize a plugin feature to generate files in xml, json, etc format in batch. In the example, it is provided two sample plugin scripts on how to generate xml and json files. If we want to generate our own kind of files, we can develop our own plugin script. Usually in database, we need to prepare a lots of parameter files for each table to run the daily jobs. In order to facilitate that, we can utilize the python program to ease down our jobs.

## How to develop own plugin script

We need to prepare a **source input file** in csv format, a **table list file** in text format, a **default parameter properties file** and create a **plugin script** in python format.

### source input file (*.csv)

This is a source data csv format file. It contains the information that we need to generate in our xml or json files. The file should be placed at *"/file_generator_program_template/config"*.

### table list file (table_list.txt)

This is a text file that contains all the table names. The file should be placed at *"/file_generator_program_template/config"* \
For example:

```text
table_utopia
table_flora
```

### default parameter properties file (default_parameter_value.properties)

This is a default parameter value properties file. The file should be placed at *"/file_generator_program_template/config"* \
For example:

```text
[DEFAULT]
KEY = ABC123
EMAIL_ADDRESS = user@email.com
```

### plugin script (*.py)

This is a python format file. It contains the logic on how to generate our desired files. \
The name of this file must be similar to our source input file name. In this file, it must include a class with a name that is similar to our source input file name. For example, we have a *"FILE_JSON.csv"*, then we must name our script as *"FILE_JSON.py"* and our class as *"FILE_JSON()"*. The class must be inherited from a parent class called as *"Plugin"*. Besides that, in our class, it should contain a method with a name as *"gen_file_for_each_table()"* along with arguments *"table_name"*, *"input_data"*, *"config"*. In this method, we will include our logic on generating the files.\
For example:

```python
class FILE_JSON(Plugin):

    def gen_file_for_each_table(
        self, 
        table_name, 
        input_data, 
        config
    ):

    pass
```

The file should be placed at *"/file_generator_program_template/src/plugin"*.

## How to run the program

We can run the program with the python installed command prompt. The *"Anaconda Prompt"* is encouraged as it includes the python packages required. \
To run the program, go to *"/file_generator_program_template/src"* and open the command prompt. \
The command:

```bash
python app.py table_list.txt FILE_XML
```

To run the program with multiple plugins, we can concatenate the plugin names as a string. \
The command:

```bash
python app.py table_list.txt FILE_XML,FILE_JSON
```

## Output files

The output file will be generated at *"/file_generator_program_template/output"* with each folder named as the plugin's name.
