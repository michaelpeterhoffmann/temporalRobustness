import csv
import sys
import re

def is_single_word(text):
    """
    Check if the text is a single word (no spaces or punctuation).
    """
    return re.match(r'^[^\s]+$', text) is not None

def is_only_emojis(text):
    """
    Check if the text contains only emojis.
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u200d"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\u3030"
        "\ufe0f"  # dingbats
        "\u2069"
        "\u2066"
        "\u200c"
        "\u202f"
        "\u205f"
        "\u3000"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.fullmatch(text) is not None

def detect_special_lines(input_file_path):
    total_lines = 0
    emoji_lines = 0
    single_word_lines = 0

    with open(input_file_path, 'r', encoding='utf-8') as tsvfile:
        tsv_reader = csv.reader(tsvfile, delimiter='\t')
        
        # Skip the header
        header = next(tsv_reader)

        for row in tsv_reader:
            total_lines += 1
            sentence = row[0].strip()  # Get the "sentence" column

            if is_only_emojis(sentence):
                emoji_lines += 1
            elif is_single_word(sentence):
                single_word_lines += 1

    # Calculate percentages
    percentage_emoji = (emoji_lines / total_lines) * 100 if total_lines > 0 else 0
    percentage_single_word = (single_word_lines / total_lines) * 100 if total_lines > 0 else 0

    # Output results
    print(f"Total lines (excluding header): {total_lines}")
    print(f"Number of lines with only emojis: {emoji_lines}")
    print(f"Percentage of lines with only emojis: {percentage_emoji:.2f}%")
    print(f"Number of lines with a single word: {single_word_lines}")
    print(f"Percentage of lines with a single word: {percentage_single_word:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detect_special_lines.py <input_file_path>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    
    detect_special_lines(input_file_path)

