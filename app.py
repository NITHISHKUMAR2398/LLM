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
            "prompt": f"Extract action tasks from the conversation\n{convo}",
            "stream": False
        }
        response = requests.post(self.url_generate, json=data)

        if response.status_code == 200:
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

        prompt = f"Provide a detailed description of the data in the table in 30 lines\n{table_data_str}"

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

        prompt = f"Generate a simple Multiple choice question with  4 options and 1 correct option by analyzing the table data in this below format: (question)\n\
            1) Option-1\n\
            2) Option 2\n\
            3) Option-3\n\
            4) Option-4 :\n{table_data_str}"

        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.url_generate, json=data)

        if response.status_code == 200:
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
