#Author: Visma Dimithra Jayakody
#Date: 26th of November 2024

# Task A: Input Validation
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """

    global date
    #Looping the input for "day" until the user enters a valid input
    while True:
        try:#validating day input 
            day=input("Please enter the day of the survey in the format DD : ")
            day=int(day)
            if day<1 or day>31:   # Checking the range of day
                print("Out of range - values must be in the range 1 and 31.")
                continue
            break
        except ValueError:
            print("Integer required ")
            continue

    #Looping the input for "month" until the user enters a valid input    
    while True:
        try:#validating month input
            month=input("Please Enter the month of the survay in the format MM : ")
            month=int(month)
            if month<1 or month>12:   # Checking the range of month
                print("Out of range - values must be in the range 1 and 12.")
                continue
            break
        except ValueError:
            print("Integer required ")
            continue    

    #Looping the input for "year" until the user enters a valid input    
    while True:
        try:#validating year input
            year=input("Please Enter the year of the survay in the format YYYY : ")
            year=int(year)
            if year<2000 or year>2024:   # Checking the range of year
                print("Out of range - values must be in the range 2000 and 2024.")
                continue
            break
        except ValueError:
            print("Integer required ")
            continue  
    
    # Converting the days and months to 2 digit format 
    day=f"{day:02d}"
    month=f"{month:02d}"
    year=str(year)

    date=f'{day}{month}{year}' # Finalizing date for the CSV filename

    pass  # Validation logic goes here

def validate_continue_input():
    "this fucntion will check if the user wants to load a new file and take actions accordingly"
    global new_file
    
    #looping until user inputs a valid input
    while True:
        new_file=input("\nLoad new data set (yes/no)?: ")
        try:
            new_file=str(new_file)
        except ValueError:
            print("Invalid input, Enter yes or no.")
            continue 

        if new_file.lower()=="yes":
            return new_file
        elif new_file.lower()=="no":
            print("Exiting program, Have a nice day!")
            return new_file
        else:
            print("Invalid input, please try yes or no.")
            continue
  

# Task B: Processed Outcomes
def process_csv_data(date):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """

    #globalizing variables that are needed to be displayed
    global total,truck,electric,two_wheeled,elm_junction,highway_junction,bus_Elm_N,vehicles_not_turning,trucks_rounded,bicycles_per_hour,over_speed,scooter_percentage,maximum,time,time_output,rain,retype   
    
    retype='no'
    hourly_vehicles = {}

    # checking if the the file is there in the current dir
    try:
        # opening the csv file
        with open(f"traffic_data{date}.csv", "r") as file:
            lines=file.readlines() # Extracting information form the csv file 
            data=[row.strip().split(',') for row in lines[1:]] # formating and adding the values to a list
            file.close() # Closing the csv file
        print(f"Analizing traffic_data{date}.csv ...")

        total=len(data) # total Number of vahicles recorded in the csv file
        truck= sum(1 for i in data if i[8].lower()=="truck") # total number of trucks recorded in the current csv
        electric=sum(1 for i in data if i[9].lower()=="true") # Total number of Electric  vehicles recorded in the current csv
        two_wheeled=sum(1 for i in data if i[8].lower()=="scooter" or i[8].lower()=="bicycle" or i[8].lower()=="motorcycle") # total number of Two_wheeled vehicles recorded in the current csv
        bicycle=sum(1 for i in data if i[8].lower()=="bicycle") # total number of Bicycles recorded in the current csv
        elm_junction=sum(1 for i in data if i[0].lower()=="elm avenue/rabbit road") # Total number of vehicles recorded in the current csv that have gone pass Elm Avenue/Rabbit road junction
        highway_junction=sum(1 for i in data if i[0].lower()=="hanley highway/westway") # Total number of vehicles recorded in the current csv that have gone pass Hanley Highway/Westway junction
        bus_Elm_N=sum(1 for i in data if (i[0].lower()=="elm avenue/rabbit road") and (i[8].lower()=="buss" and i[4].lower()=='n') ) # total number of busses that have Left Elm Avenue/Rabbit road junction in the north direction
        vehicles_not_turning= sum(1 for i in data if (i[3].lower()==i[4].lower())) # total number of vehicled recorded in the current csv that have not turned right or left after entering a junction
        trucks_rounded=round((truck/total)*100) # Percentage of trucks recorded in the current csv rounded to the nearest integer
        bicycles_per_hour=round(bicycle/24) # Average number of bicyckes recorded in the csv reounded to the nearest integer
        over_speed=sum(1 for i in data if int(i[6])<int(i[7])) # Total number of vehicled recorded as going over the speed limit in the current csv
        scooter_percentage=round((sum(1 for i in data if i[0].lower()=="elm avenue/rabbit road" and i[8].lower()=="scooter")/elm_junction)*100) # Percentage of scooters that have  gone through Elm Avenue in the csv

        # Extracting the time off every vehicled recorded to habe gone throuh Hanley HIghway junction
        
        for row in data[1:]: #skipping headers row 
            if row[0].lower() == "hanley highway/westway": 
                time_of_day = row[2]  # Extract timeOfDay
                hour = time_of_day.split(':')[0]  # Extract the hour part

                # Initialize count for this hour if not already done
                if hour not in hourly_vehicles:
                    hourly_vehicles[hour] = 0
                
                # Increment the count for this hour
                hourly_vehicles[hour] += 1
            
            
        maximum = float('-inf')  # Smallest possible value to start
        time=[] # Multiple busiest hours or single busiest hour will be stored here
        
        #finding the busiest hour
        for hour, value in hourly_vehicles.items():
            if int(value) > maximum: 
                maximum = int(value) 
                time=[int(hour)]
        
        #checking for multiple same busiest hours
        for hour, value in hourly_vehicles.items():
            if int(value) == maximum and int(hour) not in time: 
                time.append(int(hour))

        # generating the perfect output to print depending on whether the current csv have many busiest hours
        time_output=''
        if len(time)>1: # if many busiest hours
            for i in time:
                if time.index(i)==len(time)-1: # checking if the loop is at the last value 
                    time_format=f'[{i}:00 and {i+1}:00].'
                    time_output+=f'{time_format}'
                else:
                    time_format=f'[{i}:00 and {i+1}:00],'
                    time_output+=f'{time_format}'
        else: # if only only busiest hour
            time_format=f'{time[0]}:00 and {time[0]+1}:00.'
            time_output+=time_format

        # Initializing variables needed to calculate the rain hours in the csv
        temp=""
        rainTime=0
        #extracting time of record if whether condition is recorded as rain
        for i, row in enumerate(data): # Enumarating throught the data list with a count
            if "rain" in row[5].lower():
                if temp=="": #checking if this is the first record in the loop that has rain
                    first=row[2][:5]
                    temp = first
                else:
                    temp=row[2][:5]
                if i+1 <= len(data) and "rain" not in data[i+1][5].lower(): # Checking if this is the last record in the loop tha has rain
                    last=temp
                    # formating the time and dviding into hours and mins seperately
                    first_hour, first_min=map(int,first.split(':')[:2]) 
                    last_hour, last_min=map(int,last.split(':')[:2])
                    
                    # Converting the whole time into mins
                    first=first_hour*60 +first_min
                    last=last_hour*60 +last_min
                    #Calculating the duration of rain for that period
                    rainTime+=last-first
                    temp="" # reseting the rain variable for the next loop if any available 

        rain=f"{round(rainTime/60,2)}" # rounding off the total rain duration into hours
    
    # Exiting or looping the input function according to the user input
    except:
        print(f"No such file as \"trafic_data{date}\" in the current directory try again. ")
        validate_continue_input()
        if new_file.lower()=="yes":
            retype="yes"
        else:
            exit()
            


    pass  # Logic for processing data goes here

def display_outcomes():
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    #globalizing the output so that it can be used when saving to a text file
    global output

    # Finalizing the final output printed to the shell
    output=f'''\n**************************************\nData file selected is traffic_data{date}.csv\n**************************************\n
The total number of vehicles recorded for this date is {total} 
The total number of trucks recorded for this date is {truck}
The total number of electric vehicles for this date is {electric}
The total number of two-wheeled vehicles for this date is {two_wheeled}
The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {bus_Elm_N}
The total number of Vehicles through both junctions not turning left or right is {vehicles_not_turning}
The percentage of total vehicles recorded that are trucks for this date is {trucks_rounded}%
The average number of Bikes per hour for this date is {bicycles_per_hour}
The total number of Vehicles recorded as over the speed limit for this date is {over_speed}
The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {elm_junction}
The total number of vehicles recorded through Hanley Highway/Westway junction is {highway_junction}
{scooter_percentage}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.
The highest number of vehicles in an hour on Hanley Highway/Westway is {maximum}
The most vehicles through Hanley Highway/Westway were recorded between {time_output}
The number of hours of rain for this date is {rain}.'''
    
    print(output) # printing the output

    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    pass  # Printing outcomes to the console


# Task C: Save Results to Text File
def save_results_to_file(text, file_name="results.txt"):
    " This function wil create and write/append the final output to a text file in the same directory"
    with open(f"{file_name}", "a+") as text_file:
        text_file.write(text)
        text_file.write('\n\n')
        text_file.close() # closing the text file
    print("\nResuts were succesfully saved to 'results.txt' in the current directory.")

    pass  # File writing logic goes here


####################   Main Program START   ####################
if __name__ == "__main__":
    while True:  # looping the program until the user wants to quit
        # Running functions in order
        validate_date_input()  # Taking inputs
        process_csv_data(date)  # Processing the CSV file
        if retype == 'yes':
            retype = 'no'
            continue
        display_outcomes()  # Printing the output in the shell
        save_results_to_file(output, "results.txt")  # Saving the results to a text file
        validate_continue_input()  # Validating to quit program or open another CSV

        if new_file.lower() == "yes":
            continue  # Opening another program
        else:
            break  # Exiting the program

####################   Main Program END   ####################

# if you have been contracted to do this assignment please do not remove this line

    
