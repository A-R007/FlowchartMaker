# Flask Groq Flowchart Generator

This is a Flask-based web application that integrates with the **Groq API** to generate flowcharts in **Graphviz DOT** format based on user-provided descriptions. The app allows users to visualize processes as flowcharts with distinct color schemes and node types for better readability.

## Features

- **Flowchart Generation**: Generate flowcharts in Graphviz DOT format based on natural language descriptions.
- Color-coded Nodes:
  - **Start/End Nodes**: Light blue, round-shaped nodes representing the start or end of a process.
  - **Process Nodes**: Green, rectangular nodes with slightly rounded corners representing actions or tasks.
  - **Decision Nodes**: Red, diamond-shaped nodes representing decision points in the process flow.
- **Node Labeling**: Each node is labeled with descriptive text explaining its role.
- **Customizable Flow Layout**: Flowcharts can be organized either vertically or horizontally with clear, readable transitions.
- **Validation**: The app extracts and validates the DOT definition to ensure correct syntax.

## Prerequisites

Before running the app, ensure the following are installed:

- Python 3.11 or later
- `pip` (Python's package installer)

## Setup Instructions

### 1. Clone the Repository

Clone the project to your local machine using the following command:

```bash
git clone <repo-link>
cd <your-folder>
```

### 2. Create and Activate a Virtual Environment

Create and activate a virtual environment to isolate the dependencies:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of your project and add your **Groq API Key**:

```ini
GROQ_API_KEY=your_api_key_here
```

You can obtain an API key from the [Groq website](https://groq.com/).

### 5. Run the Application

Start the Flask application locally:

```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000/` in your browser.

### 6. Deploy on Render (Optional)

To deploy the app on Render:

1. Push your code to GitHub.
2. Sign in to [Render](https://render.com) and create a new web service.
3. Connect the service to your GitHub repository.
4. Add the following to your `Procfile` to specify how to start the app:

    ```plaintext
    web: gunicorn app:app
    ```

5. After deployment, the app will be available at a Render-generated domain.

## Usage

1. **Home Page**: Visit the home page (`/`) to access the web interface.
2. **Generate Flowchart**: Send a POST request to the `/generate_flowchart` endpoint with a JSON body containing a `description` field. The description should be a text representation of the process you want to visualize in the flowchart.
   
   Example request:
   
   ```json
   {
     "description": "A process that starts, performs a task, and ends with a decision."
   }
   ```

3. **Flowchart Response**: The response will be a JSON object containing the flowchart in DOT format. Use Graphviz tools to render the flowchart visually.

### Example Response:

```json
{
  "dot_definition": "digraph G { ... }"
}
```

### Error Handling:

- **Missing Description**: If no description is provided in the request, the server will respond with a `400 Bad Request` error.
  
  Example:

  ```json
  {
    "error": "No description provided"
  }
  ```

- **Flowchart Generation Failure**: If the flowchart generation fails, the server will respond with a `500 Internal Server Error`.
  
  Example:

  ```json
  {
    "error": "Failed to generate flowchart"
  }
  ```

## Troubleshooting

- **Bad Gateway Error**: Ensure that the Flask app is running correctly and check your deployment settings.
- **Invalid API Key**: If the flowchart is not being generated, ensure that you have set your **GROQ_API_KEY** correctly in the `.env` file.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.
