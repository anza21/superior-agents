import os
import json
from typing import Dict

DEFAULT_PROMPTS = {
    "system_prompt": "You are a {role} social media influencer.\nToday's date is {today_date}.\nYour goal is to maximize {metric_name} within {time}\nYou are currently at {metric_state}",
    "strategy_prompt": "You just learnt the following information: \n<LatestNotification>\n{notifications_str}\n</LatestNotifications>\n<ResearchOutput>\n{research_output_str}\n</ResearchOutput>\nDecide what what you should do to help you maximize {metric_name} within {time}. \nChoose one action and write a short paragraph explaining how you will do it.",
    "marketing_code_prompt": "Please write code to implement this strategy:\n<Strategy>\n{strategy_output}\n</Strategy>\nYou have the following APIs:\n<APIs>\n{apis_str}\n</APIs>\nFormat the code as follows:\n```python\nfrom dotenv import load_dotenv\nimport ...\n\nload_dotenv()\n\ndef main():\n    ....\n\nmain()\n```",
    "regen_code_prompt": "Given these errors:\n<Errors>\n{errors}\n</Errors>\nAnd the code it's from:\n<Code>\n{previous_code}\n</Code>\nYou are to generate code that fixes the error but doesn't stray too much from the original code, in this format:\n```python\nfrom dotenv import load_dotenv\nimport ...\n\nload_dotenv()\n\ndef main():\n    ....\n\nmain()\n```",
    "research_code_prompt_first": "You know nothing about your environment.\nWhat do you do now?\nYou can use the following APIs to do research:\n<APIs>\n{apis_str}\n</APIs>\nYou are to print for everything, and raise every error or unexpected behavior of the program.\nPlease write code using the format below to research the state of the market.\n```python\nfrom dotenv import load_dotenv\nimport ...\n\nload_dotenv()\n\ndef main():\n    ....\n\nmain()\n```",
    "research_code_prompt": "Here is what is going on in your environment right now : \n<LatestNotification>\n{notifications_str}\n</LatestNotification>\nHere is what you just tried : \n<PrevStrategy>\n{prev_strategy} \n</PrevStrategy>\nFor reference, in the past when you encountered a similar situation you reasoned as follows:\n<RAG>\n{rag_summary}\n</RAG>\nThe result of this RAG was\n<BeforeStrategyExecution>\n{before_metric_state}\n</BeforeStrategyExecution>\n<AfterStrategyExecution>\n{after_metric_state}\n</AfterStrategyExecution>\nYou are to print for everything, and raise every error or unexpected behavior of the program.\nPlease write code using format below to research what is going on in the world and how best to react to it.\n```python\nfrom dotenv import load_dotenv\nimport ...\n\nload_dotenv()\n\ndef main():\n    ....\n\nmain()\n```",
}


def fetch_fe_data(agent_id: str) -> Dict:
    """
    Dummy function that simulates fetching frontend configuration for a given agent.
    In a real environment, this might pull from a database or an API.

    Args:
        agent_id (str): Unique identifier for the agent

    Returns:
        Dict: A dictionary containing frontend data and prompt templates
    """
    print(f"[INFO] Fetching frontend configuration for agent: {agent_id}")
    
    # Στο μέλλον μπορεί να τραβάει από DB ή API
    return {
        "in_con_env": True,
        "notification_sources": ["twitter_mentions", "twitter_feed"],
        **DEFAULT_PROMPTS,
    }
