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
            "prompt": f"Extract action tasks from the given conversation in the below format and add html break tags for each task:\n\
                        Based on the conversation, here are the action tasks that can be extracted:\n\
                        Here is an example for you: Print the output in a similar way:<br>\n\
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
        df = pd.read_excel(excel_file_path)
        table_data_str = df.to_string(index=False, header=True)

        prompt = f"Consider all the rows and columns in the table and provide me a detailed description of the sheet in paragraph.\n\
                   Based on the table data provided, here are some key points to include:\n\
                        1. Describe the overall structure of the table.\n\
                        2. Highlight any trends or patterns you observe in the data.\n\
                        3. Identify any outliers or unusual data points.\n\
                        4. Discuss any correlations between different columns.\n\
                        5. Provide insights or conclusions drawn from the data.\n\
            Here is an example below :\n\
          **Paragraph 1:**\n\
            Large Language Models (LLMs) represent a significant advancement in the field of natural language processing (NLP).\n\
            These models, such as GPT-3 developed by OpenAI, are trained on vast amounts of text data and have the capability to generate human-like text in\n\
            response to prompts or queries. LLMs employ deep learning techniques, particularly transformer architectures,\n\
            which allow them to understand and generate text with remarkable accuracy and coherence. With their\n\
            immense size and complexity, LLMs can comprehend and produce text across a wide range of topics and\n\
            writing styles. Their versatility and ability to adapt to different tasks make them invaluable tools\n\
            for various applications, including content generation, language translation, and conversational agents.\n\
          \n\
           \n\
            \n\
          **Paragraph 2:**\n\
            The development and deployment of Large Language Models (LLMs) have sparked both excitement and debate within the\n\
            scientific community and society at large. On one hand, LLMs represent a remarkable achievement in\n\
            artificial intelligence, pushing the boundaries of what machines can accomplish in understanding and\n\
            generating human language. Their potential applications in areas such as education, healthcare, and\n\
            creative writing hold promise for improving efficiency and enhancing human experiences. However,\n\
            concerns have been raised regarding the ethical implications and potential risks associated with LLMs,\n\
            including biases in the training data, misinformation propagation, and job displacement. As researchers\n\
            and policymakers grapple with these challenges, it is crucial to ensure responsible development and\n\
            deployment of LLMs to harness their benefits while mitigating potential harms.\n\
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
