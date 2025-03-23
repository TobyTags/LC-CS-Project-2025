import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates
import numpy as np #using this for np.gradient when getting the differenciation of the mites and colonies data

def StateGraphs(State):
    # Load the cleaned CSV file
    file_path = "CleanedData/processed_hcny_all_tables.csv"
    print("Reading CSV file...")
    df = pd.read_csv(file_path)
    print("CSV file loaded successfully.")

    # Convert columns to appropriate data types
    print("Converting data types...")
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%B', errors='coerce')
    df['Mites'] = pd.to_numeric(df['Mites'], errors='coerce')  # Assuming 'Mites' column holds mite percentage data
    df['colonies'] = pd.to_numeric(df['colonies'], errors='coerce')
    print("Data conversion completed.")

    # Filter data for the specified state
    print(f"Filtering data for {State}...")
    state_df = df[df['State'] == State]

    # Drop any rows with missing mite percentage or date
    state_df.dropna(subset=['Date', 'Mites', 'colonies'], inplace=True)

    # Sort the data by date to ensure correct plotting order
    state_df = state_df.sort_values('Date')
    
    # Create directory for saving graphs
    output_dir = f"graphs/{State}_graphs"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving graphs to directory: {output_dir}")

    #plotting the graphs below -----------
    #----------------------------------------------

    # Plot: Mite trend over months and years by state
    print("Generating mite percentage trend plot...")
    plt.figure(figsize=(12, 9))
    plt.plot(state_df['Date'], state_df['Mites'], marker='o', linestyle='-')
    
    plt.xlabel('Date', fontsize=25)
    plt.ylabel('Mite Percentage', fontsize=25)
    plt.xticks(rotation=45, fontsize=15)

    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate date labels for better readability

    # Save the plot
    plt_path = os.path.join(output_dir, f"{State}_mite_trends.png")
    plt.savefig(plt_path)
    plt.close()  # Close the plot to free up memory
    print(f"Graph saved as {plt_path}")


    # Plot: Population over months and years by state
    #----------------------------------------------------------------

    print("Generating population trend plot...")
    plt.figure(figsize=(12, 9))
    plt.plot(state_df['Date'], state_df['colonies'], marker='o', linestyle='-')
   
    plt.xlabel('Date', fontsize=25)
    plt.ylabel('Population (Per 1000 colonies)', fontsize=25)
    plt.xticks(rotation=45, fontsize=15)

    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate date labels for better readability

    # Save the plot
    plt_path = os.path.join(output_dir, f"{State}PopulationTrends.png")
    plt.savefig(plt_path)
    plt.close()  # Close the plot to free up memory
    print(f"Graph saved as {plt_path}")


    # Plot: Population with mites over time by state
    # -------------------------------------------------------
    print("Generating population with mites trend plot...")
    plt.figure(figsize=(12, 9))

    # Normalize colonies to the range 0-100
    colonies_norm = (state_df['colonies'] - state_df['colonies'].min()) / (state_df['colonies'].max() - state_df['colonies'].min()) * 100

    # Plot the 'Mites' data
    plt.plot(state_df['Date'], state_df['Mites'], marker='o', linestyle='-', label='Mites')

    # Plot the 'colonies' data
    plt.plot(state_df['Date'], colonies_norm, marker='o', linestyle='-', label='Colonies')

    plt.xlabel('Date', fontsize=25)
    plt.ylabel('Population (Per 1000 colonies) and mites', fontsize=25)
    plt.xticks(rotation=45, fontsize=15)
    plt.grid(True)
    plt.legend()  # Display legend to differentiate between the two lines

    # Save the plot
    plt_path = os.path.join(output_dir, f"{State}PopulationAndMitesTrends.png")
    plt.savefig(plt_path)
    plt.close()  # Close the plot to free up memory
    print(f"Graph saved as {plt_path}")









    # Plot: Population with mites over time by state - ajusted for interpretation
    # -------------------------------------------------------
    print("Generating population with mites trend plot...")
    plt.figure(figsize=(12, 9))

    # Normalize colonies to the range 0-100
    colonies_norm = (state_df['colonies'] - state_df['colonies'].min()) / (state_df['colonies'].max() - state_df['colonies'].min()) * 100

    # Plot the 'Mites' data --- adding the offset by 6 months in order to interpret the true relationship of mites to population
    plt.plot(state_df['Date'] + pd.DateOffset(months=6), state_df['Mites'], marker='o', linestyle='-', label='Mites')

    # Plot the 'colonies' data
    plt.plot(state_df['Date'], colonies_norm, marker='o', linestyle='-', label='Colonies')

    plt.xlabel('Date', fontsize=25)
    plt.ylabel('Population (Per 1000 colonies) and mites', fontsize=25)
    plt.xticks(rotation=45, fontsize=15)
    plt.grid(True)
    plt.legend()  # Display legend to differentiate between the two lines

    # Save the plot
    plt_path = os.path.join(output_dir, f"{State}InterpretationOffset_PopulationAndMitesTrends.png")
    plt.savefig(plt_path)
    plt.close()  # Close the plot to free up memory
    print(f"Graph saved as {plt_path}")




    # gettting the same plot as obove but this time  the dy dx
    # -------------------------------------------------------

    # ----------------------------
    # 1. Sort & Aggregate the Data
    # ----------------------------

    # Ensure 'Date' is in datetime format
    state_df['Date'] = pd.to_datetime(state_df['Date'])

    # Sort by date (important before grouping)
    state_df = state_df.sort_values(by='Date')

    # Remove duplicates by grouping on 'Date' and taking the mean
    state_df = state_df.groupby('Date', as_index=False).mean(numeric_only=True)

    # ----------------------------
    # 2. Normalize the Data
    # ----------------------------

    # Normalize colonies to 0–100
    colonies_norm = (
        (state_df['colonies'] - state_df['colonies'].min())
        / (state_df['colonies'].max() - state_df['colonies'].min())
        * 100
    )

    # Normalize mites to 0–100
    mites_norm = (
        (state_df['Mites'] - state_df['Mites'].min())
        / (state_df['Mites'].max() - state_df['Mites'].min())
        * 100
    )

    # ----------------------------
    # 3. Prepare the Dates
    # ----------------------------

    dates = state_df['Date']
    # Add a 6-month offset to the mites date
    dates_mites = dates + pd.DateOffset(months=6)

    # Convert dates to numeric "days since Matplotlib epoch"
    x_days = mdates.date2num(dates)
    x_days_mites = mdates.date2num(dates_mites)

    # Convert days to "years since the earliest date"
    #   (makes derivative "per year" instead of "per day")
    x_years = (x_days - x_days[0]) / 365.25
    x_years_mites = (x_days_mites - x_days[0]) / 365.25

    # ----------------------------
    # 4. Compute the Derivatives
    # ----------------------------

    with np.errstate(divide='ignore', invalid='ignore'):
        dy_dx_colonies = np.gradient(colonies_norm, x_years)
        dy_dx_mites    = np.gradient(mites_norm, x_years_mites)

    # ----------------------------
    # 5. Plot the Derivatives
    # ----------------------------

    plt.figure(figsize=(12, 9))
    plt.plot(dates_mites, dy_dx_mites, marker='o', linestyle='-', 
            label='dy/dx Mites', color='blue')
    plt.plot(dates, dy_dx_colonies, marker='o', linestyle='-', 
            label='dy/dx Colonies', color='orange')
    

    plt.xlabel('Date', fontsize=20)
    plt.ylabel('Rate of Change (per year)', fontsize=20)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.legend(fontsize=12)
    plt.title("Rate of Change of Colonies and Mites Over Time", fontsize=22)

    # ----------------------------
    # 6. Save & Close the Figure
    # ----------------------------

    plt_path = os.path.join(output_dir, f"{State}_RateOfChange_PopulationAndMites.png")
    plt.savefig(plt_path, bbox_inches='tight')
    plt.close()

    print(f"Graph saved as {plt_path}")









