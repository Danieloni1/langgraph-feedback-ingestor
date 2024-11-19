from datetime import timedelta
from temporalio import workflow

# Import activities
with workflow.unsafe.imports_passed_through():
    from activities import summarize_feedback, detect_sentiment, extract_features

@workflow.defn
class FeedbackProcessingWorkflow:
    @workflow.run
    async def run(self, input_data):
        summary = await workflow.execute_activity(
            summarize_feedback,
            input_data,
            start_to_close_timeout=timedelta(seconds=30),
        )

        sentiment = await workflow.execute_activity(
            detect_sentiment,
            input_data,
            start_to_close_timeout=timedelta(seconds=30),
        )
        
        features = await workflow.execute_activity(
            extract_features,
            input_data,
            start_to_close_timeout=timedelta(seconds=30),
        )
        
        return {"summary": summary, "sentiment": sentiment, "features": features}
