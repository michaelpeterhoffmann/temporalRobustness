import pandas as pd
import sys
import csv

def filter_columns_and_save_csv(input_csv_path, output_csv_path, columns):
    try:
        # Increase the maximum field size limit
        max_int = sys.maxsize
        while True:
            # Decrease the max_int value by factor 10 as long as the OverflowError occurs
            try:
                csv.field_size_limit(max_int)
                break
            except OverflowError:
                max_int = int(max_int / 10)

        # Load the CSV file
        df = pd.read_csv(input_csv_path, encoding='utf-8', engine='python', on_bad_lines='skip')

        # Print column names for debugging
        print(f"Column Names: {df.columns.tolist()}")

        # Ensure all specified columns exist in the dataframe
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"The input CSV file does not contain the columns: {missing_columns}")

        # Debug: print the first few rows of the dataframe
        print("First few rows of the dataframe:")
        print(df.head())

        # Select only the specified columns
        filtered_df = df[columns]

        # Debug: print the first few rows of the filtered dataframe
        print("First few rows of the filtered dataframe:")
        print(filtered_df.head())

        # Save the filtered dataframe to a new CSV file
        filtered_df.to_csv(output_csv_path, index=False)

        print(f"Filtered CSV saved to {output_csv_path}")

    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
    except UnicodeDecodeError as e:
        print(f"Error decoding CSV file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python filter_columns.py <input_csv_path> <output_csv_path> <column1> [<column2> ... <columnN>]")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    columns = sys.argv[3:]

    print(f"Input CSV Path: {input_csv_path}")
    print(f"Output CSV Path: {output_csv_path}")
    print(f"Columns to include: {columns}")

    filter_columns_and_save_csv(input_csv_path, output_csv_path, columns)

