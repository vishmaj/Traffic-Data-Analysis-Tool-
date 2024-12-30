#Author: Visma Dimithra Jayakody
#Date: 20th of December 2024

# Task D: Histogram Display
import tkinter as tk
import Shell_Outcomes as first_part


class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data 
        self.date = date[:2] + "/" + date[2:4] + "/" + date[4:]
        self.root = tk.Tk()
        self.canvas = None  # Will hold the canvas for drawing
        self.csv_processor=MultiCSVProcessor()
        self.scale=None

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.destroy
        self.root.title("Histogram")
        self.canvas= tk.Canvas(self.root, width=1000, height=750, bg="white")
        self.canvas.pack()
        pass  # Setup logic for the window and canvas

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        rabbit = list(self.traffic_data[0].values())
        hayley = list(self.traffic_data[1].values())

        #Processing a proper scale to dray the histogram, considering data sets with large number of vehicles per hour
        maximum=self.traffic_data[2]
        if maximum >=100:
            self.scale=2
        elif maximum>=50:
            self.scale=5
        elif maximum>=10:
            self.scale=8
        else:
            self.scale=10
        x = 82.5
        #scale for hanley elm avenue/ rabbit road
        
        # Draw the Rabbit bars
        for j in rabbit:
            self.canvas.create_rectangle(x, 650 - (int(j) * self.scale), x + 15, 650, fill="Light Green", outline="grey")
            self.canvas.create_text(x+7.5,  (650 - (int(j) * self.scale))-10, text=str(j), font=("Arial",8,"bold"), fill="Light Green")
            x += 35

        # Reset x position for Hayley bars
        x = 97.5
        #scale for hanley highway/westway junction
        # Draw the Hayley bars
        for j in hayley:
            self.canvas.create_rectangle(x, 650 - (int(j) * self.scale), x + 15, 650, fill="LightCoral", outline="grey")
            self.canvas.create_text(x+7.5,  (650 - (int(j) * self.scale))-10, text=str(j), font=("Arial",8,"bold"), fill="LightCoral")
            x += 35

        # Draw the X-axis
        self.canvas.create_line(82.5, 650, 917.5, 650, fill="gray", width=1)
        x_line=82.5
        for i in range(24):
            self.canvas.create_text(x_line+15,660,text=str(f"{i:02d}"), font=("Helvetica",8,"bold"), fill="black")
            x_line+=35
        pass  # Drawing logic goes here

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        self.canvas.create_text(50,55,text=f"Histogram of Vehicle Frequency per Hour ({self.date})",font=("Arial",16,"bold"),anchor="w",fill="grey")
        self.canvas.create_text(585,55,text=f"| scale=(1UNIT:{self.scale}Px)",font=("Arial",12,"bold"),anchor="w",fill="grey")
        self.canvas.create_rectangle(50,70,65,85, fill="Light Green", outline="grey")
        self.canvas.create_text(70,78,text="Elm Avenue/Rabbit Road",font=("Arial",12,"bold"),anchor="w",fill="grey")
        self.canvas.create_rectangle(50,90,65,105, fill="LightCoral", outline="grey")
        self.canvas.create_text(70,98,text="Hanley Highway/Westway",font=("Arial",12,"bold"),anchor="w",fill="grey")
        self.canvas.create_text(430,685,text="Hours 00:00 to 24:00",font=("Arial",12,"bold"),anchor="w",fill="grey")

        button_style = {"font": ("Arial", 8, "bold"),"bg": "White","fg": "grey","relief": "raised","borderwidth": 1,"width": 15 }# button formatting
        load_button=tk.Button(self.root, text="Load new dataset", command=main,**button_style)#Open new data set for comparrision button
        close_button =tk.Button(self.root, text="close", command=exit,**button_style)  #Close program button
        #setting up the buttons on the canvas
        self.canvas.create_window(510, 700, anchor="ne", window=load_button)  
        self.canvas.create_window(625, 700, anchor="ne", window=close_button)  
       
        pass  # Logic for adding a legend

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        # self.root.attributes('-topmost', True)
        self.root.mainloop()
        pass  # Tkinter main loop logic


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = []
        self.date=None
        self.file_name=None
        self.first_run="yes"
        self.retype=None
        self.new_file=""

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        try:
            with open(file_path,'r') as file:
                lines=file.readlines() # Extracting information form the csv file 
                self.current_data=[row.strip().split(',') for row in lines[1:]]
                self.retype="no"
        except FileNotFoundError:
            print(f"No such file as \"{file_path}\" in the current directory try again. ")
            self.retype="yes"


        pass  # File loading and data extraction logic

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data.clear()
            
        pass  # Logic for clearing data

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        
        if self.retype=="yes" and self.first_run=="no":
            while True:
                self.new_file=input("\nDo you want to load a new file? (Y/N): ")
                if self.new_file.lower() not in ["yes","no","y","n"]:
                    print("\nInvalid input, please enter 'yes' or 'no'")
                    continue
                if self.new_file.lower() in ["no","n"]:
                    print("\nThank you for using the program")
                    exit()
                break
        first_part.validate_date_input()
        self.date=first_part.date
        self.file_name=f"traffic_data{self.date}.csv"
        self.first_run="no"

        pass  # Logic for user interaction

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        hourly_vehicles_hanley={}
        hourly_vehicles_rabbit_road={}

        #analysing the proper data needed for the histogram
        for row in self.current_data: 
            if row[0].lower() == "hanley highway/westway": 
                time_of_day = row[2]  # Extract timeOfDay
                hour = time_of_day.split(':')[0]  # Extract the hour part

                # Initialize count for this hour if not already done
                if hour not in hourly_vehicles_hanley:
                    hourly_vehicles_hanley[hour] = 0
                
                # Increment the count for this hour
                hourly_vehicles_hanley[hour] += 1

            elif row[0].lower() == "elm avenue/rabbit road": 
                time_of_day = row[2]  # Extract timeOfDay
                hour = time_of_day.split(':')[0]  # Extract the hour part

                # Initialize count for this hour if not already done
                if hour not in hourly_vehicles_rabbit_road:
                    hourly_vehicles_rabbit_road[hour] = 0
                hourly_vehicles_rabbit_road[hour] += 1

        self.clear_previous_data()
        #getting the bussiest hours of each junction for the scale if the histogram
        max_hanley = max(hourly_vehicles_hanley.values())
        max_rabbit_road = max(hourly_vehicles_rabbit_road.values())
        overall_max = max(max_hanley, max_rabbit_road)# Get the overall maximum

        #adding the values to a list to be accessed in the histogram class
        self.current_data.append(hourly_vehicles_rabbit_road)
        self.current_data.append(hourly_vehicles_hanley)
        self.current_data.append(overall_max)# To get a proper scale for the histogram

        self.retype="yes"

def main():
    """This will run the entire program"""
    app=MultiCSVProcessor()
    while True:
        app.handle_user_interaction()
        app.load_csv_file(app.file_name)
        if app.retype=="yes":
            continue
        #running the processing funciton in part A,B,C and printing
        print('\n')
        first_part.process_csv_data(app.date)
        first_part.display_outcomes()
        first_part.save_results_to_file(first_part.output,"results.txt")
        print('\n')
        app.process_files()
        histogram=HistogramApp(app.current_data,app.date)
        histogram.run()
        

        pass  # Loop logic for handling multiple files

if __name__=="__main__":
        """
        -After runnning the program for the first time, a new data set can be loaded by either pressing on the 'Load new dataset' button or by closing all opened histograms.
        -The 'Load new dataset' button is useful when the staff memeber needs to compare two data sets at the same time.
        -The 'close' button will end the whole progra. If the staff member just needs to close the current open histogram, the histogram must be closed with the 'X' icon.
        """
        main()#this will run the entire program 
