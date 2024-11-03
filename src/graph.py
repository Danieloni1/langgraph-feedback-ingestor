from langgraph.graph import StateGraph, END
from agents import analyze_question, summarize_feedback, detect_sentiment, extract_features

class AgentState(dict):
    input: str
    summary: str
    sentiment: str
    features: str


def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("analyze", analyze_question)
    workflow.add_node("summarize", summarize_feedback)
    workflow.add_node("sentiment_analysis", detect_sentiment)
    workflow.add_node("features_issues_extraction", extract_features)

    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "summarize")
    workflow.add_edge("summarize", "sentiment_analysis")
    workflow.add_edge("sentiment_analysis", "features_issues_extraction")
    workflow.add_edge("features_issues_extraction", END)

    return workflow.compile()
