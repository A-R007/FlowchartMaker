from flask import Flask, render_template, request, jsonify
import os
import logging
import uuid
import graphviz
from dotenv import load_dotenv
import groq as Groq
import re

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set Graphviz path explicitly (adjust the path if needed)
GRAPHVIZ_PATH = r"/usr/local/bin"  # For Vercel, this should work on the server
os.environ["PATH"] += os.pathsep + GRAPHVIZ_PATH

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

# Generate Flowchart using Groq LLM
def generate_flowchart(description):
    prompt = (
        f"Create a detailed and colorful flowchart in Graphviz DOT language that illustrates the following steps: {description}. "
        "Ensure the flowchart is visually appealing with color coding. "
        "Use distinct colors for different types of nodes and edges: "
        "- Use light blue for start and end nodes. "
        "- Use green for process nodes. "
        "- Use red for decision nodes. "
        "- Use blue for edges connecting nodes. "
        "Ensure each node and edge is clearly labeled with a logical flow from start to end."
    )
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        raw_response = response.choices[0].message.content.strip()
        dot_definition = extract_dot_definition(raw_response)
        if dot_definition and validate_dot_definition(dot_definition):
            return dot_definition
        logging.error(f"Invalid DOT definition extracted: {raw_response}")
        return None
    except Exception as e:
        logging.error(f"Groq API Error: {e}")
        return None

# Render Flowchart to an Image
def render_flowchart(dot_definition, output_folder="static/flowcharts"):
    os.makedirs(output_folder, exist_ok=True)
    file_id = uuid.uuid4().hex
    file_path = os.path.join(output_folder, f"flowchart_{file_id}")
    
    try:
        flowchart = graphviz.Source(dot_definition)
        output_path = f"{file_path}.png"
        flowchart.render(file_path, format="png", cleanup=True)
        return output_path
    except Exception as e:
        logging.error(f"Graphviz Rendering Error: {e}")
        logging.error(f"DOT definition that failed: {dot_definition}")
        return None

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_flowchart", methods=["POST"])
def generate():
    data = request.json
    description = data.get("description", "")

    if not description:
        return jsonify({"error": "No description provided"}), 400

    dot_definition = generate_flowchart(description)
    if not dot_definition:
        return jsonify({"error": "Failed to generate flowchart"}), 500

    output_path = render_flowchart(dot_definition)
    if not output_path:
        return jsonify({"error": "Failed to render flowchart"}), 500

    return jsonify({"flowchart_url": f"/{output_path}"})

if __name__ == "__main__":
    app.run(debug=True)
