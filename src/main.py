from process_data import extract_data
from openings import opening_counts

if __name__ == "__main__":
    extract_or_process = input("Would you like to extract data from a PGN file or process the data? (extract/process): ")
    
    if extract_or_process == "extract":
        PGN_FILE_NAME = input("Please provide the name of the PGN file to extract data from: ")
        extract_data(PGN_FILE_NAME)
    elif extract_or_process == "process":
        TESTING = input("Would you like to test the program? (y/n): ")
        if TESTING == "y":
            TESTING = True
            TESTING_NUM = int(input("How many files would you like to process? "))
        else:
            TESTING = False
            TESTING_NUM = 0
        
        SAVE_OPENINGS = input("Would you like to save the openings data? (y/n): ")
        if SAVE_OPENINGS == "y":
            SAVE_OPENINGS = True
        else:
            SAVE_OPENINGS = False
        
        UNIQUE_MATCH = input("Would you like to sort by unique matches? (y/n): ")
        if UNIQUE_MATCH == "y":
            UNIQUE_MATCH = True
        else:
            UNIQUE_MATCH = False
        
        PLAYER_CLASS = input("Would you like to sort by player class? (y/n): ")
        if PLAYER_CLASS == "y":
            PLAYER_CLASS = True
            TIME_CONTROL = False
        else:
            PLAYER_CLASS = False
            TIME_CONTROL = input("Would you like to sort by time control? (y/n): ")
            if TIME_CONTROL == "y":
                TIME_CONTROL = True
            else:
                TIME_CONTROL = False
        
        opening_counts(TESTING, TESTING_NUM, SAVE_OPENINGS, UNIQUE_MATCH, PLAYER_CLASS, TIME_CONTROL)


