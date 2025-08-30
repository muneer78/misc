# Define the input strings
input_strings = [
    "0 as oil,",
    "0 as oiltotal,",
    "0 as reefergallons,",
    "0 as reeferamt,",
    "0 as fueladdqty,",
    "0 as fueladdtotal,",
    "0 as partstotal,",
    "0 as tirerepairqty,",
    "0 as tirerepairtotal,",
    "0 as tirepurchqty,",
    "0 as tirepurchtotal,",
    "0 as permittotal,",
    "0 as moteltotal,",
    "0 as scalestotal,",
    "0 as wash,",
    "0 as meals,",
]

# Remove '0 as', ',', and double quotes from each string
cleaned_strings = [
    s.replace("0 as ", "").replace(",", "").replace('"', "") for s in input_strings
]

# Sort the cleaned strings in alphabetical order
cleaned_strings.sort()

# Print the sorted strings
for s in cleaned_strings:
    print(s)
