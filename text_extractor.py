import re
import sys

def extract_texts(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                # Extract texts inside double quotes
                quotes = re.findall(r'"(.*?)"', line)
                
                # Extract the last sentence before a comma
                last_sentence_match = re.search(r'([^,]*),', line[::-1])
                last_sentence = last_sentence_match.group(1)[::-1].strip() if last_sentence_match else ""

                # Write extracted content to the output file
                if quotes:
                    outfile.write(f'Text inside quotes: {", ".join(quotes)}\n')
                if last_sentence:
                    outfile.write(f'Last sentence before comma: {last_sentence}\n')

        print(f"Texts extracted and saved to {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_texts.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    extract_texts(input_file_path, output_file_path)
