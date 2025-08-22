import csv


# Function to read data from a CSV file and create tuples
def read_csv_to_tuples(csv_file):
    tuples_list = []
    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Change 'column1' and 'column2' to match your CSV column names
            name = row["name"]
            bet_amount = (
                float(row["bet_amount"])
                if "." in row["bet_amount"]
                else int(row["bet_amount"])
            )
            odds = float(row["odds"]) if "." in row["odds"] else int(row["odds"])
            bet_group = row["bet_group"]
            tuple_data = (name, bet_amount, odds, bet_group)
            tuples_list.append(tuple_data)
    return tuples_list


# Replace 'mybetgroup.csv' with your CSV file path
csv_file_path = "mybetgroup.csv"
data_tuples = read_csv_to_tuples(csv_file_path)

# Example usage:
for i, data_tuple in enumerate(data_tuples):
    print(data_tuple, end=", " if i < len(data_tuples) - 1 else "\n")
