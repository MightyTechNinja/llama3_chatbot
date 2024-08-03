import streamlit as st
from streamlit import markdown  # Added import for markdown
import os
from huggingface_hub import InferenceClient

huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

st.set_page_config(page_title="Chatbot") 
st.title("Hola Amigos!")  


client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token=huggingface_token,
)

# Get chat response from the model
def get_chat_response(input_text):
    response_text = ""
    for message in client.chat_completion(
        messages=[
            {"role": "system", "content": "Be a good assistant and help to solve users problems"},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1024,
        stream=True,
    ):
        response_text += message.choices[0].delta.content
    
    return response_text

        


if 'chat_history' not in st.session_state:  
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

input_text = st.chat_input("Chat with your bot here")

if input_text:
    with st.chat_message("user"):
        st.markdown(input_text) 

    st.session_state.chat_history.append({"role": "user", "text": input_text})

    chat_response = get_chat_response(input_text=input_text)

    with st.chat_message("assistant"):
            st.markdown(chat_response)
            
    st.session_state.chat_history.append({"role": "assistant", "text": chat_response})        