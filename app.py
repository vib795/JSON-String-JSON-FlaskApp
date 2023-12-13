from flask import Flask, render_template, request, jsonify
import json
import logging
from werkzeug.exceptions import HTTPException
import ast

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_json():
    input_string = request.form['json_input']
    try:
        # Decode the string as a raw string literal
        input_string = input_string.encode().decode('unicode_escape')

        # Strip leading and trailing double quotes if they are extra
        if input_string.startswith('"') and input_string.endswith('"'):
            input_string = input_string[1:-1]

        # Convert string to JSON
        json_object = json.loads(input_string)

        # Format JSON for display
        formatted_json = json.dumps(json_object, indent=4, sort_keys=True)
        return jsonify(success=True, json_output=formatted_json)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f"Error processing: {e}")
        return jsonify(success=False, error="Invalid format")

@app.route('/reverse-convert', methods=['POST'])
def reverse_convert_json():
    input_json = request.form['json_input']
    try:
        # Convert the input string to a JSON object to ensure it's valid JSON
        json_object = json.loads(input_json)

        # Convert the JSON object back to a string with special escaping
        json_string = json.dumps(json_object)
        escaped_json_string = json_string.replace('"', '\\"')

        # Wrap the escaped string in additional quotes
        final_string = f'"{escaped_json_string}"'

        return jsonify(success=True, json_output=final_string)
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Error processing: {e}")
        return jsonify(success=False, error="Invalid format")


@app.errorhandler(Exception)
def handle_exception(e):
    # Handle generic exceptions
    logger.error(f"An error occurred: {e}")
    if isinstance(e, HTTPException):
        return jsonify(error=e.description), e.code
    else:
        return jsonify(error="An internal error occurred"), 500

if __name__ == '__main__':
    app.run(debug=True)
