from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def calculate_metrics(y_true, y_pred):
    """
    Calculates accuracy, precision, recall, and F1 score based on true and predicted sentiment labels.
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average='weighted'),
        "recall": recall_score(y_true, y_pred, average='weighted'),
        "f1_score": f1_score(y_true, y_pred, average='weighted')
    }
    return metrics

def print_metrics_report(metrics):
    """
    Prints the accuracy, precision, recall, and F1 score.
    """
    print("Sentiment Analysis Evaluation Metrics:")
    print(f"Accuracy: {metrics['accuracy']:.2f}")
    print(f"Precision: {metrics['precision']:.2f}")
    print(f"Recall: {metrics['recall']:.2f}")
    print(f"F1 Score: {metrics['f1_score']:.2f}") 

def load_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

negative_words = load_words('./evaluation/negative_words.txt')
positive_words = load_words('./evaluation/positive_words.txt')

def rule_based_sentiment(feedback_text):
    feedback_text = feedback_text.lower()
    if any(word in feedback_text for word in negative_words):
        return "Negative"
    elif any(word in feedback_text for word in positive_words):
        return "Positive"
    return "Neutral"
