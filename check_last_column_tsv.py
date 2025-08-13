import sys

def find_malformed_lines(input_file_path):
    malformed_lines = []
    total_lines = 0

    with open(input_file_path, 'r', encoding='utf-8') as file:
        # Read all lines from the file
        lines = file.readlines()

        # Skip the first line (header)
        for line_number, line in enumerate(lines[1:], start=2):  # Start counting from line 2
            total_lines += 1

            # Split the line by tab character
            columns = line.strip().split('\t')

            # Check if the line has exactly 2 columns
            if len(columns) != 2:
                malformed_lines.append(line_number)
                continue
            
            text, label = columns

            # Check if the second column (label) is an integer
            try:
                int(label.strip())
            except ValueError:
                malformed_lines.append(line_number)
            except TypeError:
                malformed_lines.append(line_number)

    # Calculate percentage of malformed lines
    percentage_malformed = (len(malformed_lines) / total_lines) * 100 if total_lines > 0 else 0

    # Display results
    print(f"Total lines checked (excluding header): {total_lines}")
    print(f"Number of malformed lines: {len(malformed_lines)}")
    print(f"Percentage of malformed lines: {percentage_malformed:.2f}%")

    if malformed_lines:
        print("Malformed lines found at:")
        for line in malformed_lines:
            print(f"Line {line}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_malformed_lines.py <input_file_path>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    
    find_malformed_lines(input_file_path)

