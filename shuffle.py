import pandas as pd
import random
import sys

def shuffle_tsv(input_file, output_file):
    # Read the TSV file
    df = pd.read_csv(input_file, sep='\t')

    # Extract the header and data separately
    header = df.columns.tolist()  # Preserve the header
    data = df.values.tolist()     # Get the data as a list of rows

    # Shuffle the data
    random.shuffle(data)

    # Write the shuffled data back to a new TSV file, keeping the header
    with open(output_file, 'w', newline='') as out_file:
        out_file.write('\t'.join(header) + '\n')  # Write the header
        for row in data:
            out_file.write('\t'.join(map(str, row)) + '\n')  # Write each row

    print(f"Data shuffled and saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python shuffle_tsv.py <input_tsv_file> <output_tsv_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    shuffle_tsv(input_file, output_file)

