# Customer Feedback Analyzer with LLM Integration

## Overview
This project implements a data processing pipeline that analyzes customer feedback using a Language Model (LLM). It evaluates the results and presents the findings on a simple web page.

## Table of Contents
- [Objective](#objective)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Deliverables](#deliverables)
- [Evaluation Metrics](#evaluation-metrics)
- [License](#license)

## Objective
The main objective of this project is to build a pipeline that:
1. Ingests customer feedback from a CSV file.
2. Processes the feedback using an LLM to generate summaries, determine sentiment, and extract features.
3. Stores the processed data and presents it in an HTML format.

## Requirements
- Python 3.x
- Libraries:
  - `pandas`
  - `langchain_openai`
  - `langchain_core`
  - `langgraph`
  - `langchain`
  - `python-dotenv`
  - `argparse` (used for parsing arguments to the CLI invocation)
  - `MermaidDrawMethod` (used to plot the LangGraph graph)
  - `numpy==1.23.5` (ensure compatibility with langchain)
  - `sklearn`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Danieloni1/langgraph-feedback-ingestor.git
   cd langgraph-feedback-ingestor/src
   ```
2. Install the required libraries using pip:
   ```bash
   pip install pandas langchain_openai langchain_core langgraph python-dotenv
   ```

## Usage
1. Prepare your CSV file named `customer_feedback.csv` (under src directory) with the following columns:
   - `feedback_id` (integer)
   - `customer_name` (string)
   - `feedback_text` (string)
   - `submission_date` (date)

2. Run the main script:
   ```bash
   python main.py --data-path path/to/customer_feedback.csv # -v for verbose logging
   ```

3. After processing, the results will be saved in `index.html` and a graph image will be saved as `graph.png`.

## File Structure
```
.
├── .gitignore
├── README.md
├── src
│   ├── main.py
│   ├── agents.py
│   ├── graph.py
│   ├── helpers.py
│   ├── render.py
│   ├── ingested-data-index.html
│   ├── evaluation
│   │   ├── negative_words.txt
│   │   ├── positive_words.txt
|   |   ├── metrics.py
```

## Deliverables
- Python scripts for data processing and analysis.
- HTML file (`ingested-data-index.html`) containing the analysis results.
- A graph image (`graph.png`) representing the workflow of the feedback analysis process.
