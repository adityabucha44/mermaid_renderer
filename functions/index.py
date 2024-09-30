# index.py (Flask/FastAPI)
from flask import Flask, jsonify, request
import subprocess, os

app = Flask(__name__)


@app.route("/")
def home():
    return """<!DOCTYPE html>
<html>
    <head></head>
    <body>
        <div>
          <h1>mermaid</h1>
          <p>welcome</p>
      </div>
    </body>
</html>"""


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    input_file = data['input_file']
    output_dir = data.get('output_dir', './output')
    output_file = data.get('output_file', 'output.svg')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, output_file)

    try:
        command = ["mmdc", "-i", input_file, "-o", output_file]
        subprocess.run(command, check=True)
        return jsonify({'status': 'success', 'output_file': output_file})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'failure', 'error': str(e)}), 500

# Required Netlify handler for Python function
def handler(event, context):
    return app(event, context)
