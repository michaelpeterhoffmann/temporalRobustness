import re
import sys

# Define the specific strings to look for, originally followed by a comma
KEY_STRINGS = [
    "exclusionary extreme speech,",
    "derogatory extreme speech,",
    "dangerous speech,"
]

def process_csv(input_csv_path, output_csv_path):
    try:
        # Read the input file
        with open(input_csv_path, 'r', encoding='utf-8') as infile:
            # Read the first line (header)
            header = infile.readline().strip()

            # Read the rest of the file as a single string
            content = infile.read()

        # Remove all newlines to treat it as a single large string
        content = content.replace('\n', ' ').replace('\r', ' ')

        # Use a regex pattern to split the content based on the key strings
        pattern = r'(' + '|'.join(re.escape(key) for key in KEY_STRINGS) + r')'
        parts = re.split(pattern, content)

        # Reconstruct the lines ensuring they end with the key strings, and remove the trailing comma
        processed_lines = []
        current_line = parts[0].strip()
        
        for i in range(1, len(parts), 2):
            key_string = parts[i]
            next_part = parts[i + 1].strip() if i + 1 < len(parts) else ''
            
            # Combine the current line with the key string, then remove the trailing comma
            current_line = (current_line + ' ' + key_string).strip().rstrip(',')
            processed_lines.append(current_line)
            current_line = next_part
        
        # Handle any remaining text in current_line
        if current_line:
            processed_lines.append(current_line.strip().rstrip(','))

        # Write the processed lines to the output CSV manually
        with open(output_csv_path, 'w', encoding='utf-8') as outfile:
            outfile.write(header + '\n')  # Write the header first
            for line in processed_lines:
                outfile.write(line + '\n')

        print(f"Processed CSV saved to {output_csv_path}")

        # Re-open the output file and process each line to remove everything before and including the timestamp
        with open(output_csv_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        # Pattern to match the timestamp
        timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

        with open(output_csv_path, 'w', encoding='utf-8') as outfile:
            outfile.write(lines[0])  # Re-write the header
            outfile.write(lines[1])  # Re-write the second line
            for line in lines[2:]:  # Start processing from the third line
                # Find the position of the timestamp in the line
                match = re.search(timestamp_pattern, line)
                if match:
                    # Remove everything up to and including the timestamp
                    line = line[match.end():].strip()
                    if line:
                        outfile.write(line + '\n')
                else:
                    outfile.write(line.strip() + '\n')

        print(f"Final processed CSV with timestamps removed saved to {output_csv_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_csv.py <input_csv_path> <output_csv_path>")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]

    process_csv(input_csv_path, output_csv_path)
