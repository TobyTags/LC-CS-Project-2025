
def main3():
    import pandas as pd
    import os
    import re
    import matplotlib.pyplot as plt

    print("Generating Overall graphs from main3 function")
    # Load the cleaned CSV file
    file_path = "CleanedData/processed_hcny_all_tables.csv"
    print("Reading CSV file...")
    df = pd.read_csv(file_path)
    print("CSV file loaded successfully.")

    # Convert columns to appropriate data types
    print("Converting data types...")
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%B', errors='coerce') 
    df['Mites'] = pd.to_numeric(df['Mites'], errors='coerce')  # Assuming 'Mites' holds mite percentage data
    df['colonies'] = pd.to_numeric(df['colonies'], errors='coerce')
    print("Data conversion completed.")
    
    # Create directory for saving graphs
    output_dir = "graphs/OverallGraphs/"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving graphs to directory: {output_dir}")

    # --- Create Bar Charts below ---
    # --------------------------------------------
    
    # Group the data by State and calculate the average of Mites and colonies
    state_group = df.groupby('State').agg({'Mites': 'mean', 'colonies': 'mean'}).reset_index()
    
    # Bar chart for Average Mite Percentage by State
    plt.figure(figsize=(12, 8))
    plt.bar(state_group['State'], state_group['Mites'], color='#6f9a4d')
    plt.xlabel('State', fontsize=20)
    plt.ylabel('Average Mite Percentage', fontsize=20)
    plt.title('Average Mite Percentage by State', fontsize=25)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    mites_chart_path = os.path.join(output_dir, "Average_Mite_Percentage_by_State.jpg")
    plt.savefig(mites_chart_path)
    plt.close()
    print(f"Mite bar chart saved as {mites_chart_path}")

    # Bar chart for Average Colonies by State
    plt.figure(figsize=(12, 8))
    plt.bar(state_group['State'], state_group['colonies'], color='#2643ac')
    plt.xlabel('State', fontsize=20)
    plt.ylabel('Average Colonies (per 1000 colonies)', fontsize=20)
    plt.title('Average Colonies by State', fontsize=25)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    colonies_chart_path = os.path.join(output_dir, "Average_Colonies_by_State.jpg")
    plt.savefig(colonies_chart_path, dpi=300)  # Increase resolution with dpi=300
    plt.close()
    print(f"Colonies bar chart saved as {colonies_chart_path}")









    #here is where the user pole graph is generated-----------------------

    # Read the CSV file into a DataFrame
    csv_file = 'UserDataBase/DataBase.csv'
    dfPole = pd.read_csv(csv_file)
    print('----------------------------------------------------------------')
    
    # Count how many times each state appears
    state_counts = dfPole['State'].value_counts()

    # Create a bar chart of user interest by state
    plt.figure(figsize=(8, 6))
    state_counts.plot(kind='bar', color='skyblue')
    plt.title('User Interest by State')
    plt.xlabel('State')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Define the folder and file name where the graph will be saved
    save_dir = os.path.join('graphs')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, 'UserPole.jpg')

    # Save the plot to the specified directory
    plt.savefig(save_path)
    plt.close()

    print(f"Graph saved to {save_path}")

