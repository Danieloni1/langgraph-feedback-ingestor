import os
from dotenv import load_dotenv
from temporalio import activity
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

@activity.defn
async def summarize_feedback(state):
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = PromptTemplate.from_template(
        "Summarize the feedback in one detailed sentence: {input}"
    )
    chain = prompt | llm
    response = await chain.ainvoke(state)
    return response.content.strip()


@activity.defn
async def detect_sentiment(state):
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = PromptTemplate.from_template(
        "Determine the sentiment of this feedback summary (Positive, Negative, Neutral). Make sure you recognize ambiguity and sarcasm: {input}. Only answer with a single word: \"Positive\", \"Negative\" or \"Neutral\""
    )
    chain = prompt | llm
    response = await chain.ainvoke(state)
    return response.content.strip()


@activity.defn
async def extract_features(state):
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = PromptTemplate.from_template(
        "Extract product features or issues mentioned in this feedback: {input}"
    )
    chain = prompt | llm
    response = await chain.ainvoke(state)
    return response.content.strip()
