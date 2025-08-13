import csv
import sys

def identify_malformed_lines(input_csv_path, output_txt_path):
    malformed_lines = []

    with open(input_csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        column_names = reader.fieldnames

        if 'Text' not in column_names or 'text' not in column_names:
            raise ValueError("The input CSV file must contain 'Text' and 'text' columns.")

        for line_number, row in enumerate(reader, start=2):  # start=2 to skip header line
            for column in ['Text', 'text']:
                entry = row[column]
                if entry is not None and ',' in entry and not (entry.startswith('"') and entry.endswith('"')):
                    malformed_lines.append((line_number, row))

    with open(output_txt_path, 'w', encoding='utf-8') as output_file:
        for line_number, line in malformed_lines:
            output_file.write(f"Line {line_number}: {line}\n")

    print(f"Malformed lines identified and written to {output_txt_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python identify_malformed_lines.py <input_csv_path> <output_txt_path>")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_txt_path = sys.argv[2]

    identify_malformed_lines(input_csv_path, output_txt_path)

