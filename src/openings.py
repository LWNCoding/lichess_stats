import os
import pandas as pd

def save_openings(openings = {}, uniqueMatch = False, playerClass = False, timeControl = False):
    df = pd.DataFrame.from_dict(openings, orient = "index")
    
    # Sort the columns
    if playerClass:
        df = df[["GM", "IM", "FM", "CM", "WGM", "WIM", "WFM", "WCM", "LM", "Untitled Expert", "A", "B", "C", "D", "E", "N", "BOT"]]
    elif timeControl:
        df = df[["UltraBullet", "Bullet", "Blitz", "Rapid", "Classical", "Correspondence"]]
    else:
        df = df[["Count", "White", "Draw", "Black"]]
    
    path = os.getcwd() + "/analysis/"

    # Determine the file name
    file_name = ""
    if uniqueMatch:
        file_name += "uniqueMatch_"
    if playerClass:
        file_name += "class_"
    if timeControl:
        file_name += "timeControl_"

    ending = "openings.csv"

    df.to_csv(path + file_name + ending, index = True, header = True)

def opening_counts(TESTING = False, TESTING_NUM = 5, saveOpenings = False, uniqueMatch = False, playerClass = False, timeControl = False):
    if playerClass and timeControl:
        raise Exception("Please select only sorting by class OR time control.")
    
    INPUT_PATH = os.path.join(os.getcwd(), "data/processed/")
    uniqueMatches = set()
    openings = {}

    for root, _, files in os.walk(INPUT_PATH):
        for on_file_num, file in enumerate(files, 1):
            # For testing purposes
            if TESTING and on_file_num > TESTING_NUM:
                break

            print(f"Processing file {on_file_num} of {len(files) if not TESTING else TESTING_NUM}...")
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join(root, file), encoding="utf-8").set_index("Site")
                for _, row in df.iterrows():
                    
                    process_opening_counts(openings, uniqueMatches, row, uniqueMatch, playerClass, timeControl)

    if saveOpenings:
        save_openings(openings, uniqueMatch, playerClass, timeControl)
    
    return openings

def process_opening_counts(openings, uniqueMatches, row, uniqueMatch, playerClass, timeControl):
    # Extract the opening
    opening = row["Opening"].split(":")[0].split(",")[0]

    # Unique white-black or black-white matches between two players
    if uniqueMatch:
        match = row["White"] + row["Black"]
        if match in uniqueMatches:
            return
        uniqueMatches.add(match)

    # Determine the classification of analysis
    if timeControl:
        classification = row["Event"].split(" ")[1]
    elif playerClass:
        classification = classify_player(row, opening)
    else:
        classification = "Count"

    # Update the counts in the openings dictionary
    if opening not in openings:
        openings[opening] = {}
    if classification not in openings[opening]:
        openings[opening][classification] = 0
    openings[opening][classification] += 1

    # Additional result counting for opening names
    if not (playerClass or timeControl):
        update_result_counts(openings[opening], row["Result"])

def classify_player(row, opening):
    # White or Black opening
    isWhiteOpening = any(keyword in opening.lower() for keyword in ["opening", "game", "attack"])
    
    # Determine the title
    title = row["WhiteTitle"] if isWhiteOpening else row["BlackTitle"]
    
    # Otherwise class
    if pd.isna(title):
        rating = int(row["WhiteElo"]) if isWhiteOpening else int(row["BlackElo"])
        if rating < 1000: return "N"
        if rating < 1200: return "E"
        if rating < 1400: return "D"
        if rating < 1600: return "C"
        if rating < 1800: return "B"
        if rating < 2000: return "A"
        return "Untitled Expert"
    
    return title

def update_result_counts(opening_dict, result):
    if result == "1-0":
        opening_dict["White"] = opening_dict.get("White", 0) + 1
    elif result == "0-1":
        opening_dict["Black"] = opening_dict.get("Black", 0) + 1
    else:
        opening_dict["Draw"] = opening_dict.get("Draw", 0) + 1