import csv
import sys
import os

def combine_csv_files(input_files, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["text", "label"])  # Write the header for the combined file

        for file in input_files:
            with open(file, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                next(reader)  # Skip the first line (header)
                
                for row in reader:
                    if len(row) == 2:  # Ensure that the row has exactly two columns
                        writer.writerow(row)

    print(f"Combined CSV saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python combine_csv_files.py <output_file_path> <input_file_1> <input_file_2> ...")
        sys.exit(1)
    
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    
    combine_csv_files(input_files, output_file)
