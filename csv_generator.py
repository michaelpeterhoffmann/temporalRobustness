import sys
import re

def extract_third_column(line):
    """Extracts the third column from the line, handling both quoted and non-quoted text."""
    # Split the line into fields considering possible quoted fields with commas inside
    fields = []
    current_field = ''
    inside_quotes = False
    
    for char in line:
        if char == '"' and not inside_quotes:
            inside_quotes = True
            current_field += char
        elif char == '"' and inside_quotes:
            inside_quotes = False
            current_field += char
        elif char == ',' and not inside_quotes:
            fields.append(current_field.strip())
            current_field = ''
        else:
            current_field += char
            
    # Add the last field
    if current_field:
        fields.append(current_field.strip())
    
    # Return the third column
    if len(fields) >= 3:
        return fields[2]
    else:
        return ""

def process_file(input_file_path, output_file_path):
    speech_types = {"derogatory extreme speech", "exclusionary extreme speech", "dangerous speech"}
    
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()

        for i in range(len(lines) - 1):
            # Split the current line by commas
            current_line_fields = lines[i].strip().split(',')

            # Check if the last field (sentence) matches one of the speech types
            last_field = current_line_fields[-1].strip()
            if last_field in speech_types:
                # Go to the next line and extract the text from the third column
                next_line = lines[i + 1].strip()
                third_column_text = extract_third_column(next_line)
                
                # Write the text followed by the sentence to the output file (switching the order)
                outfile.write(f'{third_column_text},{last_field}\n')

    print(f"Processed output saved to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_file.py <input_file_path> <output_file_path>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    
    process_file(input_file_path, output_file_path)
