"""
Configuration file
- To define the folder/file path
:variable PROJECT_ROOT: project root folder path
:type PROJECT_ROOT: str
:variable CONFIG_PATH: config folder path
:type CONFIG_PATH: str
:variable OUTPUT_PATH: output folder path
:type OUTPUT_PATH: str
:variable PARAMETER_VALUE_PATH: parameter properties file path
:type PARAMETER_VALUE_PATH: str
"""

import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "output")
PARAMETER_VALUE_PATH = os.path.join(PROJECT_ROOT, "config", "default_parameter_value.properties")