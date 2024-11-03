def save_to_html(feedback_data):
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .feedback { margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; }
            .positive { color: green; }
            .neutral { color: gray; }
            .negative { color: red; }
        </style>
    </head>
    <body>
    <h2>Customer Feedback Analysis</h2>
    """

    for _, row in feedback_data.iterrows():
        sentiment_class = "positive" if row["sentiment"] == "Positive" else "neutral" if row["sentiment"] == "Neutral" else "negative"
        html_content += f"""
        <div class="feedback">
            <h3>Customer: {row['customer_name']}</h3>
            <p><strong>Feedback:</strong> {row['feedback_text']}</p>
            <p><strong>Summary:</strong> {row['summary']}</p>
            <p class="{sentiment_class}"><strong>Sentiment:</strong> {row['sentiment']}</p>
            <p><strong>Features & Issues:</strong></p>
            <ul>
                {''.join(f'<li>{feature.strip()}</li>' for feature in row['features'].split('-') if feature.strip())}
            </ul>
        </div>
        """
    html_content += "</body></html>"

    with open("index.html", "w") as f:
        f.write(html_content)
    print("Report generated: index.html")
