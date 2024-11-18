import logging
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import subprocess
import os
from helpers import load_feedback_data
from main import process_feedback_data
from render import save_to_html
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

app = Flask(__name__)

TEMPLATE_DIR = os.path.abspath('./templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data_path = request.form['data_path']
        if data_path:
            try:
                subprocess.run(
                    ['python', 'main.py', '--data-path', data_path],
                    check=True
                )
                logging.info("Feedback ingestor ran successfully.")
                return redirect(url_for('success'))
            except subprocess.CalledProcessError as e:
                logging.error(f"Error running feedback ingestor: {e}")
                return f"Error: {e}", 500
    return render_template('index.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    if 'file' not in request.files:
        logging.warning("No file part in the request.")
        return "No file part", 400

    file = request.files['file']
    data_path = request.form.get('data_path')

    if file.filename == '':
        logging.warning("No selected file.")
        return "No selected file", 400

    if file and file.filename.endswith('.csv'):
        feedback_data = pd.read_csv(file)
    elif data_path:
        feedback_data = load_feedback_data(data_path)
    else:
        logging.warning("No valid input provided.")
        return "No valid input provided.", 400

    if feedback_data is not None:
        analyzed_data = process_feedback_data(feedback_data)
        html_content = save_to_html(analyzed_data)
        return html_content
    logging.error("Failed to load feedback data.")
    return "Failed to load feedback data.", 500

@app.route('/success')
def success():
    return '''
    <div>
        <p>Feedback ingestor ran successfully!</p>
        <a href="/ingested-data-index" class="btn" style="display: inline-block; padding: 10px 20px; background-color: blue; color: white; text-decoration: none; border-radius: 5px;">Go to Index</a>
    </div>
    '''

@app.route('/ingested-data-index')
def ingested_data_index():
    try:
        return send_from_directory('.', 'ingested-data-index.html')
    except Exception:
        logging.error("Failed to send ingested data index.")
        return "There's nothing here", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
