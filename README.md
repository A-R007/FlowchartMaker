```markdown
# Flask Groq Flowchart Generator

This is a Flask-based web application that uses the Groq API to generate flowcharts in Graphviz DOT language based on a description provided by the user. The flowchart is created with specific formatting guidelines, including colors for different types of nodes and a clear, structured layout.

## Features

- **Generate Flowcharts**: Input a description, and the app generates a flowchart in DOT format.
- **Visual Styling**: The flowchart is styled with color-coding and node shapes to represent different stages in a process.
- **Flask Backend**: The app uses Flask as the web framework for routing and handling requests.
- **Groq API Integration**: The app uses the Groq API to generate the flowchart from the user's description.

## Prerequisites

Before running the app, make sure you have the following installed:

- Python 3.11 or later
- `pip` (Python's package installer)

## Setup Instructions

### 1. Clone the repository

Clone the project to your local machine using:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Create and activate a virtual environment

For a clean Python environment, create and activate a virtual environment:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root of your project and add your **Groq API Key**:

```ini
GROQ_API_KEY=your_api_key_here
```

### 5. Run the application

Run the Flask app locally:

```bash
python app.py
```

By default, the app will be available at `http://127.0.0.1:5000/` in your web browser.

### 6. Deploy on Render

To deploy the app on Render, follow these steps:

1. Push your code to GitHub if you haven't already.
2. Sign in to [Render](https://render.com) and create a new web service.
3. Connect the service to your GitHub repository and deploy.
4. Ensure your `Procfile` contains the correct start command:

    ```
    web: gunicorn app:app
    ```

5. After the deployment is successful, your service will be available on a Render domain.

## Usage

1. Open the deployed or local application in your browser.
2. Enter a description of the process you want to visualize in the flowchart.
3. Click the button to generate the flowchart.
4. The response will be a JSON object containing the DOT format for the flowchart, which can be rendered using tools like [Graphviz](https://graphviz.gitlab.io/).

## Troubleshooting

- **Bad Gateway Error**: This could be due to incorrect port configuration or issues with the Flask app. Make sure that `app.run()` is binding to the correct port (using `PORT` from the environment variables).
- **Invalid Groq API Key**: If the flowchart is not being generated, ensure that you have correctly set up your **GROQ_API_KEY** in the `.env` file.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License.
```

### Explanation:
- **Features**: Lists the main functionalities of the application.
- **Prerequisites**: Details the required software versions.
- **Setup Instructions**: Provides a step-by-step guide for setting up and running the app locally.
- **Deployment**: Explains how to deploy the app on Render.
- **Usage**: Describes the flow of using the app, including generating the flowchart.
- **Troubleshooting**: Provides common issues and solutions.
- **Contributing**: Instructions for contributing to the project.
- **License**: Mentions the project's license (MIT License in this case).

Feel free to customize it based on your preferences or additional features!
