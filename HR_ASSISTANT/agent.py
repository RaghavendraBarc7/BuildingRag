from langchain.agents import create_agent
from HR_ASSISTANT import config 

def create_hr_agent(llm, tools):
    return create_agent(
        model = llm, 
        tools = tools, 
        system_prompt=config.SYSTEM_PROMPT
    )   