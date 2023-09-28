import streamlit as st
from simpleai.search import CspProblem, backtrack

# Set page title and background color
st.set_page_config(
    page_title="Salih Ekici's Cryptoarithmetic puzzle solver",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Salih Ekici's Cryptoarithmetic puzzle solver")

# Create a sidebar for input fields
st.sidebar.header("Input Fields")

# Input fields
first_word = st.sidebar.text_input("Enter first word of the puzzle:")
second_word = st.sidebar.text_input("Enter second word of the puzzle:")
result_word = st.sidebar.text_input("Enter solution word:")
operator = st.sidebar.selectbox("Choose the operation:", ("+", "*"))

variables = set()
first_letters = []
domains = {}
inputs = [first_word, second_word, result_word]

if st.sidebar.button("Solve"):
    # Go over the list of inputs, add the first letters of each word to the first_letter list and update the variable set with the letters.
    for word in inputs:
        first_letters.append(word[0])
        variables.update(word)

    # Update the domain with the key-value pairs. Start the list from 0 or 1 based on the first letters list.
    # First letters will start from 1 since they cannot be 0 in the calculations
    for letter in variables:
        if letter in first_letters:
            domains.update({letter: list(range(1, 10))})
        else:
            domains.update({letter: list(range(0, 10))})

    # Give the letters unique values.
    def constraint_unique(variables, values):
        return len(values) == len(set(values))

    def constraint_arithmetic(variables, values):
        first_word, second_word, result_word = [word for word in inputs]
        # Create a dictionary to map letters to their assigned values
        assignment = {var: val for var, val in zip(variables, values)}

        # Convert the words to their corresponding numbers using the assignment
        first_number = int("".join(str(assignment[var]) for var in first_word))
        second_number = int("".join(str(assignment[var]) for var in second_word))
        result_number = int("".join(str(assignment[var]) for var in result_word))

        if operator == "+":
            return first_number + second_number == result_number
        if operator == "*":
            return first_number * second_number == result_number

    constraints = [
        (tuple(variables), constraint_unique),
        (tuple(variables), constraint_arithmetic),
    ]

    def solve_puzzle():
        # Your existing code to solve the puzzle
        problem = CspProblem(variables, domains, constraints)
        output = backtrack(problem)
        return output

    output = solve_puzzle()

    first_number = int("".join(str(output[var]) for var in first_word))
    second_number = int("".join(str(output[var]) for var in second_word))
    result_number = int("".join(str(output[var]) for var in result_word))

    # Display the solutions
    st.header("Solutions:")
    if not output:
        st.write("No solution found.")
    else:
        st.write(f"{first_word} \{operator} {second_word} = {result_word}")
        st.write(f"{first_number} \{operator} {second_number} = {result_number}")
