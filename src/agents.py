import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

def summarize_feedback(state):
    llm = ChatOpenAI()
    prompt = PromptTemplate.from_template(
        "Summarize the feedback in one detailed sentence: {input}"
    )
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    return {"summary": response.content.strip()}


def detect_sentiment(state):
    llm = ChatOpenAI()
    prompt = PromptTemplate.from_template(
        "Determine the sentiment of this feedback summary (Positive, Negative, Neutral). Make sure you recognize ambiguity and sarcasm: {input}"
    )
    chain = prompt | llm
    response = chain.invoke({"input": state["summary"]})
    return {"sentiment": response.content.strip()}


def extract_features(state):
    llm = ChatOpenAI()
    prompt = PromptTemplate.from_template(
        "Extract product features or issues mentioned in this feedback: {input}"
    )
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    return {"features": response.content.strip()}
