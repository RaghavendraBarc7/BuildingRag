from langchain_anthropic import ChatAnthropic

from HR_ASSISTANT import config 

def get_llm():
    llm = ChatAnthropic(
    model = config.LLM_MODEL_NAME, 
    api_key = config.claude_key,
    max_tokens = 16000, # upper limit on the length of each response
    effort = "medium",  # how much Claude thinks before answering: "low" | "medium" | "high" | "xhigh" | "max"
    # No temperature here - Claude Opus 5.5 doesn't accept temperature/top_p/top_k (the request fails if you set them).

    # If Claude declines a request for safety reasons, the API automatically retries it on a fallback Claude model.
    betas = ["server-side-fallback-2026-07-01"],
    model_kwargs = {"fallbacks": "default"},
)
    return llm