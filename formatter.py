import pandas as pd
import csv
import sys

def clean_and_save_csv(input_csv_path, output_csv_path):
    try:
        # Load the CSV file with error handling for malformed lines
        df = pd.read_csv(input_csv_path, encoding='utf-8', engine='python', on_bad_lines='skip')

        # Print the column names for debugging
        print(f"Column Names: {df.columns.tolist()}")

        # Combine columns 'Text' and 'text' entries that contain newlines
        if 'Text' in df.columns:
            df['Text'] = df['Text'].str.replace('\n', ' ')
        if 'text' in df.columns:
            df['text'] = df['text'].str.replace('\n', ' ')

        # Ensure the last column entry is either 0 or 1
        if 'label' in df.columns:
            df['label'] = df['label'].apply(lambda x: 1 if x != 0 else 0)

        # Save the cleaned dataframe to a new CSV file
        df.to_csv(output_csv_path, index=False, quoting=csv.QUOTE_ALL)

        print(f"Cleaned CSV saved to {output_csv_path}")

    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
    except UnicodeDecodeError as e:
        print(f"Error decoding CSV file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_csv.py <input_csv_path> <output_csv_path>")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]

    clean_and_save_csv(input_csv_path, output_csv_path)

