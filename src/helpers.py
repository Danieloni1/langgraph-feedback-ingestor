import pandas as pd
from evaluation.metrics import calculate_metrics, rule_based_sentiment
import json

def load_feedback_data(file_path):
    try:
        feedback_data = pd.read_csv(file_path)
        
        feedback_data = feedback_data.dropna(subset=["feedback_text"])
        
        feedback_data['customer_name'] = feedback_data['customer_name'].fillna('Unknown')
        feedback_data['submission_date'] = pd.to_datetime(feedback_data['submission_date'], errors='coerce')
        feedback_data['submission_date'] = feedback_data['submission_date'].fillna(pd.Timestamp.now())
        
        feedback_data = feedback_data.drop_duplicates(subset=["feedback_id"])
        
        return feedback_data
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return None

def evaluate(feedback_data):
    feedback_data["sentiment"] = feedback_data["feedback_text"].apply(rule_based_sentiment)
    
    metrics = calculate_metrics(feedback_data["sentiment"], feedback_data["sentiment"])

    with open('evaluation/evaluation.txt', 'w') as report_file:
        report_file.write(json.dumps(metrics, indent=4))