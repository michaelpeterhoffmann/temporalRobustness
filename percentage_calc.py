import csv
import sys

def calculate_statistics(input_file_path):
    total_lines = 0
    lines_ending_with_0 = 0
    lines_ending_with_1 = 0

    with open(input_file_path, 'r', encoding='utf-8', newline='') as tsvfile:
        tsv_reader = csv.reader(tsvfile, delimiter='\t')

        for row in tsv_reader:
            total_lines += 1

            # Check if the last word is '0' or '1'
            if row:
                last_word = row[-1].strip()
                if last_word == '0':
                    lines_ending_with_0 += 1
                elif last_word == '1':
                    lines_ending_with_1 += 1

    # Calculate percentage of lines ending with 0 and 1
    percentage_ending_with_0 = (lines_ending_with_0 / total_lines) * 100 if total_lines > 0 else 0
    percentage_ending_with_1 = (lines_ending_with_1 / total_lines) * 100 if total_lines > 0 else 0

    print(f"Total number of lines: {total_lines}")
    print(f"Number of lines ending with 0: {lines_ending_with_0}")
    print(f"Number of lines ending with 1: {lines_ending_with_1}")
    print(f"Percentage of lines ending with 0: {percentage_ending_with_0:.2f}%")
    print(f"Percentage of lines ending with 1: {percentage_ending_with_1:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_statistics.py <input_file_path>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    
    calculate_statistics(input_file_path)

