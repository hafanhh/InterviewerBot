# Create Interview ChatBot for Data Analyst/Data Scientist
import streamlit as st
import openai 
import os
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import random
from io import BytesIO
import numpy as np

api_key = os.getenv("openai_api_2nd_key"
client = openai.OpenAI(api_key=api_key)

# Selections fro each criterion
roles = ['Data Analyst', 'Data Scientist', 'Machine Learning']
levels = ['Beginner', 'Intermediate', 'Advanced']
topics = ['Python', 'SQL', 'Excel', 'Maths']
chart_option = 'Chart Description'

# Interface of Streamlit
st.title("🤖 Technical Interview Bot for Data Analyst / Data Scientist")

# Creating selection buttons
selected_role = st.selectbox("📌 Select the role:", roles)
selected_level = st.selectbox("📌 Select the level:", levels)
selected_topic = st.selectbox("📌 Select the aspect:", topics + [chart_option])

# Call OpenAI to generate interview question function
def generate_interview_question(role, level, topic):
    if topic == chart_option:
        prompt = f"As a professional interviewer, generate a random chart and ask the candidate to describe it. The difficulty level is {level}."
    else:
        prompt = "As a professional interviewer, give interview a technical interview at {level} level for {role} about {topic}"
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages = [{'role':'system', 'content':prompt}]
        )
    return response.choices[0].message.content

# Function to create charts randomly
def generate_random_chart():
    chart_types = ['bar', 'line', 'pie', 'scatter']
    chart_type = random.choice(chart_types) #Select the chart randomly
    
    plt.figure(figsize=(6,4)) #size of chart
    
    if chart_type == 'bar':
        categories = ['A', 'B', 'C', 'D']
        values = np.random.randint(10, 100, size = 4)
        plt.bar(categories, values, color = 'skyblue')
        plt.title('Sale Data for Categories')
    
    elif chart_type == 'line':
        x = np.arange(1, 11)
        y = np.random.randint(10, 100, size = 10)
        plt.plot(x, y, marker = 'o', linestyle = '-', color='red')
        plt.title('Revenue over 10 months')
        plt.xlabel('Month')
        plt.ylabel('Revenue ($1000s)')
    
    elif chart_type == 'pie':
        labels = ['Product A', 'Product B', 'Product C']
        sizes = np.random.randint(10, 50, size=3)
        plt.pie(sizes, labels = labels, autopct = "%1.1f%%", colors = ['blue', 'orange', 'green'])
        plt.title('Market Share Distribution')
        
    elif chart_type =='scatter':
        x = np.random.randint(10, 100, size = 20)
        y = np.random.randint(10, 100, size = 20)
        plt.scatter(x, y, color = 'purple')
        plt.title('Customer Satisfaction vs. Revenue')
        plt.xlabel('Satisfaction Score')
        plt.ylabel('Revenue ($1000s)')
    
    # Save chart in memory buffer
    buf = BytesIO()
    plt.savefig(buf, format = 'png')
    buf.seek(0)
    plt.close()
    return buf, chart_type 

# Function to evaluate the answer:
def evaluate_answer(question, answer):
    prompt = (
        f'**Interview Question:** {question}\n\n'
        f'**Answer:** {answer}\n\n'
        'Evaluate the response on a scale of 100 based on accuracy depth, and clarity. '
        'Provide feedback on strengths, weaknesses, and suggestions for improvement. '
        'If the answer is incorrent, explain the correct approach.'
    )
    response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages = [{'role':'system', 'content':prompt}]
    )
    return response.choices[0].message['content']

# Function to generate a hint for answer
def generate_hint(question):
    prompt = f'Provide a brief hint to guide the interviewee in answering this interview question: {question}'
    response = client.chat.completions.create(
        model ='gpt-3.5-turbo',
        messages = [{'role' : 'system', 'content':prompt}]
    )
    return response.choices[0].message['content']

# Function to generate the correct solution
def generate_solution(question):
    prompt = f'Provide a model answer with explaination for this interview question: {question}'
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role':'system', 'content':prompt}]
    )
    return response.choices[0].message['content']

# Interface on Streamlit for "importing interview question" button
if st.button("🔔 Import Interview Questions"):
    question = generate_interview_question(selected_role, selected_level, selected_topic)
    st.session_state['question'] = question #save interview question in session
    st.write(f"**Question ({selected_role} - {selected_level} - {selected_topic}):**")
    st.write(question)

# Create Random Chart Button for chart description
if selected_topic == chart_option:
    if st.button('📊 Generate Random Chart for Description Practice'):
        chart_buf, chart_type = generate_random_chart()
        st.image(chart_buf, caption = f'Describe this {chart_type} chart.')


# Box for inserting answers
if 'question' in st.session_state:
    answer = st.text_area('🔆 Insert your answer:')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button('💡 Get Hint'):
            hint = generate_hint(st.session_state['question'])
            st.write('### 🔹 Hint:')
            st.write(hint)
    
    with col2:
        if st.button('📜 Show Solution'):
            solution = generate_solution(st.session_state['question'])
            st.write('🏆 Model Answer:')
            st.write(solution)
    
    with col3:
        if st.button('✅ Evaluate Answer'):
            if answer.strip():
                feedback = evaluate_answer(st.session_state['question'], answer)
                st.write('🎯 Evaluation Result')
                st.write(feedback)
            else:
                st.warning('⚠️ Please provide an answer before evaluating.')