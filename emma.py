import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os


load_dotenv()


st.title('🧠 MindMentor')
st.write("""
Welcome to *MindMentor*, a tool designed by EMMANUEL ADULOJU to help assess mental health wellbeing through insightful questions. 
Please proceed by generating the questions and providing your honest answers.
""")


def llm_output(prompt):
    MODEL = 'gpt-4'
    key = os.getenv('OPENAI_API_KEY')
    parser = StrOutputParser()
    model = ChatOpenAI(model=MODEL, api_key=key)
    llm_output = model | parser
    return llm_output.invoke(prompt)


def questions_generator():
    prompt = 'Generate ten questions you will ask a high school student to gauge their mental health wellbeing on a scale of one to ten. Return only the questions.'
    response = llm_output(prompt)
    return response.split('?')


def feeling_rater(answers):
    formatted_answers = '\n'.join([f'Question: {q}\nAnswer: {a}' for q, a in answers])
    prompt = f'Rate how this student feels on a scale of one to ten based on how they have answered these questions. Here are the questions and answers:\n{formatted_answers}\nYour response must be in markdown format.'
    response = llm_output(prompt)
    return response


if 'questions' not in st.session_state:
    st.session_state.questions = []

st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-size: 16px;
}

.stTextInput>div>input {
    font-size: 14px;
}

.stMarkdown h1 {
    color: #4CAF50;
    font-family: 'Arial';
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


if st.button('Generate Questions 📝'):
    st.session_state.questions = questions_generator()


if st.session_state.questions:
    st.write("Please answer the following questions:")
    
    with st.form("questions_form"):
        answers = []
        for i, question in enumerate(st.session_state.questions):
            if question.strip():
                answer = st.text_input(f"Q{i+1}: {question.strip()}?", key=f"answer_{i}")
                answers.append((question.strip(), answer))
        
        # Form submit button
        submitted = st.form_submit_button("Submit and Get Rating ✅")
        
        if submitted:
            completed_answers = [(q, a) for q, a in answers if a.strip()]
            
            if completed_answers:
                rating = feeling_rater(completed_answers)
                st.markdown(rating)
            else:
                st.warning("Please answer all questions before submitting.")

# Button to clear the session and reset the app
if st.button("Rerun 🔄"):
    st.session_state.questions = []
    st.query_params.clear()