import streamlit as st
# from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key="your_api_key",  # Replace with your actual API key
    base_url="https://api.aimlapi.com",
)

# Get chat response from the model
def get_chat_response(input_text, chat_history): 

    llm = "meta-llama/Llama-3-8b-chat-hf"

    # Build the messages list for the API request
    messages = [{"role": "system", "content": "You are an AI assistant who knows everything."}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": input_text})
    
    response = client.chat.completions.create(
        model=llm,
        messages=messages
    )
    
    return response.choices[0]['message']['content']

st.set_page_config(page_title="Chatbot")  # HTML title
st.title("Adv's Chatbot")  # Page title

if 'chat_history' not in st.session_state:  # See if the chat history hasn't been created yet
    st.session_state.chat_history = []  # Initialize the chat history

# Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history:  # Loop through the chat history
    with st.chat_message(message["role"]):  # Renders a chat line for the given role, containing everything in the with block
        st.markdown(message["text"])  # Display the chat content

input_text = st.chat_input("Chat with your bot here")  # Display a chat input box

if input_text:  # Run the code in this if block after the user submits a chat message
    with st.chat_message("user"):  # Display a user chat message
        st.markdown(input_text)  # Renders the user's latest message

    st.session_state.chat_history.append({"role": "user", "text": input_text})  # Append the user's latest message to the chat history

    chat_response = get_chat_response(input_text=input_text, chat_history=st.session_state.chat_history)  # Call the model through the supporting library

    with st.chat_message("assistant"):  # Display a bot chat message
        st.markdown(chat_response)  # Display bot's latest response

    st.session_state.chat_history.append({"role": "assistant", "text": chat_response})