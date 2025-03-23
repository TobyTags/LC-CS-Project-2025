


def main1(): 
    import pandas as pd
    import os
    import re


    output_dir = "CleanedData"
    output_file_path = os.path.join(output_dir, "processed_hcny_all_tables.csv")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List to store main processed DataFrames from each file
    processed_dfs = []

    raw_data_dir = "RawData"  # Starting folder that contains many random subfolders

    # Walk through all subdirectories
    for root, dirs, files in os.walk(raw_data_dir):
        if os.path.basename(root) == "Colonies":
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    print("Processing Colonies data from file:", file_path)
                
                    try:
                        # First reading: get timestamp info (we assume the timestamp is in row 0, col 2)
                        df_ts = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip')
                        TimeStampData = str(df_ts.iloc[0, 2])
                        # Extract year and month from the timestamp
                        year_match = re.search(r'\b(20\d{2})\b', TimeStampData)
                        month_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)', TimeStampData)
                        year = year_match.group(1) if year_match else "Unknown"
                        month = month_match.group(0) if month_match else "Unknown"
                        print(f"File {file_path}: Year={year}, Month={month}")
                        
                        # Second reading: read CSV starting after the header rows (skip first 4 rows)
                        df_main = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip', skiprows=4)
                        # Rename columns as needed
                        df_main.columns = ["col1", "col2", "State", "colonies", "max_colonies", "lost_colonies", 
                                            "percent_lost", "added_colonies", "renovated_colonies", "percent_renovated"]
                        # Keep only relevant columns
                        df_main = df_main[["State", "colonies", "percent_lost"]]
                        # Drop rows with missing state
                        df_main.dropna(subset=["State"], inplace=True)
                        # Optionally, limit to the first 46 rows if that is intended
                        df_main = df_main.iloc[:46]
                        df_main.reset_index(drop=True, inplace=True)
                        # Add year and month columns
                        df_main["Year"] = year
                        df_main["Month"] = month
                        
                        processed_dfs.append(df_main)
                    except Exception as e:
                        print(f"Error processing main data from {file_path}: {e}")

    # Combine all main DataFrames into one final DataFrame
    if processed_dfs:
        final_df = pd.concat(processed_dfs, ignore_index=True)
        print("Combined main data from all files.")
    else:
        final_df = pd.DataFrame()
        print("No main data processed.")




    # --- Now update final_df with mites data ---
    # ----------------------------------------------


    # Define the list of states
    states = [
        "Alabama", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
        "Florida", "Georgia", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas",
        "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
        "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "New Jersey",
        "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
        "Oregon", "Pennsylvania", "South Carolina", "South Dakota", "Tennessee", "Texas",
        "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    ]


    import os
    import re
    import pandas as pd

    raw_data_dir = "RawData"  # Top folder with many random subfolders
    mite_data_list = []       # List to accumulate all new mite rows

    # Walk through all subdirectories looking for folders named "Mites" (case-sensitive check here; adjust if needed)
    for root, dirs, files in os.walk(raw_data_dir):
        if os.path.basename(root).lower() == "mites":
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    print("Processing mites data from file:", file_path)
                    
                    try:
                        # Read the CSV for mites extraction using header=5 (adjust if needed)
                        df_mites = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip', header=5)
                        # Drop the first two columns
                        df_mites = df_mites.iloc[:, 2:]
                        # Ensure there's a 'State' column
                        if 'State' not in df_mites.columns:
                            print(f"'State' column not found in {file_path} for mites extraction.")
                            continue
                        df_mites.set_index('State', inplace=True)
                    except Exception as e:
                        print(f"Error reading mites data from {file_path}: {e}")
                        continue
                    
                    # Extract timestamp (to get Month and Year) from the file.
                    try:
                        df_ts = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip')
                        TimeStampData = str(df_ts.iloc[0, 2])
                        year_match = re.search(r'\b(20\d{2})\b', TimeStampData)
                        month_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)', TimeStampData)
                        year = year_match.group(1) if year_match else "Unknown"
                        month = month_match.group(0) if month_match else "Unknown"
                        print(f"Found Timestamp for {file_path}: {month} {year}")
                    except Exception as e:
                        print(f"Error extracting timestamp from {file_path}: {e}")
                        continue
                    
                    # For each state, try to extract the mites percentage (if available)
                    for st in states:
                        try:
                            # Extract the mite percentage; ensure the column name is exactly 'mites'
                            Mite_temp_var = df_mites.loc[st]['mites']
                            print(f"Extracted mites for {st}: {Mite_temp_var}%")
                            
                            # Append a new record to our mite data list
                            mite_data_list.append({
                                'Month': month,
                                'Year': year,
                                'State': st,
                                'Mites': Mite_temp_var
                            })
                        except Exception as e:
                            print(f"Error extracting mites for {st} from file {file_path}: {e}")

    # Convert the accumulated mite data into a DataFrame
    if mite_data_list:
        mites_df = pd.DataFrame(mite_data_list)
        # If there are multiple entries for the same (State, Month, Year), aggregate by taking the last value (you can change this logic)
        mites_df = mites_df.groupby(['State', 'Month', 'Year'], as_index=False).agg({'Mites': 'last'})
        print("Accumulated mite data:")
        print(mites_df)
    else:
        print("No mite data was extracted.")
        mites_df = pd.DataFrame(columns=['State', 'Month', 'Year', 'Mites'])


    # Merge on State, Month, and Year; new mite values will appear as 'Mites_new'
    merged_df = pd.merge(final_df, mites_df, on=['State', 'Month', 'Year'], how='left', suffixes=('_old', '_new'))

    print(merged_df)

    final_df = merged_df
    # Save the combined DataFrame to a CSV file
    try:
        final_df.to_csv(output_file_path, index=False, encoding='utf-8')
        print(f"Combined data saved to: {output_file_path}")
    except Exception as e:
        print(f"Error saving final data: {e}")



# Now that all of the raw data has been parsed and cleaned into one df I can create some graphs - I created a new .py file to have this code in to keep my code base clean