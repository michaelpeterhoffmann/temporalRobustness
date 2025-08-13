import csv
import sys
import random

def split_tsv_file(input_file_path, train_file_path, dev_file_path, split_ratio=0.8):
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        tsv_reader = list(csv.reader(infile, delimiter='\t'))
        
        # Extract header
        header = tsv_reader[0]

        # Extract data without header
        data = tsv_reader[1:]

        # Shuffle the data to ensure randomness
        random.shuffle(data)

        # Calculate split index for 80:20 ratio
        split_index = int(len(data) * split_ratio)

        # Split data into train and dev sets
        train_data = data[:split_index]
        dev_data = data[split_index:]

        # Write to train.tsv
        with open(train_file_path, 'w', encoding='utf-8', newline='') as train_file:
            tsv_writer = csv.writer(train_file, delimiter='\t')
            tsv_writer.writerow(header)  # Write header
            tsv_writer.writerows(train_data)  # Write train data

        # Write to dev.tsv
        with open(dev_file_path, 'w', encoding='utf-8', newline='') as dev_file:
            tsv_writer = csv.writer(dev_file, delimiter='\t')
            tsv_writer.writerow(header)  # Write header
            tsv_writer.writerows(dev_data)  # Write dev data

    print(f"TSV file split completed: {train_file_path} and {dev_file_path} created.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_tsv_file.py <input_file_path>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    train_file_path = "train.tsv"
    dev_file_path = "dev.tsv"

    split_tsv_file(input_file_path, train_file_path, dev_file_path)

