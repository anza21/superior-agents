from loguru import logger

def trading_flow(session_id: str, agent_id: str, fe_data: dict, container_manager, notification_sources: list):
    """
    Main trading agent flow.

    Args:
        session_id (str): ID of the current session.
        agent_id (str): ID of the trading agent.
        fe_data (dict): Frontend configuration data.
        container_manager: Manages Docker container execution.
        notification_sources (list): Sources for notifications.

    Returns:
        None
    """
    logger.info(f"Starting Trading Agent flow for session {session_id} and agent {agent_id}")
    
    # Example: Fetch market data
    market_data = fetch_market_data()
    logger.info(f"Market Data: {market_data}")

    # Example: Execute a trading strategy
    trade_decision = execute_trading_strategy(market_data)
    logger.info(f"Trade Decision: {trade_decision}")

    # Example: Send execution command
    execute_trade(trade_decision)

    logger.info("Trading Agent cycle completed.")

def fetch_market_data():
    """
    Fetches latest market data.

    Returns:
        dict: Simulated market data.
    """
    return {"BTC": 65000, "ETH": 3200}

def execute_trading_strategy(market_data):
    """
    Executes a simple trading strategy.

    Args:
        market_data (dict): Current market prices.

    Returns:
        str: Trading decision.
    """
    if market_data["BTC"] > 60000:
        return "BUY BTC"
    else:
        return "SELL BTC"

def execute_trade(decision):
    """
    Executes a trade based on the decision.

    Args:
        decision (str): Trading action.

    Returns:
        None
    """
    logger.info(f"Executing trade: {decision}")

# ✅ Επιτρέπουμε το import
__all__ = ["trading_flow"]
