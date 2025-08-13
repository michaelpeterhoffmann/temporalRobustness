import pandas as pd
import sys

def split_tsv(input_file, output_file1, output_file2, split_ratio=0.8):
    # Read the TSV file
    df = pd.read_csv(input_file, sep='\t')

    # Extract the header
    header = df.columns.tolist()  # Preserve the header

    # Shuffle the data
    df = df.sample(frac=1).reset_index(drop=True)

    # Determine split index
    split_index = int(len(df) * split_ratio)

    # Split the data
    df1 = df.iloc[:split_index]
    df2 = df.iloc[split_index:]

    # Write the first split to output_file1 with the header
    df1.to_csv(output_file1, sep='\t', index=False)

    # Write the second split to output_file2 with the header
    df2.to_csv(output_file2, sep='\t', index=False)

    print(f"Data split into {output_file1} (80%) and {output_file2} (20%).")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python split_tsv.py <input_tsv_file> <output_file1> <output_file2>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file1 = sys.argv[2]
    output_file2 = sys.argv[3]

    split_tsv(input_file, output_file1, output_file2)

