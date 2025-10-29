import pandas as pd
import os

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
        while True:
            user_input = input("B: Both, C: Control, R: Regular ").upper()
            if user_input == "B":
                self.files = [os_path.join('data', con_file), os_path.join('data', reg_file)]
                break
            elif user_input == "C":
                self.files = [os_path.join('data', con_file)]
                break
            elif user_input == "R":
                self.files = [os_path.join('data', reg_file)]
                break
            else:
                print('Invalid Input')
        while True:
            user_input = input("E: Elevator, S: Stairs ").upper()
            if user_input == "E":
                self.elev_stair = 'Elevator_Times'
                break
            elif user_input == "S":
                self.elev_stair = 'Stair_Times'
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
        for file in self.files:
            df = pd.read_excel(file, sheet_name= self.elev_stair, usecols= "A:C")
            print(df)
            for index, row in df.iterrows():
                if row['Start_Floor'] == start_floor and row['End_Floor'] == end_floor:
                    self.data.append(row['Time_Measured'])
    
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