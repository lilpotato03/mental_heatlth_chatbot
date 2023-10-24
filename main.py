import os
from os import path
import streamlit as st
from langchain.llms import OpenAI
import json
import random
from difflib import get_close_matches
# Load knowledge base
count=0
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Save knowledge base
def save_knowledge_base(file_path,data):
    with open(file_path) as fp:
        json_text=[]
        json_text=json.load(fp)
        json_text.append(data)
    with open(file_path, 'w') as file:
        json.dump(json_text, file, indent=2,separators=(',',': '))

# Find best match using get_close_matches
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.5)
    return matches[0] if matches else None

# Get answer for a question
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base:
        if q["question"]== question:
            return q["answer"]

# Chat bot logic
def chat_bot(prompt, knowledge_base):
    global count
    count+=1
    if prompt.lower() == 'quit':
        exit()
    
    best_match = find_best_match(prompt, [q["question"] for q in knowledge_base])
    
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        st.write(f'Bot: {random.choice(answer)}')
    else:
        #return f"Bot: I don't know the answer. Can you teach me?"
        st.write("Bot: I don't know the answer. Can you teach me?")
        count+=1
        response_prompt=st.text_input('You:',key=count)
        if response_prompt:
            dict={"question":f" {prompt}",
                "answer":[f"{response_prompt}"]
                }
            save_knowledge_base('knowledge_base.json',dict)
            st.write("Bot: thank you for teaching me.Please type next and enter.")
            if dict:
                return True
def input_generator():
    global count
    count+=1
    prompt = st.text_input('You:',key=count)
    if prompt:
        return prompt
def func_loop():
        prompt=input_generator()
        if prompt:
            res=chat_bot(prompt, knowledge_base)
            if res:
                func_loop()
# Streamlit interface
st.title('🧠 TheraBot')
# Load knowledge base
knowledge_base = load_knowledge_base('knowledge_base.json')
# User input
func_loop()
# prompt loop


