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
            "model": "mistral",
             "stream": False,
             "prompt": f"Extract action tasks from the given conversation in the below format and add html break tags for each task:\n\
                Based on the conversation, here are the action tasks that can be extracted,\n\
                Here is an example for you: Print the output in a similar way\n\
                    1. Call Dr. Karthikeyan about the chart to be discussed.\n\
                    2. Check for documentaries on oral health in Netflix.\n\
                    3. Look for Oceania region in addition to Asian countries for further research.\n\
                    4. Prepare things by next Tuesday.\n\
                {convo}"
}

        response = requests.post(self.url_generate, json=data)

        if response.status_code == 200:
            print(json.loads(response.text)['response'])
            return json.loads(response.text)['response']
        else:
            return jsonify({"error": f"Request failed with status code {response.status_code}"})

class TableToText:
    def __init__(self):
        self.url_table_to_text = Config.URL_GENERATE

    def table_to_text(self):
        excel_file_path = Config.EXCEL_FILE_PATH
        df = pd.read_excel(excel_file_path)
        table_data_str = df.to_string(index=False, header=True)

        prompt = f"Consider all the rows and columns in the table and provide me a detailed description of the sheet in two separate paragraphs.\n\
                              Based on the table data provided, here are some key points to include:\n\
                              1. Describe the overall structure of the table.\n\
                              2. Highlight any trends or patterns you observe in the data.\n\
                              3. Identify any outliers or unusual data points.\n\
                              4. Discuss any correlations between different columns.\n\
                              5. Provide insights or conclusions drawn from the data.\n\
                              {table_data_str}"


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
        df = pd.read_excel(excel_file_path)
        table_data_str = df.to_string(index=False)

        prompt = f"Generate 5 random Multiple choice question with 4 options and display it out of which 1 is the correct option with reason by analyzing the  data in the below format: \n\
            and add html break tags for each question and answer. Here is an example for you.\n\
            Question 1:<br>\n\
            Which country has the highest hourly wage? <br>\n\
            A) Czech Republic <br>\n\
            B) Denmark<br>\n\
            C) Switzerland<br>\n\
            D) Hungary<br>\n\
               answer : Switzerland (The new hourly wage for the Switzerland is the highest in this data set.)<br>\n\
                {table_data_str}"
            
            

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
