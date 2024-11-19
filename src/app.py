from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import uvicorn
import logging
import pandas as pd
from temporalio.client import Client
from helpers import evaluate, load_feedback_data
from render import save_to_html
from workflow import FeedbackProcessingWorkflow

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal_client = await Client.connect("temporal:7233")
    yield

app = FastAPI(lifespan=lifespan)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

@app.get("/", response_class=HTMLResponse)
async def index():
    try:
        with open('index.html') as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logging.error(f"Error reading index.html: {e}")
        return HTMLResponse(content="Error loading page", status_code=500)

@app.post("/generate_report")
async def generate_report(file: UploadFile = File(...), data_path: str = None):
    if file.filename == '':
        logging.warning("No selected file.")
        return {"error": "No selected file"}, 400

    if file and file.filename.endswith('.csv'):
        feedback_data = pd.read_csv(file.file)
    elif data_path:
        feedback_data = load_feedback_data(data_path)
    else:
        logging.warning("No valid input provided.")
        return {"error": "No valid input provided."}, 400

    if feedback_data is not None:
        try:
            workflow_result = await trigger_workflow(feedback_data)
            html_content = save_to_html(pd.DataFrame(workflow_result))
            evaluate(workflow_result)
            logging.info("🫡 Analysis complete. Report generated")
            return HTMLResponse(content=html_content)
        except Exception as e:
            logging.error(f"Error running Temporal workflow: {e}")
            return {"error": str(e)}, 500
    logging.error("Failed to load feedback data.")
    return {"error": "Failed to load feedback data."}, 500

@app.get("/success", response_class=HTMLResponse)
async def success():
    return '''
    <div>
        <p>Feedback processing workflow ran successfully!</p>
        <a href="/ingested-data-index" class="btn" style="display: inline-block; padding: 10px 20px; background-color: blue; color: white; text-decoration: none; border-radius: 5px;">Go to Index</a>
    </div>
    '''

@app.get("/ingested-data-index")
async def ingested_data_index():
    try:
        with open('ingested-data-index.html') as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logging.error(f"Error reading ingested-data-index.html: {e}")
        return HTMLResponse(content="Error loading page", status_code=500)

async def trigger_workflow(feedback_records):
    """
    Start the workflow with feedback data.
    """
    processed_data = []
    for index, feedback_entry in feedback_records.iterrows():
        logging.debug(f"Processing feedback entry: {feedback_entry['feedback_text']}")
        user_input = {"input": feedback_entry["feedback_text"]}
        result = await app.state.temporal_client.execute_workflow(
            FeedbackProcessingWorkflow.run,
            user_input,
            id=f"feedback-processing-workflow-{uuid4()}",
            task_queue="feedback-task-queue",
        )        
        feedback_entry["summary"] = result["summary"]
        feedback_entry["sentiment"] = result["sentiment"]
        feedback_entry["features"] = result["features"]
        processed_data.append(feedback_entry)
        logging.debug(f"Processed entry: {feedback_entry}")

        if (index + 1) % 10 == 0:
            logging.info(f"🙇🏾‍♀️ Processed {index + 1} out of {len(feedback_records)} records...")

    logging.info("✅ Finished processing feedback data")
    return pd.DataFrame(processed_data)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5001)
