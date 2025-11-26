"""
USE: python <PROGNAME> (options) WORDLIST-FILE INPUT-FILE OUTPUT-FILE
OPTIONS:
    -h : print this help message and exit
"""
################################################################

import sys

################################################################

MAXWORDLEN = 5

################################################################
# Command line options handling, and help

def print_help():
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    sys.exit(0)

################################################################
# FUNCTION TO PROCESS ONE SENTENCE
# Sentence provided as a string. Result returned as a list of strings 

def segment(sent, wordset):
    sent = sent.strip()
    words = []
    position = 0
    length = len(sent)
    
    while position < length:
        # Optimization: Don't try length 5 if only 2 chars remain
        word_len = min(MAXWORDLEN, length - position) 
        
        while word_len > 0:
            
            # Get the candidate word
            candidate = sent[position : position + word_len]
            
            # Check if candidate is in the dictionary OR if it's a single character
            # (If a word is not found, we treat the single character as a word/unknown token)
            if candidate in wordset or word_len == 1:
                words.append(candidate)
                position += word_len # Move the position forward
                break # Break inner loop to search for the next word
            
            word_len -= 1 # Decrease length and try again
            
    return words

################################################################
# MAIN EXECUTION BLOCK

if __name__ == "__main__":
    
    # Check arguments
    if '-h' in sys.argv or len(sys.argv) != 4:
        print_help()

    word_list_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    ################################################################
    # READ CHINESE WORD LIST
    # Read words from Chinese word list file, and store in 
    # a suitable data structure (e.g. a set)

    word_list = set()

    try:
        with open(word_list_file, "r", encoding="utf-8") as f:
            for line in f:
                # Strip whitespace/newlines
                word = line.strip()
                if word: # Ensure we don't add empty strings
                    word_list.add(word)
    except IOError as e:
        print(f"Error reading word list file: {e}")
        sys.exit(1)

    ################################################################
    # MAIN LOOP
    # Read each line from input file, segment, and print to output file

    try:
        with open(input_file, "r", encoding="utf-8") as f_in:
            with open(output_file, "w", encoding="utf-8") as f_out:
                for line in f_in:
                    # 1. Segment the line
                    segmented_list = segment(line, word_list)
                    
                    # 2. Join words with spaces
                    result_line = " ".join(segmented_list)
                    
                    # 3. Write to file (add \n at the end)
                    f_out.write(result_line + "\n")
                    
        print(f"Segmentation complete. Results saved to {output_file}")
        
    except IOError as e:
        print(f"Error processing files: {e}")
        sys.exit(1)