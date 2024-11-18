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
            #filter { margin-bottom: 20px; }
        </style>
        <script>
            function filterFeedback() {
                const searchInput = document.getElementById('searchInput').value.toLowerCase();
                const sentimentFilter = document.getElementById('sentimentFilter').value;
                const feedbackDivs = document.getElementsByClassName('feedback');

                for (let feedback of feedbackDivs) {
                    const feedbackText = feedback.innerText.toLowerCase();
                    const sentimentClass = feedback.classList.contains('positive') ? 'Positive' :
                                           feedback.classList.contains('neutral') ? 'Neutral' :
                                           feedback.classList.contains('negative') ? 'Negative' : '';

                    const matchesSearch = feedbackText.includes(searchInput);
                    const matchesSentiment = sentimentFilter === 'All' || sentimentFilter === sentimentClass;

                    if (matchesSearch && matchesSentiment) {
                        feedback.style.display = 'block';
                    } else {
                        feedback.style.display = 'none';
                    }
                }
            }
        </script>
    </head>
    <body>
    <h2>Customer Feedback Analysis</h2>
    <div id="filter">
        <input type="text" id="searchInput" placeholder="Search feedback..." onkeyup="filterFeedback()" style="text-align: center;">
        <select id="sentimentFilter" onchange="filterFeedback()" style="text-align: center;">
            <option value="All">All Sentiments</option>
            <option value="Positive">Positive</option>
            <option value="Neutral">Neutral</option>
            <option value="Negative">Negative</option>
        </select>
    </div>
    """

    for _, row in feedback_data.iterrows():
        sentiment_class = "positive" if row["sentiment"] == "Positive" else "neutral" if row["sentiment"] == "Neutral" else "negative"
        html_content += f"""
        <div class="feedback {sentiment_class}">
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
    
    return html_content
