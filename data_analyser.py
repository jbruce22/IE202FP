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

filename = "plc"
con_data = pd.read_excel(os.path.join('data', filename))
control = Control()
data = pd.pd.read_excel(os.path.join('data', filename))
data_analyser = DataAnalyser()
