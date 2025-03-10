import streamlit as st
import pandas as pd
import os

# Set page config for embedding
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# Define CSV filename (must be in the same directory as the script)
CSV_FILENAME = "quiz_questions.csv"

# Check if CSV exists
if not os.path.exists(CSV_FILENAME):
    st.error(f"Quiz file '{CSV_FILENAME}' not found. Please make sure it exists in the same directory as this script.")
    st.stop()

# Load CSV file
df = pd.read_csv(CSV_FILENAME)

# Validate CSV structure
required_columns = {"category", "question", "choice_1", "choice_2", "choice_3", "choice_4", "correct_answer", "explanation"}
if not required_columns.issubset(df.columns):
    st.error(f"CSV is missing required columns. Expected columns: {', '.join(required_columns)}")
    st.stop()

# Convert CSV data into structured quiz dictionary
quizzes = {}
for _, row in df.iterrows():
    category = row["category"]
    if category not in quizzes:
        quizzes[category] = []
    
    quizzes[category].append({
        "question": row["question"],
        "choices": [row["choice_1"], row["choice_2"], row["choice_3"], row["choice_4"]],
        "correct_answer": row["correct_answer"],
        "explanation": row["explanation"]
    })

def run_quiz(quiz_name):
    st.title(f"{quiz_name} Quiz")

    # Initialize session state
    if f'current_question_{quiz_name}' not in st.session_state:
        st.session_state[f'current_question_{quiz_name}'] = 0
        st.session_state[f'score_{quiz_name}'] = 0
        st.session_state[f'submitted_{quiz_name}'] = False

    quiz_data = quizzes[quiz_name]
    question = quiz_data[st.session_state[f'current_question_{quiz_name}']]
    st.write(f"Question {st.session_state[f'current_question_{quiz_name}'] + 1}:")
    st.write(question['question'])

    # Display choices
    user_answer = st.radio("Choose your answer:", question['choices'], key=f"q{st.session_state[f'current_question_{quiz_name}']}")

    if st.button("Submit", key=f"submit_{quiz_name}"):
        st.session_state[f'submitted_{quiz_name}'] = True

        if user_answer == question['correct_answer']:
            st.success("Correct!")
            st.session_state[f'score_{quiz_name}'] += 1
        else:
            st.error("Incorrect!")

        st.write(f"Correct answer: {question['correct_answer']}")
        st.write(f"Explanation: {question['explanation']}")

        # Move to next question or show final score
        if st.session_state[f'current_question_{quiz_name}'] < len(quiz_data) - 1:
            if st.button("Next Question", key=f"next_{quiz_name}"):
                st.session_state[f'current_question_{quiz_name}'] += 1
                st.session_state[f'submitted_{quiz_name}'] = False
                st.experimental_rerun()
        else:
            st.write(f"Quiz completed! Your score: {st.session_state[f'score_{quiz_name}']}/{len(quiz_data)}")
            if st.button("Restart Quiz", key=f"restart_{quiz_name}"):
                st.session_state[f'current_question_{quiz_name}'] = 0
                st.session_state[f'score_{quiz_name}'] = 0
                st.session_state[f'submitted_{quiz_name}'] = False
                st.experimental_rerun()

def main():
    quiz_name = st.sidebar.selectbox("Choose a quiz", list(quizzes.keys()))
    run_quiz(quiz_name)

main()
