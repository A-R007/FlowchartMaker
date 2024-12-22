from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import groq as Groq
import re
import logging

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq client
groq_client = Groq.Client(api_key=GROQ_API_KEY)

# Extract DOT definition
def extract_dot_definition(groq_response):
    """Extract DOT definition using regex."""
    pattern = r"(digraph\s+\w+\s*{.*?})"
    match = re.search(pattern, groq_response, re.DOTALL)
    if match:
        return match.group(1)
    return None

# Validate DOT definition
def validate_dot_definition(dot_definition):
    """Validate that the DOT definition follows the basic syntax."""
    return dot_definition.strip().startswith("digraph")

# Generalized Groq Prompt
def generate_flowchart(description):
    prompt = (
        f"Create a flowchart in Graphviz DOT language for the following process: {description}. "
        "The flowchart should be structured, clear, and visually distinct. "
        "Use colors and labels to differentiate between start/end, processes, and decisions."
    )
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        raw_response = response.choices[0].message.content.strip()
        logging.debug(f"Groq API raw response: {raw_response}")
        dot_definition = extract_dot_definition(raw_response)
        if dot_definition and validate_dot_definition(dot_definition):
            return dot_definition
        logging.error(f"Invalid DOT definition extracted: {raw_response}")
        return None
    except Exception as e:
        logging.error(f"Groq API Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_flowchart', methods=['POST'])
def generate():
    try:
        data = request.json
        description = data.get('description', '')

        if not description:
            return jsonify({"error": "No description provided"}), 400

        dot_definition = generate_flowchart(description)
        if not dot_definition:
            return jsonify({"error": "Failed to generate flowchart"}), 500

        return jsonify({"dot_definition": dot_definition})
    except Exception as e:
        logging.error(f"Error in /generate_flowchart endpoint: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
