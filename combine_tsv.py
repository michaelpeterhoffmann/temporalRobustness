import pandas as pd
import sys

def combine_tsv_files(file1, file2, file3, output_file):
    # Read the first file and store the header
    df1 = pd.read_csv(file1, sep='\t')

    # Read the second and third files, skipping the header
    df2 = pd.read_csv(file2, sep='\t', header=0)
    df3 = pd.read_csv(file3, sep='\t', header=0)

    # Combine all three DataFrames
    combined_df = pd.concat([df1, df2, df3], ignore_index=True)

    # Write the combined DataFrame to a new TSV file
    combined_df.to_csv(output_file, sep='\t', index=False)

    print(f"Files {file1}, {file2}, and {file3} have been combined into {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python combine_tsv.py <file1> <file2> <file3> <output_file>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    file3 = sys.argv[3]
    output_file = sys.argv[4]

    combine_tsv_files(file1, file2, file3, output_file)

