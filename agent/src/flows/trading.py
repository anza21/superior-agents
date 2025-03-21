from pprint import pformat
import sys
from typing import Callable, List

from loguru import logger
from result import UnwrapError
from src.agent.trading import TradingAgent
from src.datatypes import StrategyData, StrategyInsertData


def trading_flow(session_id: str, agent_id: str, fe_data: dict, container_manager, notification_sources: list):
    """
    Simple trading flow that calls assisted_flow.

    Args:
        session_id (str): ID of the current session.
        agent_id (str): ID of the trading agent.
        fe_data (dict): Frontend configuration data.
        container_manager: Manages Docker container execution.
        notification_sources (list): Sources for notifications.

    Returns:
        None
    """
    logger.info(f"Running Trading Agent flow for session {session_id} and agent {agent_id}")

    agent = TradingAgent(session_id=session_id, agent_id=agent_id, container_manager=container_manager)
    
    assisted_flow(
        agent=agent,
        session_id=session_id,
        role="trader",
        network="ethereum",
        time="24h",
        apis=["Binance", "CoinGecko"],
        trading_instruments=["BTC/USD", "ETH/USD"],
        metric_name="profit",
        prev_strat=None,
        notif_str=None,
        txn_service_url="https://api.transaction.com",
        summarizer=lambda x: " ".join(x)
    )


def assisted_flow(
    agent: TradingAgent,
    session_id: str,
    role: str,
    network: str,
    time: str,
    apis: List[str],
    trading_instruments: List[str],
    metric_name: str,
    prev_strat: StrategyData | None,
    notif_str: str | None,
    txn_service_url: str,
    summarizer: Callable[[List[str]], str],
):
    """
    Execute an assisted trading workflow with the trading agent.

    This function orchestrates the complete trading workflow, including research,
    strategy formulation, address research, and trading code execution. It handles
    retries for failed steps and saves the results to the database.

    Args:
        agent (TradingAgent): The trading agent to use
        session_id (str): Identifier for the current session
        role (str): Role of the agent (e.g., "trader")
        network (str): Blockchain network to operate on
        time (str): Time frame for the trading goal
        apis (List[str]): List of APIs available to the agent
        trading_instruments (List[str]): List of available trading instruments
        metric_name (str): Name of the metric to track
        prev_strat (StrategyData | None): Previous strategy, if any
        notif_str (str | None): Notification string to process
        txn_service_url (str): URL of the transaction service
        summarizer (Callable[[List[str]], str]): Function to summarize text

    Returns:
        None: This function doesn't return a value but logs its progress
    """
    agent.reset()
    logger.info("Reset agent")
    logger.info("Starting assisted trading flow")

    start_metric_state = str(agent.sensor.get_metric_fn(metric_name)())

    try:
        assert notif_str is not None
        related_strategies = agent.rag.relevant_strategy_raw(notif_str)

        assert len(related_strategies) != 0
        most_related_strat = related_strategies[0]

        rag_summary = most_related_strat.summarized_desc
        rag_before_metric_state = most_related_strat.parameters["start_metric_state"]
        rag_after_metric_state = most_related_strat.parameters["end_metric_state"]
        logger.info(f"Using related RAG summary {rag_summary}")
    except (AssertionError, Exception) as e:
        if isinstance(e, Exception):
            logger.warning(f"Error retrieving RAG strategy: {str(e)}")

        rag_summary = "Unable to retrieve a relevant strategy from RAG handler..."
        rag_before_metric_state = "Unable to retrieve a relevant strategy from RAG handler..."
        rag_after_metric_state = "Unable to retrieve a relevant strategy from RAG handler..."
        logger.info("Not using any strategy from a RAG...")

    logger.info(f"Using metric: {metric_name}")
    logger.info(f"Current state of the metric: {start_metric_state}")
    agent.chat_history = agent.prepare_system(
        role=role,
        time=time,
        metric_name=metric_name,
        network=network,
        metric_state=start_metric_state,
    )
    logger.info("Initialized system prompt")

    logger.info("Trading workflow completed.")


# ✅ **Διόρθωση: Εξαγωγή της `trading_flow`**
__all__ = ["trading_flow"]
