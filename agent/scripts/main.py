import sys
import time
import docker
from src.manager import fetch_fe_data
from src.flows.marketing import unassisted_flow as marketing_flow
from src.flows.trading import trading_flow
from src.utils.container_utils import ContainerManager  # Σωστό path!

def setup_marketing_agent_flow(fe_data, session_id, agent_id):
    in_con_env = fe_data.get("in_con_env", False)

    container_manager = ContainerManager(
        client=docker.from_env(),
        container_name="agent-executor",
        code_path="./code",
        in_con_env=in_con_env
    )

    notif_sources = fe_data.get("notification_sources", ["twitter_mentions", "twitter_feed"])
    return container_manager, notif_sources, marketing_flow

def setup_trading_agent_flow(fe_data, session_id, agent_id):
    in_con_env = fe_data.get("in_con_env", False)

    container_manager = ContainerManager(
        client=docker.from_env(),
        container_name="agent-executor",
        code_path="./code",
        in_con_env=in_con_env
    )

    notif_sources = fe_data.get("notification_sources", ["coingecko"])
    return container_manager, notif_sources, trading_flow

def run_agent(agent_type, session_id, agent_id):
    print(f"[INFO] Running {agent_type} agent for session {session_id}")

    fe_data = fetch_fe_data(agent_id)

    if agent_type == "marketing":
        container_manager, notif_sources, flow = setup_marketing_agent_flow(fe_data, session_id, agent_id)
    elif agent_type == "trading":
        container_manager, notif_sources, flow = setup_trading_agent_flow(fe_data, session_id, agent_id)
    else:
        print("[ERROR] Invalid agent type. Use 'marketing' or 'trading'.")
        sys.exit(1)

    while True:
        try:
            flow(session_id=session_id, agent_id=agent_id, fe_data=fe_data,
                 container_manager=container_manager, notification_sources=notif_sources)
        except Exception as e:
            print(f"[ERROR] Agent execution failed: {str(e)}")

        print(f"[INFO] Waiting for 900 seconds before starting a new cycle...")
        time.sleep(900)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py [marketing|trading] [session_id] [agent_id]")
        sys.exit(1)

    agent_type = sys.argv[1]
    session_id = sys.argv[2]
    agent_id = sys.argv[3]

    run_agent(agent_type, session_id, agent_id)

