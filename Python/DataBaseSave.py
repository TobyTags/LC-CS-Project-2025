def CSV_Save(data):
    import csv
    import os

    print(data) #error handling to see what data is recived from the form


    file_path = 'UserDataBase/DataBase.csv'

    # Check if the file exists, create if not
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # If the file is new, write the header first
        if not file_exists:
            writer.writerow(["Name", "Email", "State"])  # Column headers

        # Append new row with data
        writer.writerow([data["name"], data["email"], data["option"]])

    
  