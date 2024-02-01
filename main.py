from flask import Flask, jsonify
import requests
import pandas as pd
import app as text
import os
import pandas as pd

# Get the current script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Assuming your table data is in an Excel file named 'sample_XLSX_100.xlsx' in the same directory
excel_file_path = os.path.join(script_directory, 'sample_XLSX_100.xlsx')

# Read Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

url_generate = "http://localhost:11434/api/generate"
url_table_to_text = "http://localhost:11434/api/generate"

app = Flask(__name__)

# Route for extracting tasks¸
@app.route('/extract_tasks', methods=['GET'])
def extract_tasks():
    convo = text.processed_text
    data = {
        "model": "mistral",
        "prompt": f"Extract tasks from the conversation\n{convo}",
        "stream": False
    }
    response = requests.post(url_generate, json=data)
    
    if response.status_code == 200:
        return response.text
    else:
        return jsonify({"error": f"Request failed with status code {response.status_code}"})

# Route for table to text generation
@app.route('/table_to_text', methods=['GET'])
def table_to_text():
    # Assuming your table data is in an Excel file named 'table_data.xlsx'
    excel_file_path = '/Users/nithish/Documents/dotzza-feature/sample_XLSX_100.xlsx'
    
    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path)

    # Convert DataFrame to a formatted text
    table_data_str = df.to_string(index=False)

    # Provide a prompt for the language model
    prompt = f"describe the table in 10 lines\n{table_data_str}"

    # Use the same model "mistral" for table-to-text generation
    data = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url_table_to_text, json=data)

    if response.status_code == 200:
        return response.text
    else:
        return jsonify({"error": f"Request failed with status code {response.status_code}"})

if __name__ == '__main__':
    app.run(debug=True)
