# Customer Feedback Analyzer with LLM Integration

## Overview
This project implements a data processing pipeline that analyzes customer feedback using a Language Model (LLM). It evaluates the results and presents the findings on a simple web page.

## Table of Contents
- [Objective](#objective)
- [Requirements](#requirements)
- [Installation (for running locally)](#installation-for-running-locally)
- [Usage (locally)](#usage-locally)
- [Usage (containerized)](#usage-containerized)

## Objective
Build a data processing pipeline that analyzes customer feedback using a Language Model (LLM), evaluates the results, and presents the findings on a simple web page. The project will involve developing a Python script for data processing, crafting effective prompts for LLM integration, implementing a sentiment analysis evaluation, and creating a user-friendly HTML presentation of the results. By leveraging Temporal, we can easily handle retries, state management, and orchestration of tasks, which enhances the overall efficiency and resilience of the application.

## Requirements
- Python 3.x
- Docker (optional)
- Docker compose (optional)

## Installation (for running locally)
1. Clone the repository:
   ```bash
   git clone https://github.com/Danieloni1/langgraph-feedback-ingestor.git
   cd langgraph-feedback-ingestor/src
   ```
2. Install the required libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage (locally)
1. Start the Temporal server:
   ```bash
   temporal server start-dev
   ```

2. Run the worker:
   ```bash
   python worker.py
   ```

3. Run the main application:
   ```bash
   python app.py
   ```

4. Prepare your CSV file with the following columns:
   - `feedback_id` (integer)
   - `customer_name` (string)
   - `feedback_text` (string)
   - `submission_date` (date)

5. After processing, the results will be disaplyed, a graph image will be saved as `graph.png` and evaluation will be saved to `evaluation/evaluation.txt`.

## Usage (containerized)
You can also run the application containerized:

1. Build and run the application, simply use docker compose:
   ```bash
   docker compose up --build
   ```
   Then visit `localhost:5001` for the app and `localhost:8080` for the Temporal dashboard.
