from src.agent.marketing import MarketingAgent
from loguru import logger
from result import Result
from src.agent.schema import ChatHistory
import json

def unassisted_flow(agent: MarketingAgent, session_id: str, **kwargs):
    agent.reset()
    logger.info("Starting unassisted marketing flow")

    # ✅ Σωστή διαχείριση ChatHistory
    if isinstance(agent.chat_history, ChatHistory):
        agent.chat_history = [{"role": msg.role, "content": msg.content} for msg in agent.chat_history.messages]

    # ✅ Ανάκτηση στρατηγικής RAG με έλεγχο σφαλμάτων
    try:
        notif_str = kwargs.get("notif_str", None)
        assert notif_str is not None
        related_strategies = agent.rag.relevant_strategy_raw(notif_str)

        if not related_strategies:
            raise ValueError("No relevant strategies found in RAG handler.")

        most_related_strat = related_strategies[0]
        rag_summary = most_related_strat.summarized_desc
        rag_before_metric_state = most_related_strat.parameters.get("start_metric_state", "N/A")
        rag_after_metric_state = most_related_strat.parameters.get("end_metric_state", "N/A")
        logger.info(f"Using related RAG summary {rag_summary}")

    except (AssertionError, Exception) as e:
        logger.warning(f"Error retrieving RAG strategy: {str(e)}")
        rag_summary = "Unable to retrieve a relevant strategy from RAG handler..."
        rag_before_metric_state = "N/A"
        rag_after_metric_state = "N/A"
        logger.info("Not using any strategy from RAG handler.")

    # ✅ Δημιουργία ερευνητικού κώδικα
    try:
        research_code_result = agent.gen_research_code_on_first(kwargs["apis"])

        if not research_code_result.is_ok():
            logger.error(f"Research code generation failed: {research_code_result.err()}")
            return

        research_code, _ = research_code_result.ok()
        logger.info("Research code generated successfully")


        agent.db.insert_chat_history(session_id, research_code)
        logger.info("Chat history updated successfully")

    except Exception as e:
        logger.error(f"Unexpected error in marketing agent: {e}")
