import csv
import sys
import pandas as pd

def clean_and_save_csv(input_csv_path, temp_csv_path):
    with open(input_csv_path, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        expected_columns = len(header)

        cleaned_rows = []
        cleaned_rows.append(header)
        
        current_row = []

        for row in reader:
            if not row:
                continue

            current_row.extend(row)
            
            # Check if the current row has the expected number of columns and ends with 0, 1, or 2,
            # and the second last column is a text string.
            if len(current_row) >= expected_columns and (current_row[-1] in ['0', '1', '2']) and isinstance(current_row[-2], str):
                cleaned_rows.append(current_row[:expected_columns])
                current_row = []

    # Append the last accumulated row if it's valid
    if current_row and (current_row[-1] in ['0', '1', '2']) and isinstance(current_row[-2], str):
        cleaned_rows.append(current_row)

    with open(temp_csv_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        writer.writerows(cleaned_rows)

    print(f"Temporary cleaned CSV saved to {temp_csv_path}")

def extract_columns(input_csv_path, output_csv_path, columns):
    try:
        # Clean the CSV to handle multi-line entries
        temp_csv_path = 'temp_cleaned.csv'
        clean_and_save_csv(input_csv_path, temp_csv_path)
        
        # Load the cleaned CSV file
        df = pd.read_csv(temp_csv_path, encoding='utf-8', engine='python')

        # Print the column names for debugging
        print(f"Column Names: {df.columns.tolist()}")

        # Ensure the specified columns exist
        for col in columns:
            if col not in df.columns:
                raise ValueError(f"The column '{col}' does not exist in the input CSV file.")

        # Extract the specified columns
        extracted_df = df[columns]

        # Debug: print the first few rows of the extracted dataframe
        print("Extracted DataFrame (first few rows):")
        print(extracted_df.head())

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
    if len(sys.argv) < 4 or len(sys.argv) > 6:
        print("Usage: python extract_columns.py <input_csv_path> <output_csv_path> <column1> [<column2> <column3>]")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    columns = sys.argv[3:]

    print(f"Input CSV Path: {input_csv_path}")
    print(f"Output CSV Path: {output_csv_path}")
    print(f"Columns to extract: {columns}")

    extract_columns(input_csv_path, output_csv_path, columns)
