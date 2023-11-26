# Corrected function to handle NaN values in the CSV
import pandas as pd


def convert_google_form_to_available_times(input_csv_path, output_csv_path):
    # Read the input CSV file
    df = pd.read_csv(input_csv_path)

    # Extract the column headers for time slots from the CSV
    time_slot_columns = [col for col in df.columns if col.startswith("Availabilities")]
    time_slots = [col.split("[")[-1].split("]")[0] for col in time_slot_columns]

    # Define the days of the week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Initialize a list to hold the processed data
    processed_data = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Initialize a dictionary to hold the availabilities
        availabilities = {
            f"{day} {time}": "FALSE" for time in time_slots for day in days
        }
        # Get the name of the person
        name = row["First Name"]
        # Process each time slot
        for column_name in time_slot_columns:
            time = column_name.split("[")[-1].split("]")[0]
            # Check if the entry is a string and not NaN
            if isinstance(row[column_name], str):
                # Get the string of days for the current time slot
                days_available = row[column_name]
                # Split the days and remove any whitespace
                days_list = [day.strip() for day in days_available.split(",") if day]
                # Fill the availability for each day of the week
                for day in days_list:
                    availabilities[f"{day} {time}"] = "TRUE"
        # Add the processed row to the list
        processed_data.append(
            [name]
            + [availabilities[f"{day} {time}"] for day in days for time in time_slots]
        )

    # Create a new DataFrame for the processed data
    processed_df = pd.DataFrame(
        processed_data,
        columns=["NAME"] + [f"{day} {time}" for day in days for time in time_slots],
    )

    # Save the processed data to the specified output CSV file
    processed_df.to_csv(output_csv_path, index=False)


# Paths to the input and output CSV files
input_csv_path = "base_times.csv"
output_csv_path = "outputTEST.csv"

# Call the function to convert the input CSV to the required format
convert_google_form_to_available_times(input_csv_path, output_csv_path)

# Let's check the first few lines of the output to verify
pd.read_csv(output_csv_path).head()
