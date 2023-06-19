import streamlit as st
import sys
import io
from feedback_tool import code_feedback

# Set the page config to have a wider layout and a nice title.
st.set_page_config(layout="wide", page_title="Code Readability Feedback Tool", page_icon=":eyeglasses:")

# Add some style to the title and the description.
st.markdown("""
<style>
.big-font {
    font-size:50px !important;
    color: #5a9;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Code Readability Feedback Tool</p>', unsafe_allow_html=True)

st.markdown("""
    This tool helps you improve the readability of your code.
    Please input your code in the space below, and you'll receive instant feedback on how to make it more readable.
""")

# Text area for user to input the code
user_input_code = st.text_area('Input Code:', value='', height=300, max_chars=None, key=None)

# A button for the user to submit their code
if st.button('Get Feedback'):
    # Save user input to a .txt file
    with open('user_input_code.txt', 'w') as f:
        f.write(user_input_code)
    
    # Capture the standard output
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    # call your model function with the saved .txt file
    code_feedback('user_input_code.txt')

    # Get the printed output
    feedback = buffer.getvalue()

    # Restore standard output
    sys.stdout = old_stdout
    
    # Display the feedback
    # st.markdown(f"## Feedback:\n```{feedback}```")
    # Display the feedback
    st.write(feedback)

# Add a footer with some information or contact links
st.markdown("""
---
Made by [Adrian Alviento](https://github.com/A-Alviento) | Find the code on [GitHub](https://github.com/A-Alviento/ureca-code-readability-new/tree/main)
""")
