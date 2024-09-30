from flask import Flask, request, jsonify
import subprocess, os

app = Flask(__name__)

def run_mmdc(input_file: str, output_dir: str, output_file: str):
    """
    Executes the 'mmdc' command to generate an output SVG file from the input file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, output_file)

    # Define the command
    command = ["mmdc", "-i", input_file, "-o", output_file]

    # Run the command
    try:
        subprocess.run(command, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        return str(e)

@app.route('/generate', methods=['POST'])
def generate_svg():
    data = request.json
    input_file = data.get('input_file')
    output_dir = data.get('output_dir', './output')
    output_file = data.get('output_file', 'output.svg')

    if not input_file:
        return jsonify({"error": "Input file is required"}), 400

    result = run_mmdc(input_file, output_dir, output_file)
    if "Error" in result:
        return jsonify({"error": result}), 500

    return jsonify({"message": "SVG generated successfully", "output_file": result}), 200

if __name__ == '__main__':
    app.run(debug=True)
