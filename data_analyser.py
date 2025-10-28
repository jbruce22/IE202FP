import os
import pandas as pd
import numpy as np

class DataAnalyser:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def summarize(self):
        pass

    def tables(self):
        pass

class Control:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def summarize(self):
        pass

    def tables(self):
        pass

class Average:
    def __init__(self, start_floor, end_floor):
        self.id = (start_floor, end_floor)
        self.start_floor = start_floor
        self.end_floor = end_floor

    def average_value(self):
        pass

reg_in_filename = "plc"
con_filename = "plc"
con_data = pd.read_excel(os.path.join('data', reg_in_filename))
control = Control()
reg_data = pd.read_excel(os.path.join('data', con_filename))
data_analyser = DataAnalyser()
