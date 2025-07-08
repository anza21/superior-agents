# 🧠 SuggestoAI_Agent – Autonomous Affiliate Marketing Agent

## 🧩 Agent Overview
You are an AI developer within the `Cursos` platform. Your task is to **develop, finalize, and activate** the `SuggestoAI_Agent`, an autonomous agent focused on affiliate product discovery, content generation, and omnichannel publishing.

## 🗂️ Repositories
This agent uses **two** repositories:

- `superior-agents` → 🧠 main agent logic, API interaction, scheduling, learning loop.
- `suggestoai-site` → 🌐 website frontend, where the agent publishes SEO articles, comparisons, or product posts via Git.

Both are synced with GitHub and ready for use.

---

## ✅ Goals
1. **Discover affiliate products** via APIs (Amazon, AliExpress, eBay).
2. **Generate structured content** using local LLMs with RAG (blog posts, pros & cons, Q&A, SEO).
3. **Publish automatically** to:
   - Facebook Page
   - Instagram Business
   - LinkedIn
   - Twitter
   - And update the suggestoai-site repo
4. **Track performance** (clicks, engagement, conversions).
5. **Self-improve** through feedback from results.

---

## ⚙️ Architecture Notes
- Local models run via CUDA (Llama3, etc.)
- .env includes all API keys and tokens.
- Facebook Graph API integration complete.
- Git-controlled publishing already works (via GitHub push).
- Meta Business, AliExpress API, and domain verification completed.

---

## 🔁 You Must:
- Read all existing agent logic and workflows.
- Identify missing parts and TODOs.
- Complete agent behaviors (content loop, scheduler, error handling).
- Trigger a first **test pack run** and publish at least one real content item.

---

## 💡 Suggestions
- Use `openai`, `requests`, `apscheduler`, or `langchain` where appropriate.
- Implement RAG using ChromaDB or similar.
- Use git Python library to push content to `suggestoai-site`.

---

## 📍 Developer Notes
This agent is part of the **Superior Agents Summer Residency**, and is meant to be a showcase of autonomous affiliate intelligence. It must operate **without human assistance** after launch.

Please start immediately, use local resources and infer context from repo files. 

