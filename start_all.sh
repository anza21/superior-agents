#!/bin/bash
echo "🚀 Starting Superior Agents full stack..."

# Start Docker containers
cd ~/projects/superior-agents/agent/docker
docker compose up -d

# Start REST API
cd ~/projects/superior-agents/rest-api
source ../rest-api-venv/bin/activate
uvicorn routes.api:app --port 9020 &

# Start RAG API
cd ~/projects/superior-agents/rag-api
source ../rag-api-venv/bin/activate
uvicorn api:app --port 8080 &

# Start TXN Signer
cd ~/projects/superior-agents/agent
source ../agent-venv/bin/activate
uvicorn tee_txn_signer:app --port 9021 &

# Start default marketing agent
cd ~/projects/superior-agents/agent
source ../agent-venv/bin/activate
python -m scripts.main marketing run 470c13d1-39e4-42ce-8ae0-35fffa68c269 &

echo "✅ All components started in background!"
