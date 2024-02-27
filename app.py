import main as text
from flask import Flask, jsonify
import requests
import pandas as pd
import os
import json
from config import Config

app = Flask(__name__)

class ExtractTasks:
    def __init__(self):
        self.url_generate = Config.URL_GENERATE

    def extract_tasks(self):
        convo = text.processed_text

        data = {
            "model": "mistral",  # The model name (presumably for generating responses)
            "stream": False,  # Indicates whether to stream the response (set to False)
            "prompt": f"Extract action tasks from the given conversation and add html break tags for each task:\n\
                        Based on the conversation, here are the action tasks that can be extracted:\n\
                        please use the below tasks as an example for formatting the output and provide it in similar way:<br>\n\
                        1: Call Dr.Karthikeyan about the chart to be discussed.\n\
                        2: Check for documentaries on oral health in Netflix.\n\
                        3: Look for Oceania region in addition to Asian countries for further research.\n\
                        4: Prepare things by next Tuesday.\n\
                        {convo}"

                            
        }

        response = requests.post(self.url_generate, json=data)
        
        if response.status_code == 200:
            print(json.loads(response.text)['response'])
            return json.loads(response.text)['response']
        else:
            # Return an error message if the request failed
            return jsonify({"error": f"Request failed with status code {response.status_code}"})
        
    
class TableToText:
    def __init__(self):
        self.url_table_to_text = Config.URL_GENERATE

    def table_to_text(self):
        excel_file_path = Config.EXCEL_FILE_PATH
        df = pd.read_csv(excel_file_path)
        # table_data_str = df.to_string(index=False, header=True)

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
            return jsonify({"error": f"Request failed with status code {response.status_code}"})

class GenerateMCQs:
    def __init__(self):
        self.url_generate = Config.URL_GENERATE

    def generate_mcqs(self):
        excel_file_path = Config.EXCEL_FILE_PATH
        df = pd.read_csv(excel_file_path)
        #table_data_str = df.to_string(index=False)

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
            print(json.loads(response.text)['response'])
            
            
            return json.loads(response.text)['response']
        else:
            return jsonify({"error": f"Request failed with status code {response.status_code}"})

extract_tasks_obj = ExtractTasks()
table_to_text_obj = TableToText()
generate_mcqs_obj = GenerateMCQs()

@app.route('/extract_tasks', methods=['GET'])
def extract_tasks():
    return extract_tasks_obj.extract_tasks()

@app.route('/table_to_text', methods=['GET'])
def table_to_text():
    return table_to_text_obj.table_to_text()

@app.route('/generate_mcqs', methods=['GET'])
def generate_mcqs():
    return generate_mcqs_obj.generate_mcqs()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
