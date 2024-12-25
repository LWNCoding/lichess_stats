import os 
import pandas as pd

def extract_data(FILE_NAME = "INSERT_HERE"):
    if FILE_NAME == "INSERT_HERE" or not FILE_NAME.endswith(".pgn"):
        raise Exception("Please provide the name of the PGN file to extract data from.")
    
    # Pathing
    INPUT_PATH = os.getcwd() + "/data/raw/" + FILE_NAME
    OUTPUT_PATH = os.getcwd() + "/data/processed/"
    FILE_NAME = FILE_NAME.split(".")[0] # Remove the file extension for the output file name

    # Open the file
    pgns = open(INPUT_PATH, "r")

    # Collect game data
    games = []
    curr_game = {}
    file_num = 1

    for line in pgns:
        # Extract the information from the info line
        if line.startswith("["):
            line = line[1:-3].split(" \"")
            cat = str(line[0])
            info = str(line[1])
            curr_game[cat] = info
        # Ignore the empty lines
        elif len(curr_game) > 0:
            games.append(curr_game)
            curr_game = {}

        # Save in batches of 500k games
        if len(games) == 500000:
            df = pd.DataFrame(games)
            df.set_index("Site", inplace = True)
            df.to_csv(OUTPUT_PATH + FILE_NAME + f"_{file_num}.csv", index = True, header = True)

            file_num += 1
            games = []

    # Save the remaining games
    df = pd.DataFrame(games)
    df.set_index("Site", inplace = True)
    df.to_csv(OUTPUT_PATH + FILE_NAME + f"_{file_num}.csv", index = True, header = True)