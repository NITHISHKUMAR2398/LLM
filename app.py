import streamlit as st
import pandas as pd
import requests
import json
from config import Config

class GenerateMCQs:
    def __init__(self):
        self.url_generate = Config.URL_GENERATE

    def generate_mcqs(self, df):
        # Convert dataframe to HTML format for better representation in the prompt
        #df_html = df.to_html(index=False)

        prompt = f"""
        Given the dataframe df, thoroughly analyze the data to create five meticulously crafted multiple-choice questions (MCQ), each with four options, out of which only one is the correct answer.
        Exclude columns deemed least important from consideration and focus solely on the important columns for MCQ generation.
        Utilize the provided MCQ format for structuring the output as shown below:
        
        Question 1:<br>
        Which country has the highest hourly wage? <br>
        A) India  <br>
        B) Denmark<br>
        C) Switzerland<br>
        D) None of the above<br>
        Answer : Switzerland (Switzerland holds the highest hourly wage in this dataset, standing at 17.50.)<br>
        
        Question 2:<br>
        What is the capital of India? <br>
        A) Mumbai<br>
        B) New Delhi<br>
        C) Bangalore<br>
        D) Kolkata<br>
        Answer: B) New Delhi (New Delhi is the capital of India.)<br>
        
        {df}
        """
        
        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.url_generate, json=data)
            response.raise_for_status()  # Check for HTTP errors
            return json.loads(response.text)['response']
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"

# Initialize object
generate_mcqs_obj = GenerateMCQs()

st.title("MCQ Generation from Dataset")

# Load CSV file for data analysis
csv_file_path = Config.CSV_FILE_PATH
df = pd.read_csv(csv_file_path)
st.dataframe(df.head())

# Button to analyze table data
if st.button("Generate MCQs"):
    mcqs_generation = generate_mcqs_obj.generate_mcqs(df)
    st.markdown(mcqs_generation, unsafe_allow_html=True)
