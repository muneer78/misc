import pdfplumber
import pandas as pd


def create_pasting_csv(pdf_path, output_file="/Users/muneer78/Downloads/temp/ready_to_paste.csv"):
    all_labels = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue

            # Process rows, skipping the header
            for row in table[1:]:
                # Mapping: 1:Name, 2:Address, 3:City, 4:State, 5:Zip
                if len(row) >= 6 and row[1]:
                    name = str(row[1]).strip()
                    street = str(row[2]).strip()
                    city = str(row[3]).strip()
                    state = str(row[4]).strip()
                    zip_code = str(row[5]).strip()

                    # Create a single block with line breaks
                    label_block = f"{name}\n{street}\n{city}, {state} {zip_code}"
                    all_labels.append(label_block)

    # Organize into 3 columns
    cols = 3
    rows = [all_labels[i:i + cols] for i in range(0, len(all_labels), cols)]

    # Pad the last row if it's not full
    if rows and len(rows[-1]) < cols:
        rows[-1].extend([""] * (cols - len(rows[-1])))

    # Create DataFrame and Save
    df = pd.DataFrame(rows)
    # We use quoting=1 (QUOTE_ALL) to ensure the line breaks stay inside the cells
    df.to_csv(output_file, index=False, header=False, quoting=1)
    print(f"Success! Open '{output_file}' to copy your grid.")

# Run this and copy the output
create_pasting_csv("/Users/muneer78/files/temp/Voter Contact Addresses.pdf")