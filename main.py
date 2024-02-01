from flask import Flask, jsonify
import requests
import app as text

url = "http://localhost:11434/api/generate"



app = Flask(__name__)
# Create a Flask application route to handle the request
@app.route('/extract_tasks', methods=['GET'])
def extract_tasks():
    # Convert tasks to JSON
    convo=text.processed_text
# Specify the payload data as a dictionary
    data = {
    "model": "mistral",
    "prompt": f"Extract tasks from the conversation\n{convo}",
    "stream":False
}

# Convert the data to JSON format
    json_data = {
    "json": data
}

# Make the POST request
    response = requests.post(url, **json_data)
    json_tasks = jsonify(response.text)
    return json_tasks

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)

