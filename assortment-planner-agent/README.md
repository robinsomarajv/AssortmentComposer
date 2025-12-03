# Assortment Planner Agent

Composes store assortments by orchestrating Inventory, Procurement, and PO agents via A2A. LLM-provider agnostic (LiteLLM), fully instrumented with Langfuse, and follows ADK conventions.

## Setup

1. Copy `.env.example` to `.env` and fill in secrets.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the API:
   ```sh
   uvicorn api:app --reload --port 8000
   ```

## Endpoints
- `/assortment/plan` (POST): Plan assortment (session-aware)
- `/assortment/plan/stream` (GET): Streamed planning (SSE)
- `/health` (GET): Health check
- `/a2a`: A2A agent card

