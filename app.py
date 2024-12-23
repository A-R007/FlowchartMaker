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
        f"Create a detailed and visually distinct flowchart in Graphviz DOT language that represents the following process: {description}. "
        "The flowchart should be well-structured and clearly defined, with each step represented as a node. "
        "Use the following color scheme and formatting guidelines to ensure clarity and visual appeal: \n\n"
        "- **Start and End Nodes**: Use a soft, light **blue** color to signify the beginning and the end of the process. Make the nodes round to indicate their special significance.\n"
        "- **Process Nodes**: Use a **green** color for process steps, representing actions or tasks that move the process forward. These should be rectangular with slightly rounded corners.\n"
        "- **Decision Nodes**: Use a **red** color for decision points, where the flow branches based on conditions. These nodes should be diamond-shaped to visually indicate a decision.\n"
        "- **Connecting Edges**: Use a **blue** color for edges to represent the flow between the nodes. The edges should have arrows pointing in the direction of the flow to maintain a logical sequence.\n"
        "- **Node Labels**: Ensure that each node is labeled clearly with a short, descriptive text explaining its role in the process.\n"
        "- **Clarity**: Avoid unnecessary details and keep the flowchart simple to ensure readability. Ensure that there is no ambiguity in the transitions between nodes.\n"
        "- **Layout**: The flow should be organized vertically or horizontally to ensure the layout is easy to follow. Avoid crossing lines as much as possible.\n"
        "The flowchart should be easy to follow, visually distinct, and well-organized with clear labels for each step."
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
