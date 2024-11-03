import logging
from dotenv import load_dotenv
import os
import pandas as pd
from graph import create_graph
from helpers import evaluate, load_feedback_data
from render import save_to_html
import argparse

from langchain_core.runnables.graph import MermaidDrawMethod

def configure_logging(verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s 🔊 - %(message)s')

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def process_feedback_data(feedback_data):
    logging.debug("Starting to process feedback data")
    graph = create_graph()
    processed_data = []

    graph_image = graph.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
    )
    with open('./graph.png', 'wb') as f:
        f.write(graph_image)

    for _, feedback_entry in feedback_data.iterrows():
        logging.debug(f"Processing feedback entry: {feedback_entry['feedback_text']}")
        user_input = {"input": feedback_entry["feedback_text"]}
        result = graph.invoke(user_input)
        feedback_entry["summary"] = result["summary"]
        feedback_entry["sentiment"] = result["sentiment"]
        feedback_entry["features"] = result["features"]
        processed_data.append(feedback_entry)
        logging.debug(f"Processed entry: {feedback_entry}")

    logging.debug("Finished processing feedback data")
    return pd.DataFrame(processed_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--data-path', '-p', type=str, default='customer_feedback.csv', 
                        help='Path to the customer feedback data file')
    args = parser.parse_args()

    configure_logging(args.verbose)

    logging.info("🚀 Starting the feedback analysis process...")
    feedback_data = load_feedback_data(args.data_path)
    if feedback_data is not None:
        logging.info("Feedback data loaded successfully.")
        analyzed_data = process_feedback_data(feedback_data)
        save_to_html(analyzed_data)
        evaluate(analyzed_data)
        logging.info("Analysis complete. Report generated: index.html")
    else:
        logging.error("Failed to load feedback data.")
