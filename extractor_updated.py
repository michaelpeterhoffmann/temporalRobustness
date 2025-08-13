import pandas as pd
import csv
import sys
import re

def clean_csv(input_csv_path, temp_csv_path):
    cleaned_rows = []
    with open(input_csv_path, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header
        cleaned_rows.append(header)

        for row in reader:
            # Check if the row is malformed
            if len(row) != len(header):
                # Attempt to fix the malformed row
                fixed_row = []
                row_str = ','.join(row)
                # Split the row using a regex that handles commas inside quotes
                split_row = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', row_str)
                for item in split_row:
                    fixed_row.append(item.strip().strip('"'))
                cleaned_rows.append(fixed_row)
            else:
                cleaned_rows.append(row)

    with open(temp_csv_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        writer.writerows(cleaned_rows)

    print(f"Temporary cleaned CSV saved to {temp_csv_path}")

def extract_columns(input_csv_path, output_csv_path):
    try:
        temp_csv_path = 'temp_cleaned.csv'
        clean_csv(input_csv_path, temp_csv_path)
        
        # Load the cleaned CSV file
        df = pd.read_csv(temp_csv_path, encoding='utf-8', engine='python')

        # Print the column names for debugging
        print(f"Column Names: {df.columns.tolist()}")

        # Initialize an empty dataframe for the output
        extracted_df = pd.DataFrame()

        # Loop through the columns to find pairs
        for i in range(len(df.columns) - 1):
            col1 = df.columns[i]
            col2 = df.columns[i + 1]

            # Check if the first column is text and the second column is either 0 or 1
            if df[col1].apply(lambda x: isinstance(x, str)).all() and df[col2].isin([0, 1]).all():
                temp_df = df[[col1, col2]].copy()
                temp_df.columns = ['Text', 'Label']
                extracted_df = pd.concat([extracted_df, temp_df], ignore_index=True)

        # Save the extracted dataframe to a new CSV file
        extracted_df.to_csv(output_csv_path, index=False, quoting=csv.QUOTE_ALL)

        print(f"Extracted columns saved to {output_csv_path}")

    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
    except UnicodeDecodeError as e:
        print(f"Error decoding CSV file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_columns.py <input_csv_path> <output_csv_path>")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]

    extract_columns(input_csv_path, output_csv_path)

