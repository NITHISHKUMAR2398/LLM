import streamlit as st
import requests
import pandas as pd
import json
from config import Config

class ExtractTasks:
    def __init__(self):
        self.url_generate = Config.URL_GENERATE

    def extract_tasks(self, convo):
        data = {
            "model": "mistral",
            "stream": False,
            "prompt": f"Extract action tasks from the given conversation and add html break tags for each task:\n\
                        Based on the conversation, here are the action tasks that can be extracted:\n\
                        please use the below tasks as an example for formatting the output and provide it in similar way:<br>\n\
                        1: Call Dr.Karthikeyan about the chart to be discussed.<br>\n\
                        2: Check for documentaries on oral health in Netflix.<br>\n\
                        3: Look for Oceania region in addition to Asian countries for further research.<br>\n\
                        4: Prepare things by next Tuesday.<br>\n\
                        {convo}"
        }

        response = requests.post(self.url_generate, json=data)
        
        if response.status_code == 200:
            return json.loads(response.text)['response']
        else:
            return f"Request failed with status code {response.status_code}"

class TableToText:
    def __init__(self):
        self.url_table_to_text = Config.URL_GENERATE

    def table_to_text(self, df):
        prompt =  f"Given the dataframe df, conduct a thorough analysis of the data to provide a detailed description of the dataset within a 300-word limit.\n\
                   Key points to include based on the table data:\n\
                   1. Offer a comprehensive overview of the table's structure, including the number of rows and columns, data types, and any missing values.\n\
                   2. Analyze trends or patterns within the data, such as temporal trends, spatial patterns, or recurring patterns in categorical variables.\n\
                   3. Identify and discuss any outliers or unusual data points that deviate significantly from the norm, considering their potential impact on the analysis.\n\
                   4. Explore potential correlations between different columns and their implications for understanding the relationships between variables.\n\
                   5. Evaluate the quality and integrity of the data, addressing any data quality issues and potential biases.\n\
                   6. Offer insightful conclusions drawn from the data analysis, highlighting key findings and their implications for decision-making.\n\
                   7. Provide recommendations for further exploration or research based on the analysis, suggesting potential avenues for enhancing understanding or addressing unanswered questions.\n\
                      \n\{df}"    

        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.url_table_to_text, json=data)

        if response.status_code == 200:
            return json.loads(response.text)['response']
        else:
            return f"Request failed with status code {response.status_code}"

class GenerateMCQs:
    def __init__(self):
        self.url_generate = Config.URL_GENERATE

    def generate_mcqs(self, df):
        prompt = f"Given the dataframe df, thoroughly analyze the data to create five meticulously crafted multiple-choice questions (MCQ), each with four options, out of which only one is the correct answer.\n\
                    Exclude columns deemed least important from consideration and focus solely on the essential columns for MCQ generation..\n\
                    Utilize the provided MCQ format for structuring the output as shown below:\n\
                    Question 1:<br>\n\
                    Which country has the highest hourly wage? <br>\n\
                    A) India  <br>\n\
                    B) Denmark<br>\n\
                    C) Switzerland<br>\n\
                    D) None of the above<br>\n\
                    Answer : Switzerland (Switzerland holds the highest hourly wage in this dataset, standing at 17.50.)<br>\n\
                    Question 2:<br>\n\
                    What is the capital of India? <br>\n\
                    A) Mumbai<br>\n\
                    B) New Delhi<br>\n\
                    C) Bangalore<br>\n\
                    D) Kolkata<br>\n\
                    Answer: B) New Delhi (New Delhi is the capital of India.)<br>\n\
                    {df}"
        
        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.url_generate, json=data)

        if response.status_code == 200:
            return json.loads(response.text)['response']
        else:
            return f"Request failed with status code {response.status_code}"

# Initialize objects
extract_tasks_obj = ExtractTasks()
table_to_text_obj = TableToText()
generate_mcqs_obj = GenerateMCQs()

st.title("Data Analysis Toolkit")

# Sample conversation for action task extraction
sample_conversation = st.text_area("Enter conversation for action task extraction:", "")

# Button to extract action tasks
if st.button("Extract Action Tasks"):
    if sample_conversation:
        action_tasks = extract_tasks_obj.extract_tasks(sample_conversation)
        st.markdown(action_tasks, unsafe_allow_html=True)
    else:
        st.error("Please enter a conversation.")

# Load Excel file for data analysis
excel_file_path = Config.EXCEL_FILE_PATH
df = pd.read_csv(excel_file_path)
st.dataframe(df.head())

# Button to analyze table data
if st.button("Generate MCQ's"):
    #text_analysis = table_to_text_obj.table_to_text(df)
    #st.markdown(text_analysis, unsafe_allow_html=True)

    mcqs_generation = generate_mcqs_obj.generate_mcqs(df)
    st.markdown(mcqs_generation, unsafe_allow_html=True)
