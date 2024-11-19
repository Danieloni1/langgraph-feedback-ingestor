import asyncio

from activities import detect_sentiment, extract_features, summarize_feedback
from temporalio.worker import Worker
from temporalio.client import Client

from workflow import FeedbackProcessingWorkflow

interrupt_event = asyncio.Event()

async def run_worker():
    client = await Client.connect("temporal:7233", namespace="default")
    worker = Worker(
        client,
        task_queue="feedback-task-queue",
        workflows=[FeedbackProcessingWorkflow],
        activities=[summarize_feedback, detect_sentiment, extract_features],
    )

    print("\nWorker started, ctrl+c to exit\n")
    await worker.run()
    try:
        await interrupt_event.wait()
    finally:
        print("\nShutting down the worker\n")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_worker())
    except KeyboardInterrupt:
        print("\nInterrupt received, shutting down...\n")
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())