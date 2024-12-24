import streamlit as st
from openai import OpenAI
import random

# Initialize OpenAI client
client = OpenAI()
if 'used_sentence' not in st.session_state:
    st.session_state.used_sentence = []

def generate_fill_in_the_blank():
    # Generate fill-in-the-blank exercise
    used_sentence_str = ", ".join(st.session_state.used_sentence)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Sanskrit teacher."},
            {
                "role": "user",
                "content": f"""Generate one beginner-level fill-in-the-blank Sanskrit exercise. The exercise should not be any of the following sentences: [{used_sentence_str}].
                Do not provide the English translation at all.                
                Use this structure and replace the [Verb] or [Object] with a blank: 
                Sentence: [Subject] + [Verb] + [Object]
                Answer choices: 
                1. [Option 1] 
                2. [Option 2] 
                3. [Option 3] 
                Correct answer: [Correct option]
                """
            }
        ],
        temperature=1.2
    )
    response = completion.choices[0].message.content

    completion_1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a Sanskrit teacher. Format your responses in two parts:
                1. The exercise for the user (between <EXERCISE> tags)
                2. The correct answer (between <ANSWER> tags)
               
                Keep the format consistent and clean."""
            },
            {
                "role": "user",
                "content": f"""Use this Sanskrit fill in the blank exercise: {response}

                Use the following template to format the given fill in the blank exercise:

                <EXERCISE>
                Instructions: Identify which option best completes this sentence:

                Sanskrit Sentence: [Sentence with ___ for blank]

                Options: 
                # 1. [Option 1]
                # 2. [Option 2]
                # 3. [Option 3]

                </EXERCISE>

                <ANSWER>
                [Correct Option Number]
                </ANSWER>"""
            }
        ],
        temperature=0.7
    )
    response_1 = completion_1.choices[0].message.content


    # Parse the exercise and answer
    exercise = response_1.split("<EXERCISE>")[1].split("</EXERCISE>")[0].strip()
    st.session_state.used_sentence.append(exercise)
    correct_answer = response_1.split("<ANSWER>")[1].split("</ANSWER>")[0].strip()
    print(correct_answer)
    return exercise, correct_answer
    


# Streamlit UI
st.title("Sanskrit Fill-in-the-Blank Exercise")

# Initialize session state variables
if "exercise" not in st.session_state:
    st.session_state.exercise, st.session_state.correct_answer = generate_fill_in_the_blank()
    st.session_state.user_choice = None
    st.session_state.feedback = ""

# Display the exercise
st.markdown(st.session_state.exercise)

# Create radio buttons for user to select an answer
options = ["1", "2", "3"]
st.session_state.user_choice = st.radio(
    "Choose the correct answer:",
    options,
    index=0 if st.session_state.user_choice is None else options.index(st.session_state.user_choice),
    key="user_choice_radio"
)

# Show feedback if the user confirms their choice
if st.button("Submit Answer"):
    if st.session_state.user_choice == st.session_state.correct_answer:
        st.session_state.feedback = "Correct! Well done."
    else:
        st.session_state.feedback = f"Incorrect. The correct answer is {st.session_state.correct_answer}."
    st.markdown(f"**{st.session_state.feedback}**")

# Button to generate a new question
if st.button("Next Question"):
    st.session_state.exercise, st.session_state.correct_answer = generate_fill_in_the_blank()
    st.session_state.user_choice = None
    st.session_state.feedback = ""
    st.rerun()
