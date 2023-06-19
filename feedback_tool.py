from feedback_tool_helper_functions import *

# Extracts the readability features of a code snippet
# a = "numLines", b = "avgCharsLine", c = "ratioComment", d = "ratioBlank", 
# e = "avgNewId", f = "avgIdLen", g = "ratioIndentNumLines", h = "commentReadabilityFK"
def code_extract(file_path):
    tmp0 = count_source_lines_chars_helper(file_path)
    numLines = tmp0[0]

    a = numLines
    b = tmp0[2]/numLines
    c = calculate_comment(file_path)[1]
    d = tmp0[1]/numLines
    long_lines = tmp0[3]

    tmp1 = identifiers_helper(file_path)
    e = tmp1[2]/numLines
    f = tmp1[5]
    num_Id_in_line = tmp1[6]
    long_Id = tmp1[7]
    
    g = count_blocks(file_path)/numLines
    
    tmp2 = average_readability_helper(file_path)
    h = tmp2[1]
    diff_Comment = tmp2[2]

    return log_reg_eqn(a, b, c, d, e, f, g, h), a, b, c, d, e, f, g, h, long_lines, num_Id_in_line, long_Id, diff_Comment


def code_feedback(directory):
    # Extract code features
    code_features = code_extract(directory)
    long_lines = code_features[9]
    num_Id_in_line = code_features[10]
    long_Id = code_features[11]
    diff_Comment = code_features[12]
    
    readability_score = code_features[0]
    code_features = code_features[1:9]
    print("### Readability score: " + str(round(readability_score*100, 1)) + "%")
    a, b, c, d, e, f, g, h = code_features
    if (readability_score >= 0.7):
        print("The code you provided is readable, Here's what you did well:")
        print("__________________________________________________________________________________________________________")
        print()
        if (a <= 500):
            print("Good job on keeping the line count under control. This makes your code easier to read and maintain.")
            print()
            print(f"Current number of lines: {a} lines")
            print()
            print("----------------------------------------------------------------------------------------------------------")
            print() 

        if (b <= 55):
            print("Well done on keeping your lines within an acceptable length. This improves readability.")
            print()
            print(f"Current average characters per line: {b:.2f} characters")
            print()
            print("----------------------------------------------------------------------------------------------------------")
            print() 

        if (c >= 0.2):
            print("Great job on including comments in your code. This helps others understand your code more easily.")
            print()
            print(f"Current comment-to-code ratio: {c:.2f}")
            print()
            print("----------------------------------------------------------------------------------------------------------")
            print() 

        if (d >= 0.2):
            print("Good use of whitespace in your code. This makes your code more visually appealing and easier to read.")
            print()
            print(f"Current blank lines-to-code ratio: {d:.2f}")
            print()
            print("----------------------------------------------------------------------------------------------------------")
            print() 

        if (e <= 1):
            print("Nice work on minimizing the number of new identifiers per line. This helps make your code less complex.")
            print()
            print(f"Current average new identifiers per line: {e:.2f}")
            print()
            print("----------------------------------------------------------------------------------------------------------")
            print() 

        if (f <= 9):
            print("Good job on using concise and clear identifier names. This makes your code easier to understand.")
            print()
            print(f"Current average identifier length: {f:.2f} characters")
            print()
            print("----------------------------------------------------------------------------------------------------------")
            print() 

        if (g <= 0.5):
            print("Your code structure is well-organized, making it easier to follow and understand.")
            print()
            print(f"Current number of code in same indentation-to-overall-code ratio: {g:.2f}")
            print()
            print("----------------------------------------------------------------------------------------------------------")
            print() 

        if (h >= 75 or h == 0):
            print("Your comments are clear and easy to read. Keep up the good work!")
            print()
            print(f"Current average Flesch-Kincaid readability score: {h:.2f} (Higher is more readable)")
            return
    else:
        if (readability_score > 0.5):
            print("The code you provided is somewhat readable. Here are some areas to improve:")
            print("_____________________________________________________________________________________________________________________________________________")
        else:
            print("The code you provided is not readable. Here are some suggestions for improvement:")
            print("_____________________________________________________________________________________________________________________________________________")

        print()
        

        if (a > 500):
            print("Your code has too many lines. Consider simplifying your code or splitting it into multiple files to reduce the line count to below 500.")
            print()
            print(f"Current number of lines: {a} lines")
            print()
            print("Example: If you have a large function, consider breaking it down into smaller, more focused functions.")
            print()
            print("---------------------------------------------------------------------------------------------------------------------------------------------")
            print() 

        if (b > 55):
            print(f"Some of your lines are too long. Aim to keep lines under 80 characters.")
            print()
            print(f"Current average characters per line: {b:.2f} characters")
            print()
            print("Example: Instead of chaining multiple operations on one line, split them across multiple lines.")
            print()
            print("These are your long lines:")
            print()
            for line in long_lines:
                print("     " + "line " + str(line[0]) + ": " + str(line[1]))
            print()
            print("---------------------------------------------------------------------------------------------------------------------------------------------")
            print() 

        if (c < 0.2):
            print(f"Your code could use more comments. Aim for a comment-to-code ratio of at least 1:4.")
            print()
            print(f"Current comment-to-code ratio: {c:.2f}")
            print()
            print("Example: Write comments to explain the purpose of functions, complex logic, or important variables.")
            print()
            print("---------------------------------------------------------------------------------------------------------------------------------------------")
            print() 

        if (d < 0.2):
            print(f"Increase the whitespace in your code to improve readability. Aim for a blank line ratio of at least 0.2")
            print()
            print(f"Current blank lines-to-code ratio: {d:.2f}")
            print()
            print("Example: Add blank lines between functions or logical sections of your code.")
            print()
            print("---------------------------------------------------------------------------------------------------------------------------------------------")
            print() 

        if (e > 1):
            print(f"Too many new identifiers are introduced per line. Simplify your variables and reduce the number of new variables if possible.")
            print()
            print(f"Current average new identifiers per line: {e:.2f}")
            print()
            print("Example: Group related variables together or use data structures like lists or dictionaries.")
            print()
            print("Listed below are lines of your code with more than 2 variable:")
            print()
            lineNum = 0
            for line in num_Id_in_line:
                if line > 2:
                    print("line " + str(lineNum))
                    print()
                lineNum += 1
            print()
            print("---------------------------------------------------------------------------------------------------------------------------------------------")
            print() 

        if (f > 9):
            print("Your identifier names are too long. Keep them between 6-9 characters and ensure the names clearly indicate their purpose.")
            print()
            print(f"Current average identifier length: {f:.2f} characters")
            print()
            print("Example: Instead of 'input_string', use 'in_str' as a shorter, yet stillclear alternative.")
            print()
            print("Here are your long identifiers:")
            print()
            for id in long_Id:
                print("'" + id + "'")
                print()
            print()
            print("---------------------------------------------------------------------------------------------------------------------------------------------")
            print() 

        if (g > 0.5):
            print(f"Your code structure could be improved. Organize related segments of code in the same block (same indentation level).")
            print()
            print(f"Current number of code in same indentation-to-overall-code ratio: {g:.2f}")
            print()
            print("Example: Use consistent indentation to clearly show the structure and nesting of your code.")
            print()
            print("---------------------------------------------------------------------------------------------------------------------------------------------")
            print() 

        if (h < 75 and h != 0):
            print(f"Your comments are difficult to read. Write in simple and concise English using easy-to-understand words.")
            print()
            print(f"Current average Flesch-Kincaid readability score: {h:.2f} (Higher is more readable)")
            print()
            print("Example: Instead of 'This function initializes the variables for the algorithm', write 'Initialize variables for the algorithm'.")
            print()
            print("Here are your difficult comments:")
            print()
            for comment in diff_Comment:
                print("'" + comment + "'")
                print()
            print()

