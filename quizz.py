import streamlit as st

# Set page config for embedding
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# Quiz data
quizzes = {
    "Geography": [
        {
            "question": "What is the capital of France?",
            "choices": ["London", "Berlin", "Paris", "Madrid"],
            "correct_answer": "Paris",
            "explanation": "Paris is the capital and most populous city of France."
        },
        {
            "question": "Which is the largest ocean on Earth?",
            "choices": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
            "correct_answer": "Pacific Ocean",
            "explanation": "The Pacific Ocean is the largest and deepest of Earth's oceanic divisions."
        }
    ],
    "History": [
        {
            "question": "In which year did World War II end?",
            "choices": ["1943", "1945", "1947", "1950"],
            "correct_answer": "1945",
            "explanation": "World War II ended in 1945 with the surrender of Germany in May and Japan in August."
        },
        {
            "question": "Who was the first President of the United States?",
            "choices": ["Thomas Jefferson", "John Adams", "George Washington", "Benjamin Franklin"],
            "correct_answer": "George Washington",
            "explanation": "George Washington was the first President of the United States, serving from 1789 to 1797."
        }
    ],
    "Science": [
        {
            "question": "What is the chemical symbol for gold?",
            "choices": ["Go", "Gd", "Au", "Ag"],
            "correct_answer": "Au",
            "explanation": "The chemical symbol for gold is Au, derived from the Latin word 'aurum'."
        },
        {
            "question": "What is the largest planet in our solar system?",
            "choices": ["Earth", "Mars", "Jupiter", "Saturn"],
            "correct_answer": "Jupiter",
            "explanation": "Jupiter is the largest planet in our solar system, with a mass more than two and a half times that of all the other planets combined."
        }
    ],
    "Literature": [
        {
            "question": "Who wrote 'Romeo and Juliet'?",
            "choices": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
            "correct_answer": "William Shakespeare",
            "explanation": "'Romeo and Juliet' is a tragedy written by William Shakespeare early in his career."
        },
        {
            "question": "What is the name of the hobbit in 'The Lord of the Rings'?",
            "choices": ["Bilbo", "Frodo", "Sam", "Pippin"],
            "correct_answer": "Frodo",
            "explanation": "Frodo Baggins is the primary protagonist of 'The Lord of the Rings', written by J.R.R. Tolkien."
        }
    ]
}

def run_quiz(quiz_name):
    st.title(f"{quiz_name} Quiz")
    
    # Initialize session state for this quiz
    if f'current_question_{quiz_name}' not in st.session_state:
        st.session_state[f'current_question_{quiz_name}'] = 0
        st.session_state[f'score_{quiz_name}'] = 0
        st.session_state[f'submitted_{quiz_name}'] = False

    # Display current question
    quiz_data = quizzes[quiz_name]
    question = quiz_data[st.session_state[f'current_question_{quiz_name}']]
    st.write(f"Question {st.session_state[f'current_question_{quiz_name}'] + 1}:")
    st.write(question['question'])
    
    # Display choices and get user's answer
    user_answer = st.radio("Choose your answer:", question['choices'], key=f"q{st.session_state[f'current_question_{quiz_name}']}")
    
    # Submit button
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
    # Create a sidebar for quiz selection
    quiz_name = st.sidebar.selectbox("Choose a quiz", list(quizzes.keys()))
    run_quiz(quiz_name)

if __name__ == "__main__":
    main()
