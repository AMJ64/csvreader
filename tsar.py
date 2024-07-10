import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from groq import Groq
import re

# Initialize Groq client
api_key = "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"
client = Groq(api_key=api_key)

# Streamlit interface
st.title("TINKU CHAT WALA")

# CSV file upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    st.write("CSV Data:")
    st.write(data)

    # Convert the DataFrame to a JSON format to pass as context
    data_context = data.to_json()

    # Chatbox for user prompts
    user_prompt = st.text_input("Enter your prompt to chat with the CSV data")

    if st.button("Submit"):
        if user_prompt:
            # Define the context and user prompt
            context = f"The data from the CSV file is: {data_context}"

            try:
                # Create chat completion request
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant."
                        },
                        {
                            "role": "user",
                            "content": context
                        },
                        {
                            "role": "user",
                            "content": f"{user_prompt}. Please provide only the Python code snippet without any explanations. Use the DataFrame 'data' directly."
                        }
                    ],
                    model="llama3-70b-8192",
                )

                # Get the response from the LLM
                response = chat_completion.choices[0].message.content
                st.write("Response from LLM:")
                st.write(response)

                # Filter out non-code parts (simple example, adjust as needed)
                code_snippet = re.findall(r'```python(.*?)```', response, re.DOTALL)
                if code_snippet:
                    code_to_execute = code_snippet[0].strip()
                else:
                    code_to_execute = response.strip()

                # Remove any remaining backticks
                code_to_execute = code_to_execute.replace('```', '').strip()

                # st.write("Code to execute:")
                # st.write(code_to_execute)

                # Execute the generated code to display the graph
                try:
                    exec(code_to_execute)
                    # Ensure the figure is displayed using Streamlit
                    st.pyplot(plt.gcf())
                except Exception as e:
                    st.write("Error executing the generated code:")
                    st.write(e)
            except Exception as e:
                st.write("Error during chat completion request:")
                st.write(e)
        else:
            st.write("Please enter a prompt.")