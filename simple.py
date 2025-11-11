import pandas as pd
import os
import datetime
from numbers import Number

class Analyzer:
    def __init__(self):
        self.files = []
        self.elev_stair = ''
        self.start_floor = 0
        self.end_floor = 0
        self.data = []


    def setup(self):
        con_file = "Control_Data.xlsx"
        reg_file = "Data_Collection.xlsx"
        os_path = os.path
        file_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_dir)

        while True:
            user_input = input("B: Both, C: Control, R: Regular ").upper()
            if user_input == "B":
                # build absolute paths to files in this script directory
                self.files = [os_path.join(file_dir, con_file), os_path.join(file_dir, reg_file)]
                break
            elif user_input == "C":
                self.files = [os_path.join(file_dir, con_file)]
                break
            elif user_input == "R":
                self.files = [os_path.join(file_dir, reg_file)]
                break
            else:
                print('Invalid Input')
        while True:
            user_input = input("E: Elevator, S: Stairs ").upper()
            if user_input == "E":
                self.elev_stair = 'Elevator_Times'
                break
            elif user_input == "S":
                self.elev_stair = 'Stairs_Times'
                break
            else:
                print('Invalid Input')

        while True:
            user_input = int(input("Enter start floor: "))
            if user_input >= 0 and user_input <= 5:
                self.start_floor = user_input
                break
            else:
                print('Invalid Input')

        while True:
            user_input = int(input("Enter end floor: "))
            if user_input >= 0 and user_input <= 5 and user_input != self.start_floor:
                self.end_floor = user_input
                break
            else:
                print('Invalid Input')

    def get_data(self, elev_stair, start_floor, end_floor):
        # clear previous data
        self.data = []
        for file in self.files:
            # use the passed-in sheet name (elev_stair)
            df = pd.read_excel(file, sheet_name=elev_stair, usecols="A:C")
            # print(df)
            for index, row in df.iterrows():
                try:
                    if row['Start_Floor'] == start_floor and row['End_Floor'] == end_floor:
                        t = row.get('Time_Measured') if hasattr(row, 'get') else row['Time_Measured']
                        seconds = self._to_seconds(t)
                        if seconds is not None:
                            self.data.append(seconds)
                except KeyError:
                    # If expected columns aren't present, skip this row
                    continue

    def _to_seconds(self, t):
        """Convert various time-like values to seconds (float).

        Returns None for missing/unrecognized values.
        """
        # pandas may import empty cells as NaN
        try:
            if pd.isna(t):
                return None
        except Exception:
            pass

        # numeric values (assume already seconds)
        if isinstance(t, Number):
            return float(t)

        # datetime.timedelta
        if isinstance(t, datetime.timedelta):
            return float(t.total_seconds())

        # datetime.time -> convert to seconds since midnight
        if isinstance(t, datetime.time):
            return float(t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1e6)

        # pandas Timestamp or datetime.datetime -> return seconds since midnight
        if isinstance(t, (pd.Timestamp, datetime.datetime)):
            dt = t.to_pydatetime() if isinstance(t, pd.Timestamp) else t
            return float(dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1e6)

        # if it's a string, try parsing common formats
        if isinstance(t, str):
            for fmt in ("%H:%M:%S", "%H:%M", "%M:%S"):
                try:
                    parsed = datetime.datetime.strptime(t, fmt)
                    return float(parsed.hour * 3600 + parsed.minute * 60 + parsed.second)
                except Exception:
                    continue

        # unknown type
        return None
    
    def average_time(self):
        if len(self.data) == 0:
            print("No data available for the selected criteria.")
            return None
        avg_time = sum(self.data) / len(self.data)
        return avg_time
    
if __name__ == "__main__":
    analyzer = Analyzer()
    analyzer.setup()
    analyzer.get_data(analyzer.elev_stair, analyzer.start_floor, analyzer.end_floor)
    avg_time = analyzer.average_time()
    if avg_time is not None:
        print(f'The average time from floor {analyzer.start_floor} to floor {analyzer.end_floor} '
              f'using {analyzer.elev_stair[:-6].lower()} is: {avg_time:.2f} seconds.')