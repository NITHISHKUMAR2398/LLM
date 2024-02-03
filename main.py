from flask import Flask, jsonify
import requests
import pandas as pd
import os
import app as text
import json

class ExtractTasks:
    def __init__(self):
        self.url_generate = "http://localhost:11434/api/generate"

    def extract_tasks(self):
        convo = text.processed_text
        data = {
            "model": "mistral",
            "prompt": f"Extract tasks from the conversation\n{convo}",
            "stream": False
        }
        response = requests.post(self.url_generate, json=data)

        if response.status_code == 200:
            return response.text
        else:
            return jsonify({"error": f"Request failed with status code {response.status_code}"})

class TableToText:
    def __init__(self):
        self.url_table_to_text = "http://localhost:11434/api/generate"

    def table_to_text(self):
        excel_file_path = '/Users/nithish/Documents/dotzza-feature/sample_XLSX_100.xlsx'
        df = pd.read_excel(excel_file_path)
        table_data_str = df.to_string(index=False)

        prompt = f"analyse the data in the table in few lines of information\n{table_data_str}"

        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.url_table_to_text, json=data)

        if response.status_code == 200:
            return response.text
        else:
            return jsonify({"error": f"Request failed with status code {response.status_code}"})

class GenerateMCQs:
    def __init__(self):
        self.url_generate = "http://localhost:11434/api/generate"

    def generate_mcqs(self):
        excel_file_path = '/Users/nithish/Documents/dotzza-feature/sample_XLSX_100.xlsx'
        df = pd.read_excel(excel_file_path)
        table_data_str = df.to_string(index=False)

        prompt = f"Generate 2  multiple choice questions by analysing this table data:\n{table_data_str}"

        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.url_generate, json=data)

        if response.status_code == 200:
            return json.load(response.text)['response']
        else:
            return jsonify({"error": f"Request failed with status code {response.status_code}"})

app = Flask(__name__)
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
