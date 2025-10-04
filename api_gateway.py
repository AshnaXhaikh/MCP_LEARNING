from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os

# Import the core logic from your existing client.py
from client import setup_agent, get_agent_response, SYSTEM_PROMPT 

# --- FastAPI Setup ---
app = FastAPI(title="Concierge AI Gateway")

# Configure CORS to allow communication with the frontend.
# Set allow_origins=["*"] for local development environment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- State Management ---
AGENT = None
MCP_CLIENT = None

class Query(BaseModel):
    """Schema for the incoming JSON payload."""
    user_input: str

@app.on_event("startup")
async def startup_event():
    """Initializes the agent system when the FastAPI server starts."""
    global AGENT, MCP_CLIENT
    print("--- Initializing Concierge AI Agent System ---")
    try:
        AGENT, MCP_CLIENT = await setup_agent()
        print("--- Agent System Ready ---")
    except Exception as e:
        print(f"FATAL ERROR during startup: {e}")
        # Exit if the agent setup fails
        sys.exit(1)


@app.on_event("shutdown")
async def shutdown_event():
    """Shuts down the MCP client and its subprocesses."""
    global MCP_CLIENT
    if MCP_CLIENT:
        print("--- Shutting down MCP Client subprocesses ---")
        # FIX: Use ashutdown() instead of the non-existent aclose()
        await MCP_CLIENT.ashutdown() 
        print("--- MCP Client subprocesses shut down ---")


@app.post("/ask")
async def ask_agent(query: Query):
    """API endpoint to receive a user query and return the agent's response."""
    if not AGENT:
        return {"response": "Error: Agent system is not initialized.", "status": "error"}

    try:
        response_content = await get_agent_response(AGENT, query.user_input)
        
        return {
            "query": query.user_input,
            "response": response_content,
            "status": "success"
        }
    except Exception as e:
        print(f"Agent execution error: {e}")
        return {"response": "Sorry, an internal error occurred while processing your request.", "status": "error"}


@app.get("/status")
async def get_status():
    """Simple health check endpoint."""
    status = "ready" if AGENT else "initializing"
    return {"status": status, "system_message": SYSTEM_PROMPT}


if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="127.0.0.1", port=8000)
