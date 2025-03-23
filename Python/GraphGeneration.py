import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend (no GUI) for rendering plots to files

import matplotlib.dates as mdates

import matplotlib.pyplot as plt
import os

def main2():

    # Load the cleaned CSV file
    file_path = "CleanedData/processed_hcny_all_tables.csv"

    print("Reading CSV file...")
    df = pd.read_csv(file_path)
    print("CSV file loaded successfully.")

    # Convert columns to appropriate data types
    print("Converting data types...")
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%B', errors='coerce')
    df['colonies'] = pd.to_numeric(df['colonies'], errors='coerce')
    df['percent_lost'] = pd.to_numeric(df['percent_lost'], errors='coerce')
    print("Data conversion completed.")

    # Drop any rows with missing values
    print("Dropping missing values...")
    df.dropna(subset=['Date', 'colonies', 'percent_lost'], inplace=True)

    # Create directory for saving graphs
    output_dir = "graphs"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving graphs to directory: {output_dir}")

    states = df['State'].unique()










    # Start GRAPH 1 --------------------------------------------------------------------
    # Ensure that the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    selected_states = ['Alabama', 'Arizona', 'Arkansas']

    plt.figure(figsize=(12, 6))
    for state in selected_states:
        # Filter and sort the data for each state by date
        state_data = df[df['State'] == state].sort_values('Date')
        plt.plot(state_data['Date'], state_data['colonies'], marker='o', label=state)

    plt.xlim(pd.Timestamp("2019-01-01"), pd.Timestamp("2025-01-01"))

    # Format the x-axis date labels
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    plt.title('Colonies Trend Over Months and Years by State', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of Colonies', fontsize=16)
    plt.legend(title='State')
    plt.grid(True)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'colonies_trend.jpg')
    plt.savefig(output_path, dpi=300)
    plt.close()
    # END GRAPH 1 --------------------------------------------------------------------










    # Start GRAPH 2 --------------------------------------------------------------------
    # Plot 2: Percentage of colonies lost over months and years by state
    print("Generating percentage lost plot...")
    plt.figure(figsize=(12, 6))

    selected_states = ['Alabama', 'Arizona', 'Arkansas']

    for state in selected_states:
    
        state_data = df[df['State'] == state].sort_values('Date')
        plt.plot(state_data['Date'], state_data['percent_lost'], marker='x', label=state)

    plt.title('Percentage of Colonies Lost Over Months and Years by State')
    plt.xlabel('Date')
    plt.ylabel('Percent Lost')
    plt.legend(title='State')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'percent_lost_trend.jpg'))
    plt.close()
    print("Percentage lost plot saved.")
    # END GRAPH 2 --------------------------------------------------------------------







    # Start GRAPH 3 --------------------------------------------------------------------
    # Plot 3: Colonies distribution by state (bar chart)
    print("Generating colonies distribution plot...")
    plt.figure(figsize=(20, 8))
    df.groupby('State')['colonies'].sum().sort_values().plot(kind='bar', color='skyblue')
    plt.title('Total Number of Colonies by State')
    plt.xlabel('State')
    plt.ylabel('Total Colonies')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.savefig(os.path.join(output_dir, 'total_colonies_by_state.jpg'))
    plt.close()
    print("Colonies distribution plot saved.")
    # END GRAPH 3 --------------------------------------------------------------------







    # Start GRAPH 4 --------------------------------------------------------------------
    # Plot 4: Average percentage of colonies lost per state (bar chart)
    print("Generating average percentage lost plot...")
    plt.figure(figsize=(20, 8))
    df.groupby('State')['percent_lost'].mean().sort_values().plot(kind='bar', color='salmon')
    plt.title('Average Percentage of Colonies Lost by State')
    plt.xlabel('State')
    plt.ylabel('Average Percent Lost')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.savefig(os.path.join(output_dir, 'average_percent_lost.jpg'))
    plt.close()
    print("Average percentage lost plot saved.")
    # END GRAPH 4 --------------------------------------------------------------------





    print("All graphs have been saved successfully.")