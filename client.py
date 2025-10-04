# client.py

# -------------------------------------------------------------
# 1. COMBINED IMPORTS
# -------------------------------------------------------------
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # <-- Add this

from dotenv import load_dotenv
import asyncio
import os
from pathlib import Path
import sys

load_dotenv()

# Define a system prompt for a stunning persona
# client.py

SYSTEM_PROMPT = (
    "You are a helpful and meticulous 'Multi-Service Agent'. Your task is to process user "
    "requests and summarize tool output into a single, clean response. "
    "***CRITICAL INSTRUCTION: All formatting for the final response MUST be in standard HTML. "
    "You MUST use HTML tags (<b>, <br>, <ul>, <li>) for formatting. DO NOT use Markdown, "
    "LaTeX, or any other special symbols (like **, -, or $$) in your final output.***"
    "Ensure math results are presented as plain text within the HTML."
)

async def setup_agent():
    """Initializes the MultiServerMCPClient and the LangGraph agent."""
    
    # -------------------------------------------------------------
    # 2. CONFIGURATION SETUP (REINSTATED MISSING LOGIC)
    # -------------------------------------------------------------
    base = Path(__file__).resolve().parent
    math_server_path = str(base / "math_server.py")
    weather_server_path = str(base / "weather.py")

    client = MultiServerMCPClient(
        {
            "Math": {
                "command": sys.executable or "python",
                "args": [math_server_path],
                "transport": "stdio",
            },
            "Weather": {
                "command": sys.executable or "python",
                "args": [weather_server_path],
                "transport": "stdio",
            }
        }
    )

    # -------------------------------------------------------------
    # 3. KEY CHECK AND TOOL LOADING
    # -------------------------------------------------------------
    openai_key = os.getenv("my_api_key")
    if not openai_key:
        print("FATAL ERROR: 'my_api_key' not set in environment. Check your .env file." )
        raise ValueError("OpenAI API Key is missing.")

    try:
        # Load tools from the newly launched servers
        print("Attempting to launch and load tools from MCP servers...")
        tools = await client.get_tools()
        print(f"Successfully loaded {len(tools)} tools.")
    except Exception as e:
        print(f"FATAL ERROR: Failed to load tools from MCP servers: {e}")
        # Ensure cleanup on failure
        await client.aclose()
        raise

    # client.py (inside the setup_agent function)

    # -------------------------------------------------------------
    # 4. LLM WRAPPING FIX (System Prompt and Tool Binding)
    # -------------------------------------------------------------
    llm = ChatOpenAI(
        temperature=0, 
        model="gpt-4o-mini", 
        openai_api_key=openai_key
    )
    
    # 1. BIND TOOLS DIRECTLY TO THE MODEL
    # This is what create_react_agent expects to happen internally,
    # but since we are modifying the chain, we do it explicitly.
    llm_with_tools = llm.bind_tools(tools)
    
    # Define the template with the system message AND the MessagesPlaceholder
    prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        # FIX: Use MessagesPlaceholder to correctly accept the list of messages
        MessagesPlaceholder(variable_name="messages"), 
    ]
)

    
    # 3. COMBINE: Prompt Template is piped into the Tool-Bound LLM
    # The output of the prompt template (formatted messages) goes into the model.
    llm_with_prompt = prompt_template | llm_with_tools
    
    # 4. Create agent (PASS THE FINAL RUNNABLE SEQUENCE)
    # create_react_agent accepts a runnable sequence as its first argument.
    agent = create_react_agent(llm_with_prompt, tools)
    
    return agent, client

# This is the single entry point for the Streamlit/FastAPI app to use the agent
async def get_agent_response(agent, query: str):
    """Invokes the agent with a user query and returns the final response string."""
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    
    # Safely extract the final content
    try:
        msgs = response.get("messages") or []
        if msgs:
            last = msgs[-1]
            content = last.get("content") if isinstance(last, dict) else getattr(last, "content", None)
            return content
        return "Agent response was empty."
    except Exception:
        # This catches errors during parsing the response structure
        return "Error extracting final message content."

# The main function is only used if you run this file directly for quick testing
if __name__ == "__main__":
    async def quick_test():
        agent, client = await setup_agent()
        try:
            query = "What is (450 - 50) / 4, and what is the weather in Tokyo?"
            response_content = await get_agent_response(agent, query)
            print("\n--- AGENT RESPONSE ---")
            print(response_content)
        finally:
            # Cleanly shut down subprocesses
            print("\n--- Shutting down MCP Client subprocesses ---")
            await client.aclose()

    asyncio.run(quick_test())