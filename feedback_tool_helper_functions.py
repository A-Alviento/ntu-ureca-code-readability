def count_source_lines_chars_helper(file_path):
    # Open the file for reading
    with open(file_path, 'r') as f:
        # Initialize a counter variable to keep track of the number of source code lines
        count = 0
        count1 = 0
        # keep count of end blank lines
        count2 = 0
        # check if this is the first non-blank line
        firstNonBlank = False
        chars = 0
        long_lines = []

        # Loop through each line in the file
        for line_num, line in enumerate(f, start=1):
            # Check if the line is blank line
            if line.strip() == '':
                if firstNonBlank:
                    count1 += 1 
                    count2 += 1 
                continue
            # If the line is not a blank line, increment the counter
            else:
                count += 1
                chars += len(line)
                count2 = 0
                firstNonBlank = True
                if len(line) > 55:
                    long_lines.append((line_num, line))

        # Return the number of source code lines, number of end blank lines, total number of characters, and long lines
        return count, count1 - count2, chars, long_lines


import re

# Function to estimate the number of syllables in a given word
def count_syllables(word):
    vowels = 'aeiouy'
    count = 0
    prev_char_vowel = False

    # Loop through each character in the word
    for char in word.lower():
        if char in vowels:
            if not prev_char_vowel:
                count += 1
            prev_char_vowel = True
        else:
            prev_char_vowel = False
    
    # If the word ends with 'e', subtract one from the syllable count
    if word.lower().endswith('e'):
        count -= 1
    # If the word has no vowels, set the count to 1
    if count == 0:
        count = 1

    # Return the number of syllables in the word
    return count


# Function to calculate the readability of a text
def readability(text):
    # Split the text into words and sentences
    words = re.findall(r'\b\w+\b', text)
    sentences = re.findall(r'[^.!?]+[.!?]', text)
    sentences = len(sentences)

    # Create a list to store complex words (words with three or more syllables)
    complex_words = []
    # Calculate the total number of syllables in the text
    totalSyllables = 0
    
    # If there are no sentences, set the number of sentences to 1 to avoid division by zero
    if sentences == 0:
        sentences = 1

    # Loop through each word in the text and count the number of syllables
    for word in words:
        syllables = count_syllables(word)
        totalSyllables += syllables

        # If the word has three or more syllables, add it to the list of complex words
        if (syllables >= 3):
            complex_words.append(word)
    
    # Count the number of complex words in the text
    num_complex_words = len(complex_words)

    # Calculate the Gunning Fog score
    gunningFogScore = 0.4 * (len(words) / sentences + 100 * (num_complex_words / len(words)))
    # Calculate the Flesch-Kincaid score
    fleschKincaidScore = 206.835 - 1.015*(len(words)/sentences) - 84.6*(totalSyllables/len(words))

    # Return the readability scores
    return gunningFogScore, fleschKincaidScore



# Function to calculate the average readability of a file containing multiple comments
def average_readability_helper(file_path):
    # Create a list to store the readability scores of each comment
    scores = []
    # Create a list to store comments with FK score less than 75
    difficult_comments = []

    # Open the file containing the comments
    with open(file_path, 'r') as f:
        text = f.read()
        # Extract all the comments from the file
        comments = re.findall(r'(?:/\*(?:[^*]|(?:\*+[^*/]))*\*+/)|(?://.*)', text)

        # If there are no comments in the file, return a default score
        if not comments:
            return 20, 0, []
        
        # Loop through each comment in the file and calculate its readability score
        for comment in comments:
            # Only consider comments that contain at least one word
            if (len(re.findall(r'\b\w+\b', comment)) != 0):
                scores.append(readability(comment))
            if readability(comment)[1] < 75:
                difficult_comments.append(comment)
            # If no comments meet the criteria, return a default score
            if (len(scores) == 0):
                return 20, 0, []

            readabilityGF = 0
            readabilityFK = 0
            # Calculate the average readability scores of all the comments
            for score in scores:
                readabilityGF += score[0]
                readabilityFK += score[1]

        # Return the average readability scores and difficult comments
        return readabilityGF/len(scores), readabilityFK/len(scores), difficult_comments


import re
import tokenize
from io import BytesIO
import keyword
import spacy
nlp = spacy.load("en_core_web_sm")
import spellchecker

# List of Java keywords
java_keywords = ["abstract", "continue", "for", "new", "switch", "assert", "default", "goto", "package", "synchronized", "boolean", "do", "if", "private", "this", "break", "double", "implements", "protected", "throw", "byte", "else", "import", "public", "throws", "case", "enum", "instanceof", "return", "transient", "catch", "extends", "int", "short", "try", "char", "final", "interface", "static", "void", "class", "finally", "long", "strictfp", "volatile", "const", "float", "native", "super", "while", "Object", "null", "true", "false"]



# This function checks if a given word is in english dictionary
def contains_in_vocab(word):
    # Split the line into words based on capital letters
    words = re.findall(r"[A-Z]?[a-z]+|'[^']+'|\"[^\"]+\"", word)
    tokens = []

    for word in words:
        # Check if word is enclosed in quotes
        if not (word.startswith("'") and word.endswith("'") or word.startswith('"') and word.endswith('"')):
            # Tokenize the word if it's not enclosed in quotes
            tokens.extend(tokenize.tokenize(BytesIO(word.encode("utf-8")).readline))
    
    for token_type, token_string, _, _, _ in tokens:
        spell = spellchecker.SpellChecker()
        if (spell.correction(token_string) == token_string):
            return True
    return False



# This function tokenizes a given line of code
def tokenizeLine(line):    
    # Split the line into words based on non-alphanumeric characters
    words = re.findall(r"[A-Za-z]+|'[^']+'|\"[^\"]+\"", line)
    tokens = []
    for word in words:
        if not (word.startswith("'") and word.endswith("'") or word.startswith('"') and word.endswith('"')):
            tokens.extend(tokenize.tokenize(BytesIO(word.encode("utf-8")).readline))
    return tokens



# This function counts the number of identifiers, English identifiers, unique identifiers, unique English identifiers, 
# and identifiers with length between 6 and 9 characters in a given file.
def identifiers_helper(file_path):
    # Read the file
    with open(file_path, "r") as file:
        code = file.read()
    
    # Initialize variables
    lines = code.split("\n")
    numLines = len(lines)
    identifiers_eng = []
    identifier_set = []
    numId6_9 = 0
    id_len = []
    line_count = 0
    new_identifiers = []
    for i in range(numLines+1):
        new_identifiers.append(0)
    long_identifiers = []

    for line in lines:
        line_count += 1
        tokens = tokenizeLine(line)
        
        # Check if the token is an identifier and not a Java keyword
        for token_type, token_string, _, _, _ in tokens:
            if token_type == tokenize.NAME and token_string not in java_keywords:
                identifier_set.append(token_string)
                id_len.append(len(token_string))
            
                # Check if the identifier is an English word
                if (contains_in_vocab(token_string)):
                    identifiers_eng.append(token_string)
                # Check if the identifier has length between 6 and 9 characters
                if (len(token_string) <= 9 and len(token_string) >= 6):
                    numId6_9 += 1

                new_identifiers[line_count] += 1

                # Check if the identifier has more than 9 characters
                if (len(token_string) > 9):
                    long_identifiers.append(token_string)
    # Count the number of unique identifiers and unique English identifiers
    unique_identifiers = set(identifier_set)
    unique_eng_identifiers = set(identifiers_eng)

    return len(identifier_set), len(identifiers_eng), len(unique_identifiers), len(unique_eng_identifiers), numId6_9, sum(id_len)/len(identifier_set), new_identifiers, long_identifiers




# This function takes in a filepath and returns the number of indentation blocks in the file
def count_blocks(filepath):
    # Open the file and read all the lines
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    # Create an empty list to store the number of blocks and initialize the current block indentation to None
    blocks = []
    current_block_indentation = None
    
    # Loop through all the lines
    for line in lines:
        # Strip any whitespace from the beginning of the line
        stripped_line = line.lstrip()
        
         # If the line is not empty
        if stripped_line:
            indentation = len(line) - len(stripped_line)
            
            # If there is no current block indentation, create a new block and add it to the list
            if current_block_indentation is None:
                current_block_indentation = indentation
                blocks.append(1)

            # If the current indentation is the same as the previous block, add it to that block
            elif indentation == current_block_indentation:
                blocks[-1] += 1
            
            # Otherwise, create a new block and add it to the list
            else:
                current_block_indentation = indentation
                blocks.append(1)
    
    # Return the number of blocks
    return len(blocks)


def calculate_comment(file_path):
    # Initialize counters for total lines and comment lines
    total_lines = 0
    comment_lines = 0

    # Open the file for reading
    with open(file_path, "r") as file:
        # Iterate through each line in the file
        for line in file:
            # Strip leading and trailing whitespaces from the line
            line = line.strip()
            # Increment the total lines counter
            total_lines += 1

             # If the line starts with "//", it is a single line comment
            if line.startswith("//"):
                comment_lines += 1

            # If the line starts with "/*", it is the beginning of a multi-line comment
            elif line.startswith("/*"):
                comment_lines += 1
                 # Keep reading lines until the end of the multi-line comment "*/" is reached
                while "*/" not in line:
                    line = next(file).strip()
                    total_lines += 1
                    comment_lines += 1

            # If the line contains "/*" but not "*/", it is the middle of a multi-line comment
            elif "/*" in line and "*/" not in line:
                comment_lines += 1
                # Keep reading lines until the end of the multi-line comment "*/" is reached
                while "*/" not in line:
                    line = next(file).strip()
                    total_lines += 1
                    comment_lines += 1
                # Increment the comment lines counter to include the end of the multi-line comment "*/"
                comment_lines += 1
                
    # Return both the total number of comment lines and the average number of comments per line
    return comment_lines, comment_lines/total_lines



# Define the logistic regression model
def log_reg_eqn(a, b, c, d, e, f, g, h):
    # your function implementation here
    func = e**(-(10.936868407 - 0.183089593*a - 0.056055262*b + 11.561057751*c + 3.019670203*d - 1.380159181*e - 0.188496425*f - 2.852907733*g + 0.001926625*h))
    # func = e**(-(10.496798 - 0.186879*a - 0.064361*b + 12.669662*c + 3.105942*d - 1.380851*e - 0.089375*f - 2.857258*g + 0.003225*h))
    return 1/(1+func)
